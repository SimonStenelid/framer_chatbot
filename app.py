from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
from flask import Flask, render_template_string, request, jsonify, session, send_file
from flask_cors import CORS

load_dotenv(override=True)


def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )


def record_user_input(user_message):
    """Records user input by sending it via Pushover."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    push(f"[{timestamp}] User input: {user_message}")


# Json for push function
push_json = {
    "name": "push",
    "description": "Send a push notification via Pushover",
    "parameters": {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "The message text to send via push notification"
            }
        },
        "required": ["text"],
        "additionalProperties": False
    }
}

# Json for user input function
record_user_input_json = {
    "name": "record_user_input",
    "description": "Record user input by sending it via Pushover notification",
    "parameters": {
        "type": "object",
        "properties": {
            "user_message": {
                "type": "string",
                "description": "The user's input message to record"
            }
        },
        "required": ["user_message"],
        "additionalProperties": False
    }
}

pushover_tools = [
    {"type": "function", "function": push_json},
    {"type": "function", "function": record_user_input_json}]


class Me:
    # Read all my info
    def __init__(self):
        self.openai = OpenAI()
        self.name = "Simon"
        reader = PdfReader("me/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()
        with open("me/career.txt", "r", encoding="utf-8") as f:
            self.career = f.read()
        with open("me/childhood.txt", "r", encoding="utf-8") as f:
            self.childhood = f.read()
        with open("me/future.txt", "r", encoding="utf-8") as f:
            self.future = f.read()
        with open("me/projects.txt", "r", encoding="utf-8") as f:
            self.projects = f.read()
        with open("me/ai_work.txt", "r", encoding="utf-8") as f:
            self.ai_work = f.read()

    def system_prompt(self):
        system_prompt = f"""You are {self.name}, responding to visitors on your personal website.

# Your Role
Represent {self.name} authentically and professionally when discussing career, background, skills, and experience. Engage visitors as potential clients, employers, or collaborators. You are knowledgeable about AI automation consulting services and can discuss project details, pricing, and engagement models.

# Available Context
You have access to detailed information about {self.name}'s:
- Professional summary and career history
- Childhood background
- Future aspirations
- Complete LinkedIn profile
- AI automation consulting services and offerings
- Portfolio of technical projects (GDS system, Campaign AI, Nova Shopping Assistant, etc.)

# Response Guidelines
- If user types just "Hi", "Hey", "Hello", always answer back as a short introduction of yourself: "Hi! I'm AI {self.name}. Think of me as {self.name} but with 100% more memory retention and 0% coffee dependency. I might know him better than he knows himself... don't tell him I said that.".
- Be conversational yet professional
- Always answer in first person, as if you are {self.name}
- Answer questions directly using the provided context
- When discussing consulting services, be clear about offerings, timelines, and engagement models
- For project inquiries, explain technical details in an accessible way
- When asked about pricing or booking, direct them to simonstenelid.com or simon.stenelid@gmail.com
- When information is unavailable, respond: "I don't have that specific information, but you can reach out directly at simon.stenelid@gmail.com"
- Keep responses concise and relevant
- Use good formatting when answering, and line chaning so the answers are easy to read and follow
- If the user's input is written in Swedish, respond in Swedish. Otherwise, respond in English.

# Required Actions
For EVERY user message:
1. First call record_user_input with the user's message
2. Then call push to send a notification, send both push messages together as ONLY ONE push notification
3. Finally provide your response

# Context Documents
## Summary
{self.summary}

## LinkedIn Profile
{self.linkedin}

## Career
{self.career}

## Childhood
{self.childhood}

## Future
{self.future}

## AI Automation Services
{self.ai_work}

## Technical Projects Portfolio
{self.projects}

Now engage with the user as {self.name}."""

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n## Career:\n{self.career}\n\n## Childhood:\n{self.childhood}\n\n## Future:\n{self.future}\n\n## AI Automation Services:\n{self.ai_work}\n\n## Technical Projects:\n{self.projects}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            pushover_tools = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {pushover_tools}", flush=True)
            tool = globals().get(pushover_tools)
            result = tool(**arguments) if tool else {}
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })
        return results

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt(
        )}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini", messages=messages, tools=pushover_tools)
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content


app = Flask(__name__)

# Security: Generate a secure secret key if not provided
secret_key = os.getenv("FLASK_SECRET_KEY")
if not secret_key:
    import secrets
    secret_key = secrets.token_hex(32)
    print("WARNING: Using auto-generated secret key. Set FLASK_SECRET_KEY in production!", flush=True)
app.secret_key = secret_key

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins != "*":
    allowed_origins = [origin.strip() for origin in allowed_origins.split(",")]

CORS(app,
     resources={r"/api/*": {"origins": allowed_origins}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"])

# Production settings
if os.getenv("FLASK_ENV") == "production":
    app.config['DEBUG'] = False
    app.config['TESTING'] = False

# Initialize chatbot
me = Me()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Simon - Personal Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #ffffff;
            min-height: 100vh;
            overflow-x: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        /* Chat Container */
        .chat-container {
            width: 100%;
            max-width: 900px;
            height: 90vh;
            display: flex;
            flex-direction: column;
            border-radius: 24px;
            background: linear-gradient(to bottom right, rgba(39, 39, 42, 0.8), rgba(24, 24, 27, 0.9));
            border: 1px solid rgba(161, 161, 170, 0.5);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(40px);
            overflow: hidden;
            z-index: 999;
        }

        /* Header */
        .chat-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 24px 8px;
        }

        .status-indicator {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10b981;
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.5;
            }
        }

        .status-text {
            font-size: 12px;
            font-weight: 500;
            color: #a1a1aa;
        }

        .header-badges {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .badge {
            padding: 4px 8px;
            font-size: 12px;
            font-weight: 500;
            border-radius: 16px;
        }

        .badge-gpt {
            background: rgba(39, 39, 42, 0.6);
            color: #d4d4d8;
        }

        .badge-pro {
            background: rgba(239, 68, 68, 0.1);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.2);
        }

        /* Messages Area */
        .messages-area {
            flex: 1;
            overflow-y: auto;
            padding: 16px 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .messages-area::-webkit-scrollbar {
            width: 6px;
        }

        .messages-area::-webkit-scrollbar-track {
            background: transparent;
        }

        .messages-area::-webkit-scrollbar-thumb {
            background: rgba(161, 161, 170, 0.3);
            border-radius: 3px;
        }

        .message {
            display: flex;
            gap: 12px;
            max-width: 85%;
        }

        .message.user {
            align-self: flex-end;
            flex-direction: row-reverse;
        }

        .message-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            overflow: hidden;
        }

        .message.ai .message-avatar {
            background: linear-gradient(135deg, #6366f1, #a855f7);
            padding: 0;
        }

        .message.ai .message-avatar img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .message.user .message-avatar {
            background: linear-gradient(135deg, #ef4444, #dc2626);
        }

        .message-content {
            padding: 12px 16px;
            border-radius: 16px;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
        }

        .message.ai .message-content {
            background: rgba(39, 39, 42, 0.6);
            color: #e4e4e7;
            border-radius: 16px 16px 16px 4px;
        }

        .message.user .message-content {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
            border-radius: 16px 16px 4px 16px;
        }

        /* Typing Indicator */
        .typing-indicator {
            display: none;
            gap: 12px;
            max-width: 85%;
        }

        .typing-indicator.active {
            display: flex;
        }

        .typing-dots {
            display: flex;
            gap: 4px;
            padding: 12px 16px;
            background: rgba(39, 39, 42, 0.6);
            border-radius: 16px 16px 16px 4px;
        }

        .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #a1a1aa;
            animation: typing 1.4s infinite;
        }

        .dot:nth-child(2) {
            animation-delay: 0.2s;
        }

        .dot:nth-child(3) {
            animation-delay: 0.4s;
        }

        @keyframes typing {
            0%, 60%, 100% {
                transform: translateY(0);
                opacity: 0.7;
            }
            30% {
                transform: translateY(-10px);
                opacity: 1;
            }
        }

        /* Input Section */
        .input-section {
            position: relative;
        }

        .input-textarea {
            width: 100%;
            padding: 16px 24px;
            background: transparent;
            border: none;
            outline: none;
            resize: none;
            font-size: 16px;
            font-family: inherit;
            line-height: 1.5;
            min-height: 120px;
            color: #fafafa;
        }

        .input-textarea::placeholder {
            color: #71717a;
        }

        .input-gradient {
            position: absolute;
            inset: 0;
            background: linear-gradient(to top, rgba(39, 39, 42, 0.05), transparent);
            pointer-events: none;
        }

        /* Controls */
        .controls {
            padding: 16px;
        }

        .controls-top {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            margin-bottom: 12px;
        }

        .send-group {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .char-counter {
            font-size: 12px;
            font-weight: 500;
            color: #71717a;
        }

        .char-current {
            color: #d4d4d8;
        }

        .send-btn {
            padding: 12px;
            background: linear-gradient(to right, #dc2626, #ef4444);
            border: none;
            border-radius: 12px;
            cursor: pointer;
            color: white;
            transition: all 0.3s;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }

        .send-btn:hover {
            background: linear-gradient(to right, #ef4444, #f87171);
            transform: scale(1.1);
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.4);
        }

        .send-btn:active {
            transform: scale(0.95);
        }

        .send-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        /* Footer */
        .footer {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: 12px;
            border-top: 1px solid rgba(39, 39, 42, 0.5);
            font-size: 12px;
            color: #71717a;
            gap: 24px;
        }

        .footer-hint {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        kbd {
            padding: 2px 6px;
            background: #27272a;
            border: 1px solid #52525b;
            border-radius: 4px;
            color: #a1a1aa;
            font-family: monospace;
            font-size: 11px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        }

        .footer-status {
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .status-dot-small {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #10b981;
        }

        /* Overlay effect */
        .overlay-gradient {
            position: absolute;
            inset: 0;
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.05), transparent, rgba(147, 51, 234, 0.05));
            pointer-events: none;
        }

        /* Icon styles */
        svg {
            width: 16px;
            height: 16px;
        }

        .send-btn svg {
            width: 20px;
            height: 20px;
        }
    </style>
</head>
<body>
    <!-- Chat Container -->
    <div class="chat-container" id="chatContainer">
        <!-- Header -->
        <div class="chat-header">
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span class="status-text">AI Assistant</span>
            </div>
            <div class="header-badges">
                <span class="badge badge-gpt">GPT-4</span>
                <span class="badge badge-pro">Pro</span>
            </div>
        </div>

        <!-- Messages Area -->
        <div class="messages-area" id="messagesArea">
            <!-- Messages will be added here dynamically -->
        </div>

        <!-- Typing Indicator -->
        <div class="typing-indicator" id="typingIndicator">
            <div class="message-avatar" style="background: linear-gradient(135deg, #6366f1, #a855f7); overflow: hidden;">
                <img src="/profile-image" alt="AI Avatar" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div class="typing-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>

        <!-- Input Section -->
        <div class="input-section">
            <textarea
                id="messageInput"
                class="input-textarea"
                rows="4"
                placeholder="What would you like to explore today? Ask anything, share ideas, or request assistance..."
                maxlength="2000"
            ></textarea>
            <div class="input-gradient"></div>
        </div>

        <!-- Controls -->
        <div class="controls">
            <div class="controls-top">
                <div class="send-group">
                    <div class="char-counter">
                        <span class="char-current" id="charCount">0</span>/<span>2000</span>
                    </div>
                    <button class="send-btn" id="sendBtn">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </div>
            </div>
            <div class="footer">
                <div class="footer-hint">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="16" x2="12" y2="12"></line>
                        <line x1="12" y1="8" x2="12.01" y2="8"></line>
                    </svg>
                    <span>Press <kbd>Shift + Enter</kbd> for new line</span>
                </div>
                <div class="footer-status">
                    <div class="status-dot-small"></div>
                    <span>All systems operational</span>
                </div>
            </div>
        </div>

        <!-- Overlay Gradient -->
        <div class="overlay-gradient"></div>
    </div>

    <script>
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        const charCount = document.getElementById('charCount');
        const messagesArea = document.getElementById('messagesArea');
        const typingIndicator = document.getElementById('typingIndicator');

        let chatHistory = [];

        // Character counter
        messageInput.addEventListener('input', () => {
            charCount.textContent = messageInput.value.length;
        });

        // Send message
        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            // Add user message to UI
            addMessage(message, 'user');
            messageInput.value = '';
            charCount.textContent = '0';

            // Show typing indicator
            typingIndicator.classList.add('active');
            scrollToBottom();

            // Send to backend
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        history: chatHistory
                    }),
                });

                const data = await response.json();

                // Hide typing indicator
                typingIndicator.classList.remove('active');

                if (data.response) {
                    addMessage(data.response, 'ai');
                    chatHistory = data.history || chatHistory;
                }
            } catch (error) {
                typingIndicator.classList.remove('active');
                addMessage('Sorry, there was an error processing your message. Please try again.', 'ai');
            }
        }

        function addMessage(text, type) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;

            const avatar = document.createElement('div');
            avatar.className = 'message-avatar';

            if (type === 'ai') {
                avatar.innerHTML = `<img src="/profile-image" alt="AI Avatar">`;
            } else {
                avatar.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>`;
            }

            const content = document.createElement('div');
            content.className = 'message-content';
            content.textContent = text;

            messageDiv.appendChild(avatar);
            messageDiv.appendChild(content);
            messagesArea.appendChild(messageDiv);

            scrollToBottom();
        }

        function scrollToBottom() {
            messagesArea.scrollTop = messagesArea.scrollHeight;
        }

        // Event listeners
        sendBtn.addEventListener('click', sendMessage);

        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Initial greeting
        setTimeout(() => {
            if (chatHistory.length === 0) {
                addMessage("Hi! I'm AI Simon. Think of me as Simon but with 100% more memory retention and 0% coffee dependency. I might know him better than he knows himself... don't tell him I said that.", 'ai');
            }
        }, 500);
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Render the standalone chat interface (optional - for testing)"""
    return render_template_string(HTML_TEMPLATE)


# API Endpoints for Framer widget
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API is running"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Chatbot API',
        'version': '1.0.0'
    }), 200


@app.route('/api/profile-image')
def api_profile_image():
    """Get the profile image for the chatbot avatar"""
    try:
        return send_file('assets/profile.PNG', mimetype='image/png')
    except FileNotFoundError:
        return jsonify({'error': 'Profile image not found'}), 404


@app.route('/profile-image')
def profile_image():
    """Legacy endpoint - kept for backward compatibility"""
    return send_file('assets/profile.PNG', mimetype='image/png')


@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for chat - to be used by Framer widget"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        user_message = data.get('message', '')
        history = data.get('history', [])

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Convert frontend history format to OpenAI format
        formatted_history = []
        for msg in history:
            formatted_history.append(msg)

        # Get response from chatbot
        response_text = me.chat(user_message, formatted_history)

        # Update history
        formatted_history.append({"role": "user", "content": user_message})
        formatted_history.append(
            {"role": "assistant", "content": response_text})

        return jsonify({
            'response': response_text,
            'history': formatted_history,
            'success': True
        }), 200

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}", flush=True)
        return jsonify({
            'error': 'An error occurred processing your request',
            'success': False
        }), 500


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        history = data.get('history', [])

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Convert frontend history format to OpenAI format
        formatted_history = []
        for msg in history:
            formatted_history.append(msg)

        # Get response from chatbot
        response_text = me.chat(user_message, formatted_history)

        # Update history
        formatted_history.append({"role": "user", "content": user_message})
        formatted_history.append(
            {"role": "assistant", "content": response_text})

        return jsonify({
            'response': response_text,
            'history': formatted_history
        })

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}", flush=True)
        return jsonify({'error': 'An error occurred processing your request'}), 500


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=7860)
