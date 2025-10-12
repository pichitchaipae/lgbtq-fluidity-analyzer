import React, { useState, useRef, useEffect } from 'react';
import { chatbot } from '../api';
import { SurveyAnswers } from '../types';
import './ChatBot.css';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatBotProps {
  surveyResult: SurveyAnswers;
  language: string;
}

export const ChatBot: React.FC<ChatBotProps> = ({ surveyResult, language }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [error, setError] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Send initial greeting
    const greeting: Message = {
      id: Date.now().toString(),
      role: 'assistant',
      content: language === 'th' 
        ? '👋 สวัสดีค่ะ! ฉันเป็นผู้ช่วยวิเคราะห์ LGBTQ+ Sexual Fluidity ฉันได้ดูผลการสำรวจของคุณแล้ว มีอะไรที่คุณอยากถามเกี่ยวกับผลลัพธ์ของคุณไหมคะ?'
        : '👋 Hello! I\'m the LGBTQ+ Sexual Fluidity Analysis assistant. I\'ve reviewed your survey results. What would you like to know about your results?',
      timestamp: new Date(),
    };
    setMessages([greeting]);

    // Set initial suggestions
    setSuggestions(
      language === 'th'
        ? [
            'คะแนนของฉันหมายความว่าอย่างไร?',
            'ฉันควรทำอย่างไรต่อไป?',
            'อธิบายผลลัพธ์ให้ฉันฟังหน่อย',
            'มีคำแนะนำอะไรสำหรับฉันไหม?',
          ]
        : [
            'What do my scores mean?',
            'What should I do next?',
            'Can you explain my results?',
            'Do you have any suggestions for me?',
          ]
    );
  }, [language]);

  const sendMessage = async (messageText: string) => {
    if (!messageText.trim()) return;

    setError('');
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: messageText,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Prepare conversation history (last 5 messages)
      const conversationHistory = messages
        .slice(-5)
        .map((msg) => ({
          role: msg.role,
          content: msg.content,
        }));

      const response = await chatbot({
        survey_result: surveyResult,
        message: messageText,
        conversation_history: conversationHistory,
        language: language,
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.message,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setSuggestions(response.suggestions);
    } catch (err) {
      console.error('Chatbot error:', err);
      
      // แสดง error message ที่ละเอียดกว่า
      let errorMessage = language === 'th'
        ? 'เกิดข้อผิดพลาดในการส่งข้อความ กรุณาลองใหม่อีกครั้ง'
        : 'An error occurred while sending your message. Please try again.';
      
      if (err instanceof Error) {
        if (err.message.includes('timeout')) {
          errorMessage = language === 'th'
            ? '⏱️ การประมวลผลใช้เวลานานเกินไป กรุณาลองใหม่อีกครั้ง'
            : '⏱️ Request timeout. Please try again.';
        } else if (err.message.includes('Network Error')) {
          errorMessage = language === 'th'
            ? '🌐 ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ได้ กรุณาตรวจสอบการเชื่อมต่ออินเทอร์เน็ต'
            : '🌐 Network error. Please check your internet connection.';
        } else if (err.message) {
          // แสดง error message จาก server
          errorMessage = `❌ ${err.message}`;
        }
      }
      
      setError(errorMessage);
      
      // ลบข้อความของ user ที่ส่งไปแล้วเพื่อให้ลองส่งใหม่ได้
      setMessages((prev) => prev.filter(msg => msg.id !== userMessage.id));
      setInputMessage(messageText); // คืนค่าข้อความกลับไปให้ user แก้ไขได้
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(inputMessage);
  };

  const handleSuggestionClick = (suggestion: string) => {
    sendMessage(suggestion);
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h3>
          {language === 'th' 
            ? '💬 พูดคุยกับ AI ผู้ช่วย' 
            : '💬 Chat with AI Assistant'}
        </h3>
        <p className="chatbot-subtitle">
          {language === 'th'
            ? 'ถามคำถามเกี่ยวกับผลการสำรวจของคุณ'
            : 'Ask questions about your survey results'}
        </p>
      </div>

      <div className="chatbot-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message message-${message.role}`}>
            <div className="message-avatar">
              {message.role === 'assistant' ? '🤖' : '👤'}
            </div>
            <div className="message-content">
              <div className="message-text">{message.content}</div>
              <div className="message-time">
                {message.timestamp.toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message message-assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="message-text typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && (
        <div className="chatbot-error">
          ⚠️ {error}
        </div>
      )}

      {suggestions.length > 0 && !isLoading && (
        <div className="chatbot-suggestions">
          <p className="suggestions-label">
            {language === 'th' ? 'คำถามที่แนะนำ:' : 'Suggested questions:'}
          </p>
          <div className="suggestions-buttons">
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                className="suggestion-button"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="chatbot-input-form">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder={
            language === 'th'
              ? 'พิมพ์ข้อความของคุณ...'
              : 'Type your message...'
          }
          className="chatbot-input"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="chatbot-send-button"
          disabled={isLoading || !inputMessage.trim()}
        >
          {isLoading ? '⏳' : '📤'}
        </button>
      </form>
    </div>
  );
};
