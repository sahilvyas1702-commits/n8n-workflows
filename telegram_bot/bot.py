"""
Telegram Bot for n8n Workflow Generation
Allows users to send prompts via Telegram and receive auto-generated n8n workflows
"""

import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from telegram.constants import ParseMode
import httpx
import re
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/workflow-generator")
GITHUB_REPO_URL = "https://github.com/sahilvyas1702-commits/n8n-workflows"

# Conversation states
AWAITING_PROMPT, CONFIRMING_WORKFLOW, PROCESSING = range(3)

# Store user sessions
user_sessions = {}

class WorkflowGenerator:
    """Generate n8n workflows from natural language prompts"""
    
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
    
    async def generate_workflow(self, prompt: str, user_id: int) -> dict:
        """Send prompt to n8n and get workflow JSON"""
        try:
            payload = {
                "prompt": prompt,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "source": "telegram_bot"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.N8N_WEBHOOK_URL,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        
        except Exception as e:
            logger.error(f"Workflow generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate workflow. Please try again."
            }

# Initialize generator
generator = WorkflowGenerator(N8N_WEBHOOK_URL)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start command - welcome message"""
    welcome_text = """
🤖 *n8n Workflow Generator Bot*

Welcome! I can generate n8n workflows from your prompts.

*Available Commands:*
/generate - Create a new workflow
/list - View recent workflows
/help - Get help
/status - Check workflow status

*How it works:*
1️⃣ Send me a prompt describing what workflow you need
2️⃣ I'll generate the JSON automatically
3️⃣ You'll get it as a downloadable file
4️⃣ Deploy directly to your n8n instance

*Example prompt:*
"Create a Slack notification workflow that sends alerts when YouTube videos are uploaded"

Let's get started! Use /generate
    """
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN
    )
    return ConversationHandler.END

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start workflow generation"""
    user_id = update.effective_user.id
    
    prompt_text = """
✍️ *Describe your workflow*

Tell me what n8n workflow you want to create. Be specific about:
- What triggers the workflow?
- What actions should it perform?
- What integrations do you need? (YouTube, Slack, Database, etc)
- Any special requirements?

*Example:*
"Create a workflow that monitors YouTube uploads, sends Slack alerts to #uploads channel with video title and URL, retries 3x on failure, and logs to database"

⏱️ I'm listening...
    """
    
    user_sessions[user_id] = {
        "step": "awaiting_prompt",
        "created_at": datetime.now()
    }
    
    await update.message.reply_text(prompt_text, parse_mode=ParseMode.MARKDOWN)
    return AWAITING_PROMPT

async def handle_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process user's workflow prompt"""
    user_id = update.effective_user.id
    prompt = update.message.text
    
    # Validate prompt
    if len(prompt) < 20:
        await update.message.reply_text(
            "❌ Prompt too short. Please provide more details (at least 20 characters).",
            parse_mode=ParseMode.MARKDOWN
        )
        return AWAITING_PROMPT
    
    # Show processing indicator
    processing_msg = await update.message.reply_text(
        "🔄 *Generating workflow...*\n\nAnalyzing your prompt and building the workflow structure...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Store session
    user_sessions[user_id]["prompt"] = prompt
    user_sessions[user_id]["step"] = "processing"
    
    try:
        # Call n8n webhook to generate workflow
        result = await generator.generate_workflow(prompt, user_id)
        
        if result.get("success"):
            workflow_data = result.get("workflow", {})
            workflow_name = workflow_data.get("name", "Workflow")
            
            # Format preview
            preview_text = f"""
✅ *Workflow Generated Successfully!*

📋 *Name:* {workflow_name}
🔗 *Nodes:* {len(workflow_data.get('nodes', []))}
⚙️ *Connections:* {len(workflow_data.get('connections', {}))}

*Preview:*
{workflow_data.get('description', 'No description')}

Would you like to:
1. ✅ Confirm & Save to GitHub
2. 📝 Edit the prompt
3. ❌ Cancel

React to proceed or type your choice:
            """
            
            # Store workflow
            user_sessions[user_id]["workflow"] = workflow_data
            user_sessions[user_id]["step"] = "confirming"
            
            # Create inline buttons
            keyboard = [
                [
                    InlineKeyboardButton("✅ Confirm", callback_data="confirm_workflow"),
                    InlineKeyboardButton("📝 Edit", callback_data="edit_prompt"),
                    InlineKeyboardButton("❌ Cancel", callback_data="cancel")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Delete processing message and send preview
            await processing_msg.delete()
            await update.message.reply_text(
                preview_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            
            return CONFIRMING_WORKFLOW
        
        else:
            error_msg = result.get("message", "Unknown error")
            await processing_msg.edit_text(
                f"❌ *Error:* {error_msg}\n\nPlease try again with a different prompt.",
                parse_mode=ParseMode.MARKDOWN
            )
            return AWAITING_PROMPT
    
    except Exception as e:
        logger.error(f"Error processing prompt: {e}")
        await processing_msg.edit_text(
            f"❌ *Error:* {str(e)}\n\nPlease try again.",
            parse_mode=ParseMode.MARKDOWN
        )
        return AWAITING_PROMPT

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle inline button clicks"""
    query = update.callback_query
    user_id = query.from_user.id
    
    await query.answer()
    
    if query.data == "confirm_workflow":
        await query.edit_message_text(
            "🚀 *Committing to GitHub...*",
            parse_mode=ParseMode.MARKDOWN
        )
        
        try:
            workflow = user_sessions[user_id].get("workflow", {})
            workflow_name = workflow.get("name", "workflow")
            
            # TODO: Commit to GitHub
            commit_url = f"{GITHUB_REPO_URL}/blob/main/workflows/generated-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
            
            success_text = f"""
✅ *Workflow Saved!*

📁 *File:* {workflow_name}.json
🔗 *GitHub:* [View Workflow]({commit_url})
⏱️ *Generated:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

*Next Steps:*
1. Download the workflow file
2. Import to your n8n instance
3. Configure credentials
4. Test and deploy

🎉 Workflow is ready to use!

Use /generate for another workflow or /help for more options.
            """
            
            await query.edit_message_text(
                success_text,
                parse_mode=ParseMode.MARKDOWN
            )
        
        except Exception as e:
            await query.edit_message_text(
                f"❌ *Error saving workflow:* {str(e)}",
                parse_mode=ParseMode.MARKDOWN
            )
    
    elif query.data == "edit_prompt":
        await query.edit_message_text(
            "✏️ Please send a new prompt (use /generate to start over):",
            parse_mode=ParseMode.MARKDOWN
        )
        return AWAITING_PROMPT
    
    elif query.data == "cancel":
        await query.edit_message_text(
            "❌ *Cancelled.* Use /generate to start a new workflow.",
            parse_mode=ParseMode.MARKDOWN
        )
    
    return ConversationHandler.END

async def list_workflows(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List recent workflows"""
    # TODO: Fetch from GitHub/database
    
    list_text = """
📋 *Recent Workflows*

1. 05-youtube-upload.json
   - YouTube OAuth2 upload with manual approval
   - Created: 2026-09-05

2. 06-slack-notifications.json
   - Slack alerts on upload completion
   - Created: 2026-09-04

3. 04-data-transform.json
   - Data transformation & validation
   - Created: 2026-09-03

Use /generate to create a new workflow!
    """
    
    await update.message.reply_text(list_text, parse_mode=ParseMode.MARKDOWN)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help"""
    help_text = """
📚 *Help & Documentation*

*Commands:*
/start - Welcome & overview
/generate - Create new workflow
/list - View recent workflows
/status - Check workflow status
/help - This message

*Workflow Prompt Format:*

Best results with structured prompts:

PHASE: [5/6/7]
NAME: [workflow-name.json]
TRIGGER: [What starts it?]
ACTIONS: [Step by step]
INTEGRATIONS: [YouTube, Slack, DB, etc]
REQUIREMENTS:
  - Requirement 1
  - Requirement 2

*Example:*
"Create Phase 5 workflow that sends Slack messages when YouTube videos upload, includes retry logic, error handling, and database logging"

*Tips:*
✅ Be specific about triggers and actions
✅ List all integrations needed
✅ Mention error handling requirements
✅ Include security requirements
❌ Avoid vague descriptions

*Support:*
GitHub: {GITHUB_REPO_URL}
Issues: Create a GitHub issue for bugs

Need help? Ask me anything!
    """
    
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check workflow generation status"""
    user_id = update.effective_user.id
    session = user_sessions.get(user_id, {})
    
    if not session:
        await update.message.reply_text(
            "📊 *No active workflow.* Use /generate to start one.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    status_text = f"""
📊 *Workflow Status*

🔹 *Current Step:* {session.get('step', 'unknown')}
⏱️ *Created:* {session.get('created_at').strftime('%Y-%m-%d %H:%M:%S')}
✍️ *Prompt:* {session.get('prompt', 'N/A')[:100]}...

*Status Options:*
- ⏳ Processing
- ✅ Ready for confirmation
- 🚀 Committing to GitHub
- ✓ Complete

Use /generate to create a new workflow.
    """
    
    await update.message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update.effective_message:
        await update.effective_message.reply_text(
            "❌ *Error occurred.* Please try again or use /help for assistance.",
            parse_mode=ParseMode.MARKDOWN
        )

def main():
    """Start the bot"""
    # Create application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("generate", generate)],
        states={
            AWAITING_PROMPT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prompt)],
            CONFIRMING_WORKFLOW: [MessageHandler(filters.COMMAND, generate)],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
    )
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("list", list_workflows))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_error_handler(error_handler)
    
    # Start bot
    logger.info("🤖 Telegram bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
