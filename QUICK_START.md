# 🚀 Quick Start - Telegram Workflow Generator

## ⚡ 2-Minute Setup

### 1. Create Your Telegram Bot
```bash
# Open Telegram
# Search: @BotFather
# Send: /newbot
# Follow prompts
# Copy token: 123456789:ABCDefGHIjklMNOpqrsTUVwxyz
```

### 2. Get Your User ID
```bash
# Open Telegram
# Search: @userinfobot
# Send: /start
# Copy your ID: 123456789
```

### 3. Clone & Setup
```bash
git clone https://github.com/sahilvyas1702-commits/n8n-workflows.git
cd n8n-workflows

# Create .env file
cp telegram_bot/.env.example telegram_bot/.env

# Edit .env with your values:
# TELEGRAM_BOT_TOKEN=your_token_here
# YOUR_TELEGRAM_USER_ID=your_id_here
```

### 4. Install & Run
```bash
pip install -r telegram_bot/requirements.txt
python telegram_bot/bot.py
```

### 5. Start Using
- Open Telegram
- Search: `your_username_bot`
- Send: `/start`
- Send: `/generate`
- Type your prompt!

---

## 🎯 Example Prompts

### Simple:
```
"Create a workflow that sends Slack messages when something happens"
```

### Detailed:
```
"Create Phase 5 workflow that:
- Monitors YouTube upload completion
- Sends Slack alert to #uploads channel
- Includes video title, URL, privacy status
- Retries 3x on network error
- Logs to PostgreSQL database
- No hardcoded tokens
"
```

### Structured:
```
PHASE: 5
NAME: 06-slack-notifications.json
TRIGGER: YouTube upload completes
ACTIONS:
  1. Parse upload metadata
  2. Format Slack message
  3. Send to #uploads channel
  4. Log to database
  5. Notify on error
INTEGRATIONS: YouTube, Slack, PostgreSQL
REQUIREMENTS:
  - No hardcoded secrets
  - Retry 3x
  - 5 min timeout
OUTPUT: Success/error response
```

---

## 📋 Available Commands

| Command | What it does |
|---------|-------------|
| `/start` | Welcome message & overview |
| `/generate` | Create a new workflow |
| `/list` | Show recent workflows |
| `/status` | Check current workflow status |
| `/help` | Show help & examples |
| `/settings` | Configure bot settings |
| `/feedback` | Send feedback |

---

## ✅ Complete Workflow

```
You: /generate
Bot: ✍️ Describe your workflow...

You: Create a workflow that sends Slack notifications 
     when YouTube videos are uploaded

Bot: 🔄 Generating workflow...

Bot: ✅ Workflow Generated!
     [Shows preview]
     
     Would you like to:
     ✅ Confirm & Save
     📝 Edit
     ❌ Cancel

You: [Click ✅ Confirm]

Bot: 🚀 Committing to GitHub...
     
     ✅ Workflow Saved!
     📁 File: slack-notifications.json
     🔗 GitHub: [Link]
     
     Ready to use! 🎉
```

---

## 🔧 Troubleshooting

**Bot doesn't start:**
```bash
# Check Python version (3.8+)
python --version

# Check token
echo $TELEGRAM_BOT_TOKEN

# Reinstall dependencies
pip install --upgrade -r telegram_bot/requirements.txt
```

**Bot doesn't respond:**
- Verify bot is running
- Check bot token in `.env`
- Restart: `Ctrl+C` then `python telegram_bot/bot.py`

**Workflows not saving:**
- Check GitHub token
- Verify repo name
- Check file permissions

---

## 🌍 Deploy 24/7

### Docker
```bash
docker build -t workflow-bot telegram_bot/
docker run -e TELEGRAM_BOT_TOKEN="your-token" workflow-bot
```

### Cloud Hosting
- **Railway.app** (Free tier)
- **Render.com** (Free tier)
- **Replit** (Free tier)
- **AWS Lambda** (Free tier 12 months)

---

## 📞 Support

- GitHub Issues: Report bugs
- Telegram: Use `/feedback` command
- Logs: Check `telegram_bot.log`

---

## ✨ Features

✅ Natural language to n8n workflow  
✅ Auto-commit to GitHub  
✅ Approval workflow integration  
✅ Error handling & retries  
✅ Telegram notifications  
✅ Completely private (only you access)  
✅ No external data collection  
✅ Run anywhere (local, Docker, cloud)  

---

**Ready?** Start with: `python telegram_bot/bot.py` 🚀
