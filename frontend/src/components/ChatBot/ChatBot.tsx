import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, MessageCircle, Send, Trash2 } from "lucide-react";
import { sendMessage, clearChatHistory } from "../../backend";
import type { ChatMessage } from "../../backend/types";
import styles from "./ChatBot.module.css";

const SESSION_KEY = "alfa_chat_session_id";

export default function ChatBot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(() => {
    return localStorage.getItem(SESSION_KEY);
  });
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      role: "user",
      content: input.trim(),
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await sendMessage(userMessage.content, sessionId || undefined);

      if (response.session_id !== sessionId) {
        setSessionId(response.session_id);
        localStorage.setItem(SESSION_KEY, response.session_id);
      }

      const botMessage: ChatMessage = {
        role: "assistant",
        content: response.reply,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: ChatMessage = {
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again.",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleClear = async () => {
    if (!sessionId) return;
    try {
      await clearChatHistory(sessionId);
      setMessages([]);
      localStorage.removeItem(SESSION_KEY);
      setSessionId(null);
    } catch (error) {
      console.error("Failed to clear chat:", error);
    }
  };

  return (
    <>
      <motion.button
        className={styles.fab}
        onClick={() => setIsOpen(true)}
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
      >
        <MessageCircle size={24} />
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            className={styles.modal}
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ duration: 0.2 }}
          >
            <div className={styles.header}>
              <div className={styles.headerInfo}>
                <h3>Alfa Assistant</h3>
                <span className={styles.status}>Online</span>
              </div>
              <div className={styles.headerActions}>
                {messages.length > 0 && (
                  <button
                    className={styles.iconBtn}
                    onClick={handleClear}
                    title="Clear chat"
                  >
                    <Trash2 size={18} />
                  </button>
                )}
                <button
                  className={styles.iconBtn}
                  onClick={() => setIsOpen(false)}
                  title="Close"
                >
                  <X size={20} />
                </button>
              </div>
            </div>

            <div className={styles.messages}>
              {messages.length === 0 && (
                <div className={styles.welcome}>
                  <p>Hello! I'm your Alfa Assistant.</p>
                  <p>Ask me anything about our visa and travel services.</p>
                </div>
              )}
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`${styles.message} ${styles[msg.role]}`}
                >
                  <div className={styles.bubble}>
                    {msg.content}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className={`${styles.message} ${styles.assistant}`}>
                  <div className={styles.bubble}>
                    <div className={styles.typing}>
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <div className={styles.inputArea}>
              <textarea
                className={styles.input}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type your message..."
                rows={1}
              />
              <button
                className={styles.sendBtn}
                onClick={handleSend}
                disabled={!input.trim() || isLoading}
              >
                <Send size={20} />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
