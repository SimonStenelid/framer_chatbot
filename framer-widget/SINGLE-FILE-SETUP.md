# Single File Setup Guide - Chat Widget for Framer

This guide shows you how to add the chat widget to Framer using the single combined file.

---

## 📦 File Location

**File**: `ChatWidget-Combined.tsx`

This single file contains everything:
- All components (ChatButton, ChatWindow, MessageList, MessageInput, Message)
- API service layer
- TypeScript types
- Animations and styles
- Framer property controls

**Total**: ~800 lines in one file

---

## 🚀 Quick Setup (5 Steps)

### Step 1: Copy the File

1. Open the file: `ChatWidget-Combined.tsx`
2. **Select all** (Cmd+A / Ctrl+A)
3. **Copy** (Cmd+C / Ctrl+C)

---

### Step 2: Create Code Component in Framer

1. Open your **Framer project**
2. Click **Assets** panel (left sidebar)
3. Click the **+** button
4. Select **Code** → **New Code File**
5. Name it: `ChatWidget`
6. **Paste** the entire file contents (Cmd+V / Ctrl+V)
7. **Save** (Cmd+S / Ctrl+S)

---

### Step 3: Add to Your Canvas

1. Find **ChatWidget** in the Assets panel
2. **Drag it** onto your canvas
3. You'll see the component appear

---

### Step 4: Configure Properties

In the **Properties panel** on the right, you'll see:

#### API URL (Required)
- **For local testing**: `http://localhost:7860`
- **For production**: `https://your-backend.onrender.com`

#### Position (Optional)
- `bottom-right` (default)
- `bottom-left`

#### Initial Message (Optional)
- Default: "Hi! I'm AI Simon..."
- Customize to your greeting

#### Input Placeholder (Optional)
- Default: "Type your message..."
- Customize the input placeholder

---

### Step 5: Set to Fixed Position

**Important**: Make the widget appear on all pages!

1. Select the ChatWidget layer in the canvas
2. In the **Layout** section (right panel)
3. Change **Position** from "Relative" to **"Fixed"**
4. This makes it float on all pages

---

## ✅ That's It!

Your chat widget is now ready. Preview your site to test it!

---

## 🎨 Add the Font (Recommended)

For the best look, add Instrument Sans:

1. Go to **Project Settings** (gear icon)
2. Click **Fonts**
3. Click **+ Add Font**
4. Search for **"Instrument Sans"**
5. Select **Regular (400)** weight
6. Click **Add**

If you skip this, the widget will use system fonts (still looks good!).

---

## 🧪 Testing

### Test Locally First

1. **Start your backend**:
   ```bash
   cd my_chatbot
   source .venv/bin/activate
   python app.py
   ```

2. **In Framer**, set API URL to:
   ```
   http://localhost:7860
   ```

3. **Click Preview** in Framer (top-right)

4. **Test the widget**:
   - Click the chat button
   - Type a message
   - Verify you get a response

### Check Console for Errors

If something isn't working:
1. **Right-click** in preview window
2. Select **Inspect** (or press F12)
3. Go to **Console** tab
4. Look for error messages (red text)

Common errors:
- `Failed to fetch` → Backend not running
- `CORS policy` → CORS not configured
- `404 Not Found` → Wrong API URL

---

## 🌐 Deploy & Go Live

### 1. Deploy Your Backend

See `BACKEND_SETUP.md` for deployment instructions.

**Recommended platforms**:
- Render.com (free tier)
- Railway.app ($5 free credit)
- Fly.io (free tier)

After deployment, you'll get a URL like:
```
https://your-chatbot.onrender.com
```

### 2. Configure CORS

In your deployed backend's environment variables:
```env
ALLOWED_ORIGINS=https://yoursite.framer.app
```

If using multiple domains (www, custom domain):
```env
ALLOWED_ORIGINS=https://yoursite.framer.app,https://www.yoursite.com
```

### 3. Update API URL in Framer

1. Select the ChatWidget component
2. In properties, update **API URL** to your deployed URL:
   ```
   https://your-chatbot.onrender.com
   ```
3. **Publish** your Framer site

### 4. Test Live

Visit your published Framer site and test the chat!

---

## 🎯 Customization

All customization is done by editing the code in Framer.

### Change Colors

Find and replace these hex codes in the code:

```tsx
// Black (user messages, buttons)
"#000000" → "YOUR_PRIMARY_COLOR"

// White (AI messages, backgrounds)
"#FFFFFF" → "YOUR_SECONDARY_COLOR"

// Gray borders
"#E5E5E5" → "YOUR_BORDER_COLOR"
```

### Change Sizes

Find these lines and adjust:

```tsx
// Desktop width (line ~450)
width: "400px"

// Desktop height (line ~451)
maxHeight: "600px"

// Font size (multiple places)
fontSize: "14px"
```

### Change Animations

Find these durations and adjust:

```tsx
// Slide animation (line ~730)
animation: "slideUp 0.3s ease"

// Fade animation (line ~720)
animation: "fadeIn 0.2s ease"

// Button hover (line ~630)
transition: "all 0.2s ease"
```

---

## 🐛 Troubleshooting

### Widget Doesn't Appear

**Check**:
1. Is it set to "Fixed" position? ✓
2. Is it on the canvas? ✓
3. Any errors in console? (F12)

**Fix**: Make sure z-index isn't conflicting with other elements.

### Can't Send Messages

**Check**:
1. Is backend running? Test: `YOUR_API_URL/api/health`
2. Is API URL correct in properties?
3. CORS configured with your Framer domain?

**Fix**: Check browser console for specific error.

### CORS Error

**Error**: "Access to fetch blocked by CORS policy"

**Fix**:
1. Add your Framer domain to backend `.env`:
   ```env
   ALLOWED_ORIGINS=https://yoursite.framer.app
   ```
2. Restart backend
3. Clear browser cache and try again

### Font Looks Different

**Check**: Did you add Instrument Sans in Framer?

**Fix**:
- Go to Project Settings → Fonts
- Add "Instrument Sans" font
- Or edit the code to use a different font

### Mobile View Issues

**Check**: Preview on mobile device or Chrome DevTools device emulation

**Fix**: Widget automatically goes full-screen on mobile (≤768px width)

---

## 📱 Mobile Behavior

| Screen Width | Behavior |
|--------------|----------|
| > 768px | 400×600px floating window in corner |
| ≤ 768px | Full-screen with backdrop overlay |

To change breakpoint, find line ~440:
```tsx
setIsMobile(window.innerWidth <= 768);
```

Change `768` to your preferred breakpoint.

---

## 🔍 What's in the File?

The combined file includes (in order):

1. **Type Definitions** (lines 1-50)
   - Message, ChatResponse, Props, etc.

2. **API Service Class** (lines 52-120)
   - Health check
   - Send message
   - Error handling

3. **Message Component** (lines 122-170)
   - Individual message bubbles
   - User vs AI styling

4. **MessageList Component** (lines 172-250)
   - Scrollable message container
   - Typing indicator
   - Auto-scroll

5. **MessageInput Component** (lines 252-380)
   - Auto-resize textarea
   - Send button
   - Loading states

6. **ChatWindow Component** (lines 382-550)
   - Complete chat interface
   - Header with close button
   - Mobile responsive

7. **ChatButton Component** (lines 552-620)
   - Floating button
   - Hover effects

8. **Main ChatWidget** (lines 622-750)
   - State management
   - API integration
   - Orchestration

9. **Global Styles** (lines 752-780)
   - Animations (fadeIn, bounce, spin, etc.)

10. **Framer Controls** (lines 782-800)
    - Property panel configuration

---

## 💡 Pro Tips

### Preview in Different Devices

In Framer:
1. Click **Preview** (top-right)
2. Click device icon to switch between:
   - Desktop
   - Tablet
   - Mobile

### Test Before Publishing

Always test in preview mode before publishing:
- ✅ Desktop layout
- ✅ Mobile layout
- ✅ Send messages
- ✅ Loading states
- ✅ Error handling

### Monitor Usage

Your backend sends Pushover notifications for every message. Use this to:
- See what users are asking
- Monitor usage patterns
- Identify issues

### Keep It Simple

The default design is intentionally minimal. Resist the urge to add too many features that might distract from your main website content.

---

## 📊 Performance

The widget is optimized:
- **Lazy loaded** (only loads when button is clicked)
- **No external dependencies** (just React)
- **Inline styles** (no CSS file to load)
- **~800 lines** (small bundle size)

---

## ✨ Features Included

✅ Floating chat button (minimized state)
✅ Expandable chat window (maximized state)
✅ Message bubbles (user & AI)
✅ Typing indicator (3 animated dots)
✅ Auto-scroll to latest message
✅ Auto-resize input (up to 3 lines)
✅ Enter to send, Shift+Enter for new line
✅ Loading spinners
✅ Error messages
✅ Mobile responsive (full-screen)
✅ Smooth animations
✅ Hover effects
✅ Keyboard shortcuts
✅ ARIA labels
✅ Health check on mount

---

## 🎉 You're Done!

Your chat widget is now integrated with Framer!

**Next**:
1. Deploy your backend
2. Update API URL in Framer
3. Publish your site
4. Share with the world! 🚀

---

## 📚 Additional Resources

- **API Documentation**: `API_DOCUMENTATION.md`
- **Backend Setup**: `BACKEND_SETUP.md`
- **Component Details**: `README.md`
- **Framer Docs**: https://www.framer.com/developers/

---

**File**: `/Users/simonstenelid/Desktop/Framer Chatbot/my_chatbot/framer-widget/ChatWidget-Combined.tsx`

**Size**: ~800 lines
**Language**: TypeScript + React
**Ready for**: Copy & paste into Framer!
