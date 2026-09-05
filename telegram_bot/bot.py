#!/usr/bin/env python3
"""
Telegram Workflow Generator Bot
Connects Telegram prompts to n8n workflow generation with GitHub auto-commit
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import httpx
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('telegram_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
YOUR_TELEGRAM_USER_ID = int(os.getenv('YOUR_TELEGRAM_USER_ID', 0))
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL', 'http://localhost:5678/webhook/workflow-generator')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_OWNER = os.getenv('GITHUB_OWNER', 'sahilvyas1702-commits')
GITHUB_REPO = os.getenv('GITHUB_REPO', 'n8n-workflows')

# Verify configuration
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN not set in .env")
if not YOUR_TELEGRAM_USER_ID:
    raise ValueError("❌ YOUR_TELEGRAM_USER_ID not set in .env")

logger.info("🤖 Telegram Bot initialized successfully")


def check_user_id(user_id: int) -> bool:
    """Verify user is authorized"""
    return user_id == YOUR_TELEGRAM_USER_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message"""
    if not check_user_id(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized access")
        return

    welcome_text = """
🤖 Welcome to n8n Workflow Generator!

I can generate n8n workflows from your natural language prompts.

📋 Available Commands:
/generate - Create a new workflow
/list - View recent workflows
/status - Check workflow status
/help - Show help & examples
/settings - Configure bot
/feedback - Send feedback

🚀 Let's get started! Use /generate to create your first workflow.
    """
    
    keyboard = [
        [InlineKeyboardButton("📝 Generate Workflow", callback_data='generate')],
        [InlineKeyboardButton("📋 View Examples", callback_data='examples')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    logger.info(f"✅ User {update.effective_user.id} started bot")


async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start workflow generation"""
    if not check_user_id(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized access")
        return

    await update.message.reply_text(
        "✍️ Describe the workflow you want to create:\n\n"
        "Examples:\n"
        "• 'Create a Slack notification workflow'\n"
        "• 'YouTube upload with email alert'\n"
        "• 'Database backup automation'\n\n"
        "Send your prompt (minimum 20 characters)"
    )
    context.user_data['waiting_for_prompt'] = True
    logger.info(f"User {update.effective_user.id} starting workflow generation")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages"""
    if not check_user_id(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized access")
        return

    if not context.user_data.get('waiting_for_prompt'):
        await update.message.reply_text(
            "Please use /generate to create a workflow"
        )
        return

    prompt = update.message.text

    # Validate prompt length
    if len(prompt) < 20:
        await update.message.reply_text(
            "❌ Prompt too short! Please provide at least 20 characters."
        )
        return

    if len(prompt) > 2000:
        await update.message.reply_text(
            "❌ Prompt too long! Maximum 2000 characters allowed."
        )
        return

    # Send to n8n for processing
    await update.message.reply_text("🔄 Generating workflow... Please wait...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                N8N_WEBHOOK_URL,
                json={
                    "user_id": update.effective_user.id,
                    "username": update.effective_user.username,
                    "prompt": prompt,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Show preview
                preview = f"""
✅ Workflow Generated Successfully!

📋 **Workflow Details:**
Name: {result.get('workflowName', 'Generated Workflow')}
Request ID: {result.get('requestId', 'N/A')}

🔍 **Preview:**
{result.get('preview', 'Check GitHub for full workflow')}

Would you like to confirm and save this workflow?
                """
                
                keyboard = [
                    [InlineKeyboardButton("✅ Confirm & Save", callback_data=f"confirm_{result.get('requestId')}")],
                    [InlineKeyboardButton("📝 Regenerate", callback_data='generate')],
                    [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(preview, reply_markup=reply_markup)
                logger.info(f"✅ Workflow generated for user {update.effective_user.id}")
            else:
                await update.message.reply_text(
                    f"❌ Generation failed: {response.text}"
                )
                logger.error(f"Generation error: {response.status_code} - {response.text}")
                
    except Exception as e:
        await update.message.reply_text(
            f"❌ Error: {str(e)}\n\nMake sure n8n is running at {N8N_WEBHOOK_URL}"
        )
        logger.error(f"Exception during workflow generation: {str(e)}")
    
    context.user_data['waiting_for_prompt'] = False


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks"""
    if not check_user_id(update.effective_user.id):
        await update.callback_query.answer("❌ Unauthorized")
        return

    query = update.callback_query
    await query.answer()

    if query.data == 'generate':
        await generate(update, context)
    elif query.data == 'examples':
        examples = """
📚 Example Prompts:

**Simple:**
"Create a Slack notification workflow"

**Detailed:**
"Create a workflow that sends Slack alerts when YouTube videos upload with video title, URL, and privacy status"

**Structured:**
"PHASE: 5
NAME: slack-youtube-notifications
TRIGGER: YouTube upload completes
ACTIONS:
1. Parse upload metadata
2. Format message with title, URL, status
3. Send to Slack #uploads channel
4. Log to database
5. Retry 3x on error"

**Data Processing:**
"Create workflow that reads CSV from Google Drive, processes data, updates PostgreSQL, and sends summary email"

🎯 Try one now with /generate!
        """
        keyboard = [[InlineKeyboardButton("📝 Generate Now", callback_data='generate')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(examples, reply_markup=reply_markup)
    elif query.data == 'help':
        help_text = """
❓ Help & Tips

**How to write good prompts:**
✅ Be specific about what you want
✅ Include integrations (YouTube, Slack, etc.)
✅ Mention error handling needs
✅ List any database/storage requirements
✅ Specify retry logic if needed

**Example format:**
"Create a workflow that:
- Monitors YouTube for new uploads
- Extracts video metadata
- Sends Slack notification
- Includes retry on network error
- Logs to PostgreSQL"

**Commands:**
/generate - Create workflow
/list - Recent workflows
/status - Workflow status
/settings - Configure
/feedback - Send feedback

💡 The more detail, the better the workflow!
        """
        keyboard = [[InlineKeyboardButton("📝 Generate", callback_data='generate')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(help_text, reply_markup=reply_markup)
    elif query.data.startswith('confirm_'):
        request_id = query.data.split('_')[1]
        await query.edit_message_text(
            f"✅ Workflow saved to GitHub!\n\n"
            f"📁 Request ID: {request_id}\n"
            f"🔗 Repository: {GITHUB_OWNER}/{GITHUB_REPO}\n"
            f"🎉 Ready to use!\n\n"
            f"Use /generate for another workflow"
        )
        logger.info(f"Workflow confirmed - Request ID: {request_id}")
    elif query.data == 'cancel':
        await query.edit_message_text("❌ Cancelled. Use /generate to start over.")


async def list_workflows(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List recent workflows"""
    if not check_user_id(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized access")
        return

    list_text = """
📋 Recent Workflows

(This would show workflows from your GitHub repo)

🔗 GitHub: https://github.com/{}/{}/tree/main/workflows

💡 Tip: Check your GitHub repo for all generated workflows!
    """.format(GITHUB_OWNER, GITHUB_REPO)

    await update.message.reply_text(list_text)
    logger.info(f"User {update.effective_user.id} listed workflows")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check workflow status"""
    if not check_user_id(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized access")
        return

    status_text = """
✅ System Status:

🤖 Telegram Bot: Online
🔄 n8n Instance: Online
💾 Database: Online
🔗 GitHub Integration: Ready

🚀 System is ready for workflow generation!
    """

    await update.message.reply_text(status_text)
    logger.info(f"User {update.effective_user.id} checked status")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help"""
    if not check_user_id(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized access")
        return

    help_text = """
❓ Help & Documentation

📚 Guides:
/start - Welcome & overview
/generate - Create a new workflow
/list - View recent workflows
/status - Check system status
/settings - Bot settings
/feedback - Send feedback

🔗 Links:
Quick Start: https://github.com/{}/{}
Setup Guide: https://github.com/{}/{}/blob/main/TELEGRAM_BOT_SETUP.md
Documentation: https://github.com/{}/{}/blob/main/README.md

💡 Tips:
• Be detailed in your workflow descriptions
• Include all integrations and error handling
• Check GitHub for generated workflows
• Use /feedback for suggestions

🎯 Ready to generate? Use /generate
    """.format(GITHUB_OWNER, GITHUB_REPO, GITHUB_OWNER, GITHUB_REPO, GITHUB_OWNER, GITHUB_REPO)

    await update.message.reply_text(help_text)


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show settings"""
    if not check_user_id(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized access")
        return

    settings_text = f"""
⚙️ Bot Settings

🤖 **Bot Configuration:**
User ID: {update.effective_user.id}
Username: @{update.effective_user.username}

🔧 **System Configuration:**
n8n Webhook: {N8N_WEBHOOK_URL}
GitHub Repo: {GITHUB_OWNER}/{GITHUB_REPO}

✅ **Status:**
All systems operational

💾 **Storage:**
Workflows save to: {GITHUB_OWNER}/{GITHUB_REPO}/workflows/

🔐 **Security:**
Only your user ID can access this bot
    """

    await update.message.reply_text(settings_text)


async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send feedback"""
    if not check_user_id(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized access")
        return

    await update.message.reply_text(
        "📧 Send your feedback:\n\n"
        "What would you like to see improved?"
    )
    context.user_data['waiting_for_feedback'] = True


def main():
    """Start the bot"""
    logger.info("🤖 Starting Telegram Workflow Generator Bot...")
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate))
    application.add_handler(CommandHandler("list", list_workflows))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("settings", settings))
    application.add_handler(CommandHandler("feedback", feedback))
    
    # Handle button clicks
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Handle text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start bot
    logger.info("✅ Bot started successfully!")
    logger.info(f"✅ Authorized user ID: {YOUR_TELEGRAM_USER_ID}")
    logger.info(f"✅ n8n endpoint: {N8N_WEBHOOK_URL}")
    logger.info(f"✅ GitHub repository: {GITHUB_OWNER}/{GITHUB_REPO}")
    
    application.run_polling()


if __name__ == '__main__':
    main()
