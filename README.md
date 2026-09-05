# 🚀 n8n Workflow Automation Platform

A complete automation suite combining **n8n workflows** with a **Telegram bot** for intelligent workflow generation, YouTube uploads, and enterprise-grade automation.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📌 Features

### 🎬 Phase 4: YouTube Upload Workflow
- ✅ OAuth2 authentication (no hardcoded secrets)
- ✅ Manual approval gate before publishing
- ✅ Default private/unlisted uploads
- ✅ Resumable uploads with 3-retry logic
- ✅ Quota error handling
- ✅ Duplicate prevention with audit logs
- ✅ Full input validation

### 🤖 Phase 5: Telegram Workflow Generator
- ✅ Send prompts via Telegram
- ✅ AI-powered workflow generation
- ✅ Auto-commit to GitHub
- ✅ Real-time notifications
- ✅ Complete privacy (only you can access)
- ✅ No external data collection

### 🔧 Supported Integrations
- YouTube (OAuth2)
- Slack
- PostgreSQL/MySQL
- GitHub
- Email
- Webhooks
- HTTP APIs

---

## 🚀 Quick Start

### 1️⃣ Prerequisites
- Python 3.8+
- Docker & Docker Compose (optional)
- Telegram account
- n8n instance (included in docker-compose)

### 2️⃣ Clone Repository
```bash
git clone https://github.com/sahilvyas1702-commits/n8n-workflows.git
cd n8n-workflows
```

### 3️⃣ Setup Telegram Bot
```bash
# Create bot with @BotFather
# Get your user ID from @userinfobot

# Copy environment template
cp telegram_bot/.env.example telegram_bot/.env

# Edit with your credentials
nano telegram_bot/.env
```

### 4️⃣ Run with Docker
```bash
docker-compose up -d
```

Or locally:
```bash
pip install -r telegram_bot/requirements.txt
python telegram_bot/bot.py
```

### 5️⃣ Start Using
- Open Telegram
- Search: `your_username_bot`
- Send: `/start`
- Send: `/generate`

---

## 📂 Project Structure

```
n8n-workflows/
├── workflows/
│   ├── 05-youtube-upload.json          # YouTube upload with approval
│   └── 06-telegram-processor.json      # Telegram prompt processor
├── telegram_bot/
│   ├── bot.py                          # Main Telegram bot
│   ├── requirements.txt                # Python dependencies
│   ├── Dockerfile                      # Bot containerization
│   └── .env.example                    # Environment template
├── docker-compose.yml                  # Complete stack setup
├── QUICK_START.md                      # Fast setup guide
├── TELEGRAM_BOT_SETUP.md              # Detailed bot guide
└── README.md                           # This file
```

---

## 🎯 Usage Examples

### Generate Workflow via Telegram
```
You: /generate
Bot: ✍️ Describe your workflow...

You: Create a Slack notification workflow that sends alerts 
     when YouTube videos are uploaded

Bot: 🔄 Generating workflow...
Bot: ✅ Workflow Generated!
     [Shows preview]
     
You: [Click ✅ Confirm]

Bot: ✅ Workflow Saved!
     GitHub: [Link to workflow]
```

### Upload Video with Approval
1. Send video metadata to YouTube workflow
2. Workflow pauses for manual approval
3. Click approve in n8n UI
4. Video uploads automatically
5. Audit log created

### Monitor Workflows
```bash
# View logs
tail -f telegram_bot/logs/telegram_bot.log

# Check workflow status
docker-compose logs n8n

# Database queries
docker-compose exec postgres psql -U workflows
```

---

## 🔐 Security

### ✅ Best Practices Implemented
- No hardcoded secrets (uses n8n credentials)
- Environment variables for sensitive data
- OAuth2 for API authentication
- `.gitignore` prevents accidental commits
- User ID validation for Telegram bot
- Audit logging for all actions

### 🛡️ Secrets Management
```bash
# Never commit secrets
echo ".env" >> .gitignore

# Use environment variables
export TELEGRAM_BOT_TOKEN="your_token"
export GITHUB_TOKEN="your_token"

# Or use .env file (not committed)
cp telegram_bot/.env.example telegram_bot/.env
# Edit with real values
```

---

## 📋 Available Commands

### Telegram Bot
| Command | Purpose |
|---------|---------|
| `/start` | Welcome & overview |
| `/generate` | Create new workflow |
| `/list` | View recent workflows |
| `/status` | Check workflow status |
| `/help` | Show help & examples |
| `/settings` | Configure bot |
| `/feedback` | Send feedback |

### Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f telegram-bot

# Stop services
docker-compose down

# Rebuild images
docker-compose up -d --build
```

---

## 🔧 Configuration

### Environment Variables
See `telegram_bot/.env.example` for all options:
```bash
TELEGRAM_BOT_TOKEN=your_token_here
YOUR_TELEGRAM_USER_ID=your_user_id
N8N_WEBHOOK_URL=http://localhost:5678/webhook/workflow-generator
GITHUB_TOKEN=your_github_token
GITHUB_OWNER=your_github_username
GITHUB_REPO=n8n-workflows
```

### n8n Setup
1. Access at `http://localhost:5678`
2. Create credentials for YouTube, Slack, etc.
3. Import workflows from `workflows/` directory
4. Set up webhooks for Telegram integration

### Database (PostgreSQL)
```bash
# Access database
docker-compose exec postgres psql -U workflows -d workflow_logs

# View audit logs
SELECT * FROM audit_logs;

# Check workflow history
SELECT * FROM workflow_executions;
```

---

## 📖 Documentation

- **[Quick Start](QUICK_START.md)** - 2-minute setup guide
- **[Telegram Bot Setup](TELEGRAM_BOT_SETUP.md)** - Detailed configuration
- **[YouTube Workflow](workflows/05-youtube-upload.json)** - Upload specifications
- **[Telegram Processor](workflows/06-telegram-processor.json)** - Prompt processing

---

## 🐛 Troubleshooting

### Bot Not Responding
```bash
# Check if running
docker-compose ps

# View logs
docker-compose logs telegram-bot

# Restart
docker-compose restart telegram-bot
```

### Workflows Not Saving
```bash
# Check GitHub token
echo $GITHUB_TOKEN

# Verify repo access
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GITHUB_OWNER/$GITHUB_REPO
```

### Connection Issues
```bash
# Test n8n connectivity
curl http://localhost:5678/health

# Test Telegram API
curl https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe
```

---

## 🚢 Deployment

### Local Development
```bash
python telegram_bot/bot.py
```

### Docker (Recommended)
```bash
docker-compose up -d
```

### Cloud Platforms
- **Railway.app** - Free tier, 500 hours/month
- **Render.com** - Free tier available
- **DigitalOcean** - $6/month
- **AWS EC2** - Free tier 12 months
- **Heroku** - Paid (was free)

See deployment guide for detailed instructions.

---

## 📊 Workflow Phases

| Phase | Name | Status |
|-------|------|--------|
| 4 | YouTube Upload | ✅ Complete |
| 5 | Telegram Bot | ✅ Complete |
| 6 | Workflow Processor | ✅ Complete |
| 7+ | Future Phases | 🔄 Coming Soon |

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Support

- **GitHub Issues** - Report bugs or request features
- **Telegram Bot** - Use `/feedback` command
- **Documentation** - Check QUICK_START.md or TELEGRAM_BOT_SETUP.md
- **Logs** - Check `telegram_bot/logs/telegram_bot.log`

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with [n8n](https://n8n.io)
- Telegram Bot integration via [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Inspired by workflow automation best practices

---

## 🎯 Roadmap

- [ ] Phase 7: Email & SMS notifications
- [ ] Phase 8: Advanced AI integration
- [ ] Phase 9: Analytics dashboard
- [ ] Phase 10: Multi-language support
- [ ] Web UI for workflow management
- [ ] Mobile app for status monitoring

---

**Made with ❤️ by the Automation Team**

**Start now:** Follow [QUICK_START.md](QUICK_START.md) → 🚀
