# AI Chatbot - Production Ready

A production-ready AI chatbot backend with Framer frontend integration. Built with Flask, OpenAI GPT-4-mini, and deployed via Docker.

---

## 🎯 What Is This?

A complete AI chatbot system that:
- **Backend**: Flask API that handles chat requests via OpenAI
- **Frontend**: React/TypeScript widget for Framer websites
- **Notifications**: Pushover alerts for every user message
- **Production**: Docker container ready for Render.com deployment

---

## ✨ Features

- ✅ AI-powered responses using OpenAI GPT-4-mini
- ✅ Real-time chat with conversation history
- ✅ CORS-enabled API for frontend integration
- ✅ Pushover notifications for monitoring
- ✅ Health check endpoint for uptime monitoring
- ✅ Docker containerization
- ✅ Production-ready security
- ✅ Minimalist black & white Framer widget
- ✅ Mobile responsive design

---

## 📁 Project Structure

```
my_chatbot/
├── app.py                      # Flask backend application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Production Docker configuration
├── .dockerignore              # Docker build exclusions
├── .env.example               # Environment variables template
├── .gitignore                 # Git exclusions
├── me/                        # Personal information for AI
│   ├── linkedin.pdf           # LinkedIn profile
│   ├── summary.txt            # Professional summary
│   ├── career.txt             # Career history
│   ├── childhood.txt          # Background
│   └── future.txt             # Future aspirations
├── assets/                    # Static assets
│   └── profile.PNG            # Profile image
├── framer-widget/             # Frontend widget
│   ├── ChatWidget-Framer.tsx  # Single-file Framer component
│   └── SINGLE-FILE-SETUP.md   # Framer integration guide
├── DEPLOYMENT.md              # Complete deployment guide
└── README.md                  # This file
```

---

## 🚀 Quick Start

### 1. Local Development

```bash
# Clone or navigate to project
cd my_chatbot

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your API keys

# Run locally
python app.py
```

Visit: http://localhost:7860

### 2. Test API

```bash
# Health check
curl http://localhost:7860/api/health

# Send chat message
curl -X POST http://localhost:7860/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hi","history":[]}'
```

### 3. Deploy to Production

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete deployment guide.

**Quick deploy to Render.com:**
1. Push to GitHub
2. Connect to Render.com
3. Set environment variables
4. Deploy!

---

## 🔧 Configuration

### Environment Variables

Required variables (set in `.env` or hosting platform):

```env
# OpenAI API
OPENAI_API_KEY=sk-your-key-here

# Pushover Notifications (optional)
PUSHOVER_TOKEN=your-token
PUSHOVER_USER=your-user-key

# Flask Security
FLASK_SECRET_KEY=generate-random-32-char-hex
FLASK_ENV=production

# CORS (your Framer domain)
ALLOWED_ORIGINS=https://yoursite.framer.app
```

### Personal Information

Update files in `me/` folder with your own information:
- `linkedin.pdf` - Export your LinkedIn profile
- `summary.txt` - Professional summary
- `career.txt` - Career history
- `childhood.txt` - Background
- `future.txt` - Future goals

The AI uses this information to answer questions about you.

---

## 🎨 Frontend Widget

### Framer Integration

1. Open `framer-widget/ChatWidget-Framer.tsx`
2. Copy entire file
3. In Framer: Assets → Code → New Code File
4. Paste and name it "ChatWidget"
5. Drag to canvas
6. Configure API URL in properties

See **[framer-widget/SINGLE-FILE-SETUP.md](framer-widget/SINGLE-FILE-SETUP.md)** for detailed guide.

### Widget Features

- Floating chat button (bottom corner)
- Expandable 400×600px chat window
- Black & white minimalist design
- Mobile responsive (full-screen)
- Smooth animations
- Instrument Sans typography
- Auto-scroll messages
- Typing indicators
- Error handling

---

## 🐳 Docker

### Build and Run Locally

```bash
# Build image
docker build -t ai-chatbot .

# Run container
docker run -p 7860:7860 \
  -e OPENAI_API_KEY=your-key \
  -e PUSHOVER_TOKEN=your-token \
  -e PUSHOVER_USER=your-user \
  -e FLASK_SECRET_KEY=your-secret \
  -e ALLOWED_ORIGINS=* \
  ai-chatbot
```

### Production Deployment

Render.com automatically uses the Dockerfile when you deploy.

---

## 🔒 Security

### Built-in Security Features

✅ **CORS Protection**: Whitelist your domains only
✅ **Secret Key**: Auto-generated if not provided
✅ **Non-root User**: Container runs as appuser (UID 1000)
✅ **No Hardcoded Secrets**: All via environment variables
✅ **HTTPS**: Automatic with Render.com
✅ **Health Checks**: Automatic monitoring

### Best Practices

- Never commit `.env` files
- Use strong, random secret keys
- Rotate API keys periodically
- Monitor logs for suspicious activity
- Set CORS to specific domains in production
- Keep dependencies updated

---

## 📊 API Endpoints

### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Chatbot API",
  "version": "1.0.0"
}
```

### POST `/api/chat`
Send message and get AI response.

**Request:**
```json
{
  "message": "Hello, tell me about yourself",
  "history": []
}
```

**Response:**
```json
{
  "response": "Hi! I'm AI Simon...",
  "history": [...],
  "success": true
}
```

### GET `/api/profile-image`
Get profile avatar image (PNG).

---

## 💰 Cost Breakdown

### Free Components

- ✅ Render.com: 750 hours/month (free tier)
- ✅ GitHub: Unlimited private repos
- ✅ Flask/Python: Open source
- ✅ Framer: Included with any plan

### Paid Components

- **OpenAI GPT-4-mini**: ~$0.15 per 1M tokens (very cheap)
- **Pushover**: $5 one-time per platform (optional)
- **Custom domain**: $10-15/year (optional)

**Estimated monthly cost**: ~$0-5 for personal use

---

## 🚀 Deployment Options

### Recommended: Render.com

✅ Free tier with 750 hours/month
✅ Auto-deploy from GitHub
✅ Automatic HTTPS
✅ Built-in health checks
✅ Environment variables
✅ No credit card required

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for step-by-step guide.

### Alternative Platforms

- **Railway**: $5 free credit/month
- **Fly.io**: Free tier available
- **Heroku**: No longer has free tier
- **DigitalOcean**: $4/month droplet
- **AWS**: Free tier (12 months)

---

## 🧪 Testing

### Manual Testing

```bash
# Start backend
python app.py

# In another terminal
curl http://localhost:7860/api/health
curl -X POST http://localhost:7860/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hi","history":[]}'
```

### Frontend Testing

1. Start backend locally
2. Open Framer project
3. Set widget API URL to `http://localhost:7860`
4. Preview and test chat functionality

---

## 📈 Monitoring

### Logs

**Local:**
```bash
# Terminal shows all requests and errors
python app.py
```

**Production (Render):**
- Dashboard → Your service → Logs tab
- Real-time streaming logs

### Pushover Notifications

Every user message sends notification with:
- Timestamp
- Message content
- Instant mobile/desktop alerts

### Health Checks

Render automatically pings `/api/health` every 30 seconds.
If unhealthy, service automatically restarts.

---

## 🐛 Troubleshooting

### Backend Issues

**Build fails:**
- Check Dockerfile syntax
- Verify all files are committed to Git
- Check Render build logs

**CORS errors:**
- Verify ALLOWED_ORIGINS matches your Framer URL exactly
- Include `https://` protocol
- No trailing slashes

**OpenAI errors:**
- Check API key is valid
- Verify account has credits
- Check usage limits

### Frontend Issues

**Widget doesn't appear:**
- Check it's set to "Fixed" position in Framer
- Verify no JavaScript errors (F12 console)

**No response from chat:**
- Verify API URL is correct
- Check backend is running
- Check CORS configuration

See **[framer-widget/SINGLE-FILE-SETUP.md](framer-widget/SINGLE-FILE-SETUP.md)** for more troubleshooting.

---

## 🔄 Updates & Maintenance

### Update Code

```bash
# Make changes
git add .
git commit -m "Update: description"
git push origin main
```

Render automatically redeploys on push.

### Update Dependencies

```bash
# Update requirements.txt
pip freeze > requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### Update Environment Variables

In Render dashboard:
- Environment tab
- Edit variable
- Save (triggers redeploy)

---

## 📚 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide
- **[framer-widget/SINGLE-FILE-SETUP.md](framer-widget/SINGLE-FILE-SETUP.md)** - Framer widget setup
- **[.env.example](.env.example)** - Environment variables template

---

## 🎯 Tech Stack

**Backend:**
- Python 3.11
- Flask 3.0
- OpenAI GPT-4-mini
- Flask-CORS
- Gunicorn (production server)

**Frontend:**
- React 18
- TypeScript
- Framer Code Components
- Instrument Sans font

**Infrastructure:**
- Docker
- Render.com
- GitHub
- Pushover

---

## ✅ Production Checklist

Before going live:

- [ ] All environment variables set
- [ ] CORS configured for production domain
- [ ] OpenAI credits loaded
- [ ] Pushover configured (optional)
- [ ] Backend deployed and healthy
- [ ] Framer widget connected
- [ ] Tested on desktop
- [ ] Tested on mobile
- [ ] No errors in logs
- [ ] SSL certificate active

---

## 🤝 Customization

### Change AI Personality

Edit files in `me/` folder with your own information.

### Change Widget Appearance

Edit `framer-widget/ChatWidget-Framer.tsx`:
- Colors: Search for `#000000` and `#FFFFFF`
- Sizes: Adjust `width`, `height`, `padding`
- Font: Change `fontFamily` values
- Position: Change default from `bottom-right` to `bottom-left`

### Add Features

Ideas for extensions:
- Rate limiting (Flask-Limiter)
- Database for chat history (PostgreSQL)
- Analytics (Google Analytics)
- Multi-language support
- Voice input/output
- File upload support

---

## 📞 Support

For issues:
1. Check logs (local or Render dashboard)
2. Verify environment variables
3. Test API endpoints directly
4. Check CORS configuration
5. Review documentation

---

## 📄 License

This is your personal project. Keep your API keys secure!

---

## 🎉 Success!

Your AI chatbot is ready for production!

**Created by:** Simon Stenelid
**Powered by:** OpenAI GPT-4-mini
**Deployed with:** Render.com + Docker
**Frontend:** Framer

---

**Happy chatting! 🤖💬**
