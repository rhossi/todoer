'use client';

import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { chatAPI } from '@/lib/api';

interface ChatWindowProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function ChatWindow({ isOpen, onClose }: ChatWindowProps) {
  const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await chatAPI.sendMessage(userMessage, messages);
      setMessages((prev) => [...prev, { role: 'assistant', content: response.response }]);
    } catch (error: any) {
      console.error('Error sending message:', error);
      const errorMessage = error?.response?.data?.detail || error?.message || 'Sorry, I encountered an error. Please try again.';
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: `Error: ${errorMessage}`
      }]);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed bottom-20 right-4 w-96 h-[500px] rounded-3xl bg-charcoal border border-white/10 shadow-card flex flex-col z-50">
      <div className="bg-charcoal-muted text-white p-4 rounded-t-3xl flex justify-between items-center border-b border-white/5">
        <h3 className="font-semibold text-lg">Chat Assistant</h3>
        <button onClick={onClose} className="text-dash-gray hover:text-white text-xl">
          ✕
        </button>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-dash-gray text-center py-8">
            Start a conversation! Ask me to create, list, update, or delete todos.
          </div>
        )}
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] p-3 rounded-lg ${
                msg.role === 'user'
                  ? 'bg-dash-green text-gray-900'
                  : 'bg-charcoal-muted text-white border border-white/5'
              }`}
            >
              {msg.role === 'assistant' ? (
                <ReactMarkdown
                  className="markdown-content"
                  components={{
                    // Style paragraphs
                    p: ({ node, ...props }) => <p className="mb-2 last:mb-0" {...props} />,
                    // Style headings
                    h1: ({ node, ...props }) => <h1 className="text-lg font-bold mb-2 mt-3 first:mt-0" {...props} />,
                    h2: ({ node, ...props }) => <h2 className="text-base font-bold mb-2 mt-3 first:mt-0" {...props} />,
                    h3: ({ node, ...props }) => <h3 className="text-sm font-bold mb-1 mt-2 first:mt-0" {...props} />,
                    // Style code blocks
                    code: ({ node, inline, className, children, ...props }: any) => {
                      return inline ? (
                        <code className="bg-white/20 px-1 py-0.5 rounded text-xs font-mono" {...props}>
                          {children}
                        </code>
                      ) : (
                        <code className="block bg-white/10 p-2 rounded text-sm font-mono overflow-x-auto my-2" {...props}>
                          {children}
                        </code>
                      );
                    },
                    // Style pre blocks
                    pre: ({ node, ...props }) => <pre className="bg-white/10 p-2 rounded text-sm font-mono overflow-x-auto my-2" {...props} />,
                    // Style lists
                    ul: ({ node, ...props }) => <ul className="list-disc list-inside mb-2 space-y-1" {...props} />,
                    ol: ({ node, ...props }) => <ol className="list-decimal list-inside mb-2 space-y-1" {...props} />,
                    li: ({ node, ...props }) => <li className="ml-2" {...props} />,
                    // Style links
                    a: ({ node, ...props }) => (
                      <a className="text-blue-600 underline hover:text-blue-800" target="_blank" rel="noopener noreferrer" {...props} />
                    ),
                    // Style strong/bold
                    strong: ({ node, ...props }) => <strong className="font-bold" {...props} />,
                    // Style emphasis/italic
                    em: ({ node, ...props }) => <em className="italic" {...props} />,
                  }}
                >
                  {msg.content}
                </ReactMarkdown>
              ) : (
                <div className="whitespace-pre-wrap">{msg.content}</div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-charcoal-muted text-white p-2 rounded-lg border border-white/10">
              Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="p-4 border-t border-white/5 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type your message..."
          className="flex-1 px-3 py-2 rounded-2xl bg-charcoal-muted border border-white/10 text-white placeholder:text-dash-gray focus:outline-none focus:ring-2 focus:ring-dash-green"
          disabled={loading}
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="bg-dash-green text-gray-900 px-4 py-2 rounded-2xl font-semibold hover:bg-dash-green-strong disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}

