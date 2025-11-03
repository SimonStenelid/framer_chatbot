import React, { useState, useEffect, useRef, KeyboardEvent } from "react";
import type { ComponentType } from "react";

// ============================================================================
// TYPES
// ============================================================================

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface ChatResponse {
  response: string;
  history: Message[];
  success: boolean;
  error?: string;
}

interface ChatWidgetProps {
  apiUrl?: string;
  position?: "bottom-right" | "bottom-left";
  initialMessage?: string;
  placeholder?: string;
}

// ============================================================================
// API SERVICE
// ============================================================================

class ChatAPI {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl ? baseUrl.replace(/\/$/, "") : "";
  }

  async healthCheck() {
    try {
      const response = await fetch(`${this.baseUrl}/api/health`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      if (!response.ok) throw new Error(`Health check failed: ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error("Health check error:", error);
      throw new Error("Unable to connect to chat service");
    }
  }

  async sendMessage(message: string, history: Message[] = []): Promise<ChatResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, history }),
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `Request failed: ${response.status}`);
      }
      const data: ChatResponse = await response.json();
      if (!data.success) throw new Error(data.error || "Request failed");
      return data;
    } catch (error) {
      throw error instanceof Error ? error : new Error("Failed to send message");
    }
  }
}

// ============================================================================
// COMPONENTS
// ============================================================================

const Message: React.FC<{ message: Message }> = ({ message }) => {
  const isUser = message.role === "user";
  return (
    <div style={{ display: "flex", justifyContent: isUser ? "flex-end" : "flex-start", marginBottom: "12px", animation: "fadeIn 0.3s ease" }}>
      <div style={{
        maxWidth: "85%", padding: "12px 16px", borderRadius: "16px",
        backgroundColor: isUser ? "#000000" : "#FFFFFF",
        color: isUser ? "#FFFFFF" : "#000000",
        border: isUser ? "none" : "1px solid #E5E5E5",
        fontFamily: '"Instrument Sans", -apple-system, BlinkMacSystemFont, sans-serif',
        fontSize: "14px", fontWeight: 400, letterSpacing: "-0.03em", lineHeight: "1.4",
        whiteSpace: "pre-wrap", wordBreak: "break-word",
      }}>
        {message.content}
      </div>
    </div>
  );
};

const MessageList: React.FC<{ messages: Message[]; isLoading: boolean }> = ({ messages, isLoading }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div
      ref={containerRef}
      style={{
        flex: 1,
        overflowY: "auto",
        overflowX: "hidden",
        padding: "20px",
        backgroundColor: "#FAFAFA",
        display: "flex",
        flexDirection: "column",
        WebkitOverflowScrolling: "touch",
        scrollBehavior: "smooth"
      }}
    >
      {messages.length === 0 && !isLoading && (
        <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center", color: "#A0A0A0", fontFamily: '"Instrument Sans", sans-serif', fontSize: "14px", textAlign: "center" }}>
          Start a conversation...
        </div>
      )}
      {messages.map((message, index) => <Message key={index} message={message} />)}
      {isLoading && (
        <div style={{ display: "flex", justifyContent: "flex-start", marginBottom: "12px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "6px", padding: "12px 16px", borderRadius: "16px", backgroundColor: "#FFFFFF", border: "1px solid #E5E5E5" }}>
            {[0, 0.2, 0.4].map((delay, i) => (
              <div key={i} style={{ width: "8px", height: "8px", borderRadius: "50%", backgroundColor: "#000000", animation: "bounce 1.4s infinite", animationDelay: `${delay}s` }} />
            ))}
          </div>
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

const MessageInput: React.FC<{ onSend: (message: string) => void; isLoading: boolean; placeholder: string }> = ({ onSend, isLoading, placeholder }) => {
  const [value, setValue] = useState("");
  const [isFocused, setIsFocused] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    const trimmedValue = value.trim();
    if (trimmedValue && !isLoading) {
      onSend(trimmedValue);
      setValue("");
      if (textareaRef.current) textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setValue(e.target.value);
    const textarea = e.target;
    textarea.style.height = "auto";
    textarea.style.height = `${Math.min(textarea.scrollHeight, 100)}px`;
  };

  return (
    <div style={{ display: "flex", alignItems: "flex-end", gap: "8px", padding: "16px", borderTop: "1px solid #E5E5E5", backgroundColor: "#FFFFFF" }}>
      <textarea
        ref={textareaRef} value={value} onChange={handleChange} onKeyDown={handleKeyDown}
        onFocus={() => setIsFocused(true)} onBlur={() => setIsFocused(false)}
        placeholder={placeholder} disabled={isLoading} rows={1}
        style={{
          flex: 1, resize: "none", border: `1px solid ${isFocused ? "#000000" : "#E5E5E5"}`,
          borderRadius: "12px", padding: "10px 14px",
          fontFamily: '"Instrument Sans", sans-serif', fontSize: "14px",
          color: "#000000", backgroundColor: "#FFFFFF", outline: "none",
          transition: "border-color 0.2s ease", minHeight: "40px", maxHeight: "100px", overflow: "auto",
        }}
      />
      <button onClick={handleSend} disabled={!value.trim() || isLoading}
        style={{
          width: "40px", height: "40px", borderRadius: "12px",
          backgroundColor: value.trim() && !isLoading ? "#000000" : "#E5E5E5",
          color: value.trim() && !isLoading ? "#FFFFFF" : "#A0A0A0",
          border: "none", cursor: value.trim() && !isLoading ? "pointer" : "not-allowed",
          display: "flex", alignItems: "center", justifyContent: "center", transition: "all 0.2s ease",
        }}
      >
        {isLoading ? (
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ animation: "spin 1s linear infinite" }}>
            <circle cx="12" cy="12" r="10" opacity="0.25" />
            <path d="M12 2a10 10 0 0 1 10 10" />
          </svg>
        ) : (
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
        )}
      </button>
    </div>
  );
};

const ChatWindow: React.FC<{
  isOpen: boolean; onClose: () => void; messages: Message[];
  onSendMessage: (message: string) => void; isLoading: boolean;
  error: string | null; placeholder: string; position: string;
}> = ({ isOpen, onClose, messages, onSendMessage, isLoading, error, placeholder, position }) => {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth <= 768);
    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  if (!isOpen) return null;

  const positionStyles = position === "bottom-right" ? { bottom: "24px", right: "24px" } : { bottom: "24px", left: "24px" };
  const mobileStyles = isMobile ? { top: 0, left: 0, right: 0, bottom: 0, width: "100%", height: "100%", borderRadius: "0", maxHeight: "100vh" }
    : { ...positionStyles, width: "400px", maxHeight: "600px", borderRadius: "16px" };

  return (
    <>
      {isMobile && <div onClick={onClose} style={{ position: "fixed", top: 0, left: 0, right: 0, bottom: 0, backgroundColor: "rgba(0, 0, 0, 0.5)", zIndex: 9998, animation: "fadeIn 0.2s ease" }} />}
      <div style={{ position: "fixed", ...mobileStyles, zIndex: 9999, backgroundColor: "#FFFFFF", boxShadow: isMobile ? "none" : "0 8px 24px rgba(0, 0, 0, 0.15)", display: "flex", flexDirection: "column", animation: isMobile ? "slideUpMobile 0.3s ease" : "slideUp 0.3s ease" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "20px", borderBottom: "1px solid #E5E5E5" }}>
          <h3 style={{ margin: 0, fontFamily: '"Instrument Sans", sans-serif', fontSize: "16px", fontWeight: 400, color: "#000000" }}>Chat with Simon</h3>
          {!isMobile && (
            <button onClick={onClose} style={{ width: "32px", height: "32px", borderRadius: "8px", backgroundColor: "transparent", border: "none", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#000000" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          )}
        </div>
        {error && <div style={{ padding: "12px 20px", backgroundColor: "#FEF2F2", borderBottom: "1px solid #FEE2E2", color: "#991B1B", fontSize: "13px" }}>{error}</div>}
        <MessageList messages={messages} isLoading={isLoading} />
        <MessageInput onSend={onSendMessage} isLoading={isLoading} placeholder={placeholder} />
        {isMobile && (
          <div style={{ padding: "16px", borderTop: "1px solid #E5E5E5", backgroundColor: "#FFFFFF" }}>
            <button onClick={onClose} style={{ width: "100%", padding: "12px", borderRadius: "12px", backgroundColor: "#F5F5F5", color: "#000000", border: "none", cursor: "pointer", fontFamily: '"Instrument Sans", sans-serif', fontSize: "14px", fontWeight: 400, display: "flex", alignItems: "center", justifyContent: "center", gap: "8px", transition: "background-color 0.2s ease" }}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#000000" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
              <span>Close Chat</span>
            </button>
          </div>
        )}
      </div>
    </>
  );
};

const ChatButton: React.FC<{ onClick: () => void; position: string }> = ({ onClick, position }) => {
  const positionStyles = position === "bottom-right" ? { bottom: "24px", right: "24px" } : { bottom: "24px", left: "24px" };
  return (
    <button onClick={onClick}
      style={{
        position: "fixed", ...positionStyles, zIndex: 9998, backgroundColor: "#000000", color: "#FFFFFF",
        border: "none", borderRadius: "999px", padding: "14px 24px",
        fontFamily: '"Instrument Sans", sans-serif', fontSize: "14px", cursor: "pointer",
        display: "flex", alignItems: "center", gap: "8px",
        boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)", transition: "all 0.2s ease",
      }}
    >
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
      </svg>
      <span>Chat</span>
    </button>
  );
};

// ============================================================================
// MAIN COMPONENT
// ============================================================================

const ChatWidget: ComponentType<ChatWidgetProps> = ({
  apiUrl = "http://localhost:7860",
  position = "bottom-right",
  initialMessage = "Hi! I'm AI Simon. Think of me as Simon but with 100% more memory retention and 0% coffee dependency.",
  placeholder = "Type your message..."
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [api] = useState(() => new ChatAPI(apiUrl || "http://localhost:7860"));

  useEffect(() => {
    if (initialMessage && messages.length === 0) {
      setMessages([{ role: "assistant", content: initialMessage }]);
    }
  }, [initialMessage, messages.length]);

  useEffect(() => {
    api.healthCheck().then(() => console.log("Chat API healthy")).catch(err => console.error("Health check failed:", err));
  }, [api]);

  const handleSendMessage = async (message: string) => {
    const userMessage: Message = { role: "user", content: message };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const historyForAPI = messages.filter(msg => msg.content !== initialMessage);
      const response = await api.sendMessage(message, historyForAPI);
      setMessages(prev => [...prev, { role: "assistant", content: response.response }]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message");
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400&display=swap" rel="stylesheet" />
      <style>{`
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes bounce { 0%, 60%, 100% { transform: translateY(0); opacity: 1; } 30% { transform: translateY(-10px); opacity: 0.7; } }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px) scale(0.95); } to { opacity: 1; transform: translateY(0) scale(1); } }
        @keyframes slideUpMobile { from { opacity: 0; transform: translateY(100%); } to { opacity: 1; transform: translateY(0); } }

        /* Custom scrollbar styles */
        *::-webkit-scrollbar {
          width: 8px;
        }
        *::-webkit-scrollbar-track {
          background: transparent;
        }
        *::-webkit-scrollbar-thumb {
          background: #D1D1D1;
          border-radius: 4px;
        }
        *::-webkit-scrollbar-thumb:hover {
          background: #A0A0A0;
        }
      `}</style>
      {!isOpen && <ChatButton onClick={() => setIsOpen(true)} position={position} />}
      <ChatWindow isOpen={isOpen} onClose={() => { setIsOpen(false); setError(null); }} messages={messages} onSendMessage={handleSendMessage} isLoading={isLoading} error={error} placeholder={placeholder} position={position} />
    </>
  );
};

// Attach property controls to the component
ChatWidget.propertyControls = {
  apiUrl: {
    type: "string",
    title: "API URL",
    defaultValue: "http://localhost:7860",
    description: "Backend API URL",
  },
  position: {
    type: "enum",
    title: "Position",
    options: ["bottom-right", "bottom-left"],
    defaultValue: "bottom-right",
  },
  initialMessage: {
    type: "string",
    title: "Initial Message",
    defaultValue: "Hi! I'm AI Simon. Think of me as Simon but with 100% more memory retention and 0% coffee dependency.",
    displayTextArea: true,
  },
  placeholder: {
    type: "string",
    title: "Placeholder",
    defaultValue: "Type your message...",
  },
};

export default ChatWidget;
