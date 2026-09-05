# Telegram Bot Setup Guide - Personal Instance

## 🤖 Quick Start (5 minutes)

### Step 1: Create Your Personal Bot with BotFather

1. Open Telegram and search for **@BotFather**
2. Send `/start`
3. Send `/newbot`
4. Follow the prompts:
   - Bot name: `Workflow Generator` (or anything you want)
   - Bot username: `your_name_workflow_bot` (must be unique, ends with `_bot`)
5. BotFather will give you a **TOKEN** - copy it!

Example:
```
🎉 Done! Congratulations on your new bot. You will find it at t.me/your_name_workflow_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands.

Use this token to access the HTTP API:
123456789:ABCDefGHIjklMNOpqrsTUVwxyz
```

---

### Step 2: Set Your Bot Token

Create a `.env` file in your repository:

```bash
# .env
TELEGRAM_BOT_TOKEN=123456789:ABCDefGHIjklMNOpqrsTUVwxyz
N8N_WEBHOOK_URL=http://your-n8n-instance:5678/webhook/workflow-generator
YOUR_TELEGRAM_USER_ID=123456789
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
```

**Where to find YOUR_TELEGRAM_USER_ID:**
1. Open Telegram
2. Search for **@userinfobot**
3. Send `/start`
4. It shows your ID

---

### Step 3: Install & Run Bot

```bash
# Clone repository
git clone https://github.com/sahilvyas1702-commits/n8n-workflows.git
cd n8n-workflows

# Install dependencies
pip install -r telegram_bot/requirements.txt

# Run bot
python telegram_bot/bot.py
```

Output:
```
INFO - 🤖 Telegram bot starting...
INFO - Bot polling started
```

---

### Step 4: Start Using It

1. Open your bot: `t.me/your_name_workflow_bot`
2. Send `/start`
3. Send `/generate`
4. Type your prompt

---

## 🔒 Security & Privacy

✅ **Only YOU can access** (restricted to your Telegram user ID)
✅ **No data collection** - everything local to your bot
✅ **No external access** - runs on your own infrastructure
✅ **No logging** of your prompts
✅ **Direct GitHub integration** - commits go to your repo
✅ **Complete control** - you own the bot token

---

## 📋 Commands Available

| Command | Purpose |
|---------|---------|
| `/start` | Welcome & overview |
| `/generate` | Create new workflow |
| `/list` | View recent workflows |
| `/status` | Check current workflow |
| `/help` | Show help & examples |
| `/settings` | Bot configuration |
| `/feedback` | Send feedback |

---

## 🚀 Advanced: Host Bot 24/7

### Option A: Your Computer (Simple)
```bash
# Keep running in terminal
python telegram_bot/bot.py

# Or use screen/tmux
screen -S telegram-bot
python telegram_bot/bot.py
# Ctrl+A then D to detach
```

### Option B: Docker (Recommended)
```dockerfile
# Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY telegram_bot/requirements.txt .
RUN pip install -r requirements.txt
COPY telegram_bot/ .
CMD ["python", "bot.py"]
```

```bash
# Build & run
docker build -t telegram-workflow-bot .
docker run -e TELEGRAM_BOT_TOKEN="your-token" telegram-workflow-bot
```

### Option C: Cloud Hosting (Free)
- **Railway.app** (free tier, 500 hours/month)
- **Heroku** (requires payment now, but was free)
- **Render.com** (free tier available)
- **DigitalOcean** ($6/month)
- **AWS EC2** (free tier 12 months)

---

## 💬 Example Conversation Flow

```
You: /start

Bot: 🤖 n8n Workflow Generator Bot
     Welcome! I can generate n8n workflows from your prompts.
     
     Available Commands:
     /generate - Create a new workflow
     /list - View recent workflows
     /help - Get help
     /status - Check workflow status
     
     Let's get started! Use /generate

---

You: /generate

Bot: ✍️ Describe your workflow
     
     Tell me what n8n workflow you want to create...
     
     ⏱️ I'm listening...

---

You: Create a Slack notification workflow that sends alerts 
     when YouTube videos are uploaded, includes retry logic 
     and database logging

Bot: 🔄 Generating workflow...
     Analyzing your prompt and building the workflow structure...

[After generation]

Bot: ✅ Workflow Generated Successfully!
     
     📋 Name: Slack Notifications
     🔗 Nodes: 18
     ⚙️ Connections: 17
     
     Would you like to:
     1. ✅ Confirm & Save to GitHub
     2. 📝 Edit the prompt
     3. ❌ Cancel
     
     [Buttons appear]

You: [Click ✅ Confirm]

Bot: 🚀 Committing to GitHub...
     
     ✅ Workflow Saved!
     
     📁 File: slack-notifications.json
     🔗 GitHub: [Link to workflow]
     ⏱️ Generated: 2026-09-05 11:30:45
     
     Next Steps:
     1. Download the workflow file
     2. Import to your n8n instance
     3. Configure credentials
     4. Test and deploy
     
     🎉 Workflow is ready to use!
     Use /generate for another workflow or /help for more options.
```

---

## 🔐 Privacy Checklist

- [ ] Created bot with @BotFather
- [ ] Set `YOUR_TELEGRAM_USER_ID` in `.env`
- [ ] `.env` file in `.gitignore` (never commit secrets)
- [ ] Bot token stored only locally
- [ ] No third-party API tracking
- [ ] All workflows stored in your GitHub repo
- [ ] Only you have access to bot token

---

## 🆘 Troubleshooting

**"Bot doesn't respond"**
- Check bot is running: `python telegram_bot/bot.py`
- Verify token in `.env`
- Restart bot

**"Permission denied"**
- Check your Telegram user ID
- Make sure it matches in `.env`

**"Can't connect to n8n"**
- Verify n8n webhook URL in `.env`
- Check n8n is running on correct port
- Test webhook manually

**"Workflows not saving to GitHub"**
- Verify GitHub token in `.env`
- Check repo accessibility
- Ensure correct repo name

---

## 📞 Support

- **GitHub Issues:** Create issue in your repo
- **Telegram:** Message your bot with `/feedback`
- **Logs:** Check `telegram_bot.log` file

---

## ✅ Complete! You're Ready

1. ✅ Created personal bot
2. ✅ Got bot token
3. ✅ Set `.env` file
4. ✅ Running bot locally
5. ✅ Start generating workflows!

**Start with:** Open Telegram → Search `your_name_workflow_bot` → Send `/start`

🎉 Welcome to automated workflow generation!
