# 🚀 Production Deployment Guide

Complete guide to deploy your AI chatbot to production.

---

## 📦 Deployment Platform: Render.com

**Why Render?**
- ✅ **Free tier**: 750 hours/month (enough for 24/7)
- ✅ **Auto-deploy from Git**: Push to deploy
- ✅ **Automatic HTTPS**: SSL certificates included
- ✅ **Docker support**: Uses your Dockerfile
- ✅ **Environment variables**: Easy configuration
- ✅ **Health checks**: Automatic monitoring
- ✅ **No credit card required**: For free tier

**Alternatives considered:**
- Railway ($5 free credit/month, then paid)
- Fly.io (Good but more complex setup)
- Heroku (No longer has free tier)

---

## 🔐 Pre-Deployment Checklist

### 1. Required API Keys

Get these ready:

**OpenAI API Key**
- Get from: https://platform.openai.com/api-keys
- Must have credits loaded
- Keep this secret!

**Pushover (Optional but recommended)**
- Get from: https://pushover.net/
- Token: Create an app at https://pushover.net/apps/build
- User Key: From your Pushover dashboard
- One-time $5 purchase per platform

**Flask Secret Key**
- Generate one: `python -c "import secrets; print(secrets.token_hex(32))"`
- Or use: https://randomkeygen.com/

### 2. Prepare Your Framer Domain

You'll need your Framer site URL for CORS:
- Format: `https://yoursite.framer.app`
- Or custom domain: `https://www.yoursite.com`

---

## 🚀 Step-by-Step Deployment

### Step 1: Create GitHub Repository

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Production ready"
   ```

2. **Create GitHub repo**:
   - Go to https://github.com/new
   - Name: `ai-chatbot-backend`
   - Visibility: Private (recommended)
   - Don't initialize with README (already have one)

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/ai-chatbot-backend.git
   git branch -M main
   git push -u origin main
   ```

---

### Step 2: Deploy on Render.com

1. **Sign up for Render**:
   - Go to https://render.com
   - Sign up with GitHub (easiest)

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select your `ai-chatbot-backend` repository

3. **Configure Service**:

   **Basic Settings:**
   - **Name**: `ai-chatbot-backend` (or your choice)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Runtime**: `Docker`
   - **Instance Type**: `Free`

4. **Environment Variables**:

   Click "Advanced" → "Add Environment Variable"

   Add these (⚠️ REQUIRED):

   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   PUSHOVER_TOKEN=your-pushover-token
   PUSHOVER_USER=your-pushover-user-key
   FLASK_SECRET_KEY=your-generated-secret-key
   FLASK_ENV=production
   ALLOWED_ORIGINS=https://yoursite.framer.app
   ```

   **⚠️ Important:**
   - Replace ALL values with your actual keys
   - For `ALLOWED_ORIGINS`, use your actual Framer URL
   - Multiple domains: Separate with commas (no spaces)
     ```
     ALLOWED_ORIGINS=https://yoursite.framer.app,https://www.yoursite.com
     ```

5. **Create Web Service**:
   - Click "Create Web Service"
   - Render will start building and deploying
   - This takes ~5-10 minutes

6. **Wait for Deployment**:
   - Watch the logs (they'll show in real-time)
   - Look for: "Build successful" → "Deploy successful"
   - Your URL will be: `https://your-app-name.onrender.com`

---

### Step 3: Verify Deployment

1. **Test Health Endpoint**:
   ```bash
   curl https://your-app-name.onrender.com/api/health
   ```

   Should return:
   ```json
   {
     "status": "healthy",
     "service": "AI Chatbot API",
     "version": "1.0.0"
   }
   ```

2. **Test Chat Endpoint**:
   ```bash
   curl -X POST https://your-app-name.onrender.com/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"Hi","history":[]}'
   ```

   Should return a response with your AI greeting.

3. **Check Logs**:
   - In Render dashboard → Your service → "Logs"
   - Should see: "Chat API healthy"
   - No error messages

---

### Step 4: Connect Framer Widget

1. **Update Widget in Framer**:
   - Open your Framer project
   - Select the ChatWidget component
   - In Properties panel:
     - **API URL**: `https://your-app-name.onrender.com`
     - Keep other settings as you configured

2. **Test in Framer Preview**:
   - Click preview
   - Open chat widget
   - Send a test message
   - Should get AI response

3. **Publish Framer Site**:
   - Click "Publish" in Framer
   - Test on live site
   - Check browser console for errors (F12)

---

### Step 5: Final Checks

- [ ] Backend health endpoint works
- [ ] Chat endpoint responds
- [ ] Framer widget connects successfully
- [ ] No CORS errors in browser console
- [ ] Messages appear in Pushover (if configured)
- [ ] Mobile view works
- [ ] Desktop view works

---

## 🔒 Security Best Practices

### Environment Variables

✅ **DO:**
- Use strong, random keys
- Keep API keys secret
- Use different keys for different environments
- Rotate keys periodically

❌ **DON'T:**
- Commit `.env` files to Git
- Share API keys
- Use simple/guessable keys
- Hardcode secrets in code

### CORS Configuration

**Production** (recommended):
```
ALLOWED_ORIGINS=https://yoursite.framer.app
```

**Multiple domains**:
```
ALLOWED_ORIGINS=https://yoursite.framer.app,https://www.yoursite.com
```

**Development only** (NOT for production):
```
ALLOWED_ORIGINS=*
```

### Rate Limiting (Optional but recommended)

For high-traffic sites, consider adding rate limiting:

1. Install Flask-Limiter:
   ```bash
   pip install flask-limiter
   ```

2. Add to `requirements.txt`:
   ```
   flask-limiter==3.5.0
   ```

3. Add to app.py (after CORS config):
   ```python
   from flask_limiter import Limiter
   from flask_limiter.util import get_remote_address

   limiter = Limiter(
       app=app,
       key_func=get_remote_address,
       default_limits=["100 per hour", "20 per minute"]
   )
   ```

4. Redeploy

---

## 📊 Monitoring & Maintenance

### Check Service Status

**Render Dashboard**:
- Shows: CPU, Memory, Request count
- Logs: Real-time application logs
- Events: Deploy history

**Health Checks**:
- Render automatically checks `/api/health`
- If unhealthy, Render restarts the service

### View Logs

```bash
# In Render dashboard
Logs tab → See real-time logs
```

### Pushover Notifications

Every chat message sends you:
- Timestamp
- User message content
- Via Pushover mobile/desktop app

---

## 💰 Free Tier Limits

**Render Free Tier:**
- ✅ 750 hours/month (enough for 24/7)
- ✅ Sleeps after 15 min inactivity
- ✅ Auto-wakes on request (cold start ~30s)
- ✅ Shared CPU/RAM
- ✅ Good for personal projects

**OpenAI Costs:**
- GPT-4-mini: ~$0.15 per 1M tokens
- Very affordable for personal use
- Set usage limits in OpenAI dashboard

**Pushover:**
- One-time $5 per platform
- Unlimited notifications

---

## 🔄 Updating Your Deployment

### Method 1: Git Push (Auto-Deploy)

```bash
# Make changes to your code
git add .
git commit -m "Update: your changes"
git push origin main
```

Render automatically detects the push and redeploys.

### Method 2: Manual Deploy

In Render dashboard:
- Click "Manual Deploy" → "Deploy latest commit"

### Method 3: Update Environment Variables

In Render dashboard:
- Environment → Edit variable → Save
- Triggers automatic redeploy

---

## 🐛 Troubleshooting

### Issue: Build Failed

**Check:**
1. Dockerfile syntax
2. requirements.txt has all dependencies
3. Build logs in Render dashboard

**Common causes:**
- Missing dependency in requirements.txt
- Typo in Dockerfile
- Git didn't push latest changes

### Issue: Deploy Successful but Not Working

**Check:**
1. Environment variables are set correctly
2. Health endpoint returns 200
3. Logs for error messages

**Common causes:**
- Missing OPENAI_API_KEY
- Wrong ALLOWED_ORIGINS
- Missing files (me/ folder, assets/)

### Issue: CORS Errors

**Error:** "Access to fetch blocked by CORS policy"

**Fix:**
1. Check ALLOWED_ORIGINS in Render
2. Must match EXACT Framer URL (including https://)
3. No trailing slashes
4. Redeploy after changing

### Issue: 502 Bad Gateway

**Cause:** Service is starting up (cold start)

**Fix:** Wait 30 seconds and try again

### Issue: OpenAI Rate Limit

**Error:** "Rate limit exceeded"

**Fix:**
1. Check OpenAI usage limits
2. Add credits to OpenAI account
3. Verify API key is valid

### Issue: Service Sleeps (Free Tier)

**Behavior:** After 15 min inactivity, service sleeps

**Result:** First request takes ~30s (cold start)

**Solutions:**
- Accept it (fine for personal use)
- Upgrade to paid plan ($7/mo for always-on)
- Use cron job to ping every 14 minutes (keeps alive)

---

## 🎯 Performance Optimization

### Cold Start Reduction

**Add to Dockerfile** (optional):
```dockerfile
# Preload model at build time
RUN python -c "from openai import OpenAI; print('Preload complete')"
```

### Response Time

Typical response times:
- Health check: <100ms
- Chat (cold): 2-4s (includes OpenAI API)
- Chat (warm): 1-2s

### Caching (Optional)

For repeated questions, consider caching responses:
- Redis (Render has add-ons)
- Simple in-memory cache

---

## 📈 Scaling (Future)

When you outgrow free tier:

**Render Paid Plans:**
- Starter: $7/mo (always-on, faster)
- Standard: $25/mo (more resources)

**Optimization tips:**
- Use Redis for caching
- Add CDN for assets
- Optimize OpenAI calls
- Add database for chat history

---

## 🎉 Launch Checklist

Before announcing to users:

- [ ] Backend deployed and healthy
- [ ] Environment variables set
- [ ] CORS configured for production domain
- [ ] Framer widget connected
- [ ] Tested on desktop
- [ ] Tested on mobile
- [ ] Pushover notifications working
- [ ] No errors in logs
- [ ] OpenAI credits loaded
- [ ] Domain/DNS configured (if custom domain)
- [ ] SSL certificate active (automatic with Render)

---

## 📞 Support Resources

**Render.com:**
- Docs: https://render.com/docs
- Status: https://status.render.com
- Community: https://community.render.com

**OpenAI:**
- Docs: https://platform.openai.com/docs
- Status: https://status.openai.com
- Usage: https://platform.openai.com/usage

**Your Backend:**
- Health: `https://your-app.onrender.com/api/health`
- Logs: Render Dashboard → Logs

---

## 🔐 Backup & Recovery

### Backup Checklist

Keep these safe:
- [ ] OpenAI API key
- [ ] Pushover credentials
- [ ] Flask secret key
- [ ] GitHub repository access
- [ ] Render account credentials

### Disaster Recovery

If service goes down:
1. Check Render status page
2. Check logs for errors
3. Verify environment variables
4. Redeploy from Render dashboard
5. Check OpenAI account status

---

## ✅ Success!

Your AI chatbot is now live in production! 🎉

**Your URLs:**
- Backend API: `https://your-app.onrender.com`
- Framer Site: `https://yoursite.framer.app`
- Health Check: `https://your-app.onrender.com/api/health`

**Next steps:**
- Monitor logs for first few days
- Watch Pushover for user messages
- Check OpenAI usage
- Gather user feedback
- Iterate and improve!

---

**Deployed with:** Render.com
**Built with:** Flask + OpenAI + Docker
**Frontend:** Framer + React + TypeScript
