import React, { useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Bot, Lightbulb, Send, Sparkles, User } from "lucide-react";

const promptPills = [
  "Explain Big O Notation",
  "Debug my Spring Boot API",
  "Optimize my React component re-renders",
];

const createMessage = ({ role, text }) => ({
  id: `${Date.now()}-${Math.round(Math.random() * 10000)}`,
  role,
  text,
});

const seededConversation = [
  createMessage({
    role: "assistant",
    text: "I can help with DSA, React, and Spring Boot. Ask for explanations, debugging, or practice strategies.",
  }),
  createMessage({
    role: "user",
    text: "Explain Big O Notation",
  }),
  createMessage({
    role: "assistant",
    text: "Big O describes how runtime grows as input size grows.\\n\\n```js\\n// O(n): one pass through the array\\nfunction containsTarget(arr, target) {\\n  for (const item of arr) {\\n    if (item === target) return true;\\n  }\\n  return false;\\n}\\n```\\n\\nFor interviews, focus on identifying loops, nested loops, and data structure operations.",
  }),
];

const escapeHtml = (value) =>
  value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#39;");

const formatInlineMarkdown = (text) => {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(
      /`([^`]+)`/g,
      '<code class="px-1.5 py-0.5 rounded bg-slate-200 text-slate-800 text-[12px]">$1</code>',
    )
    .replace(/\n/g, "<br />");
};

const renderMarkdownParts = (text) => {
  const segments = text.split(/```([\s\S]*?)```/g);
  return segments.map((segment, idx) => {
    const isCode = idx % 2 === 1;
    if (isCode) {
      return {
        type: "code",
        value: segment.trim(),
      };
    }
    return {
      type: "text",
      value: segment,
    };
  });
};

const getReply = (prompt) => {
  const normalized = prompt.toLowerCase();

  if (normalized.includes("big o")) {
    return "Big O tells you scalability. O(1) is constant, O(log n) is very efficient growth, O(n) is linear, O(n^2) usually appears with nested loops. I can also classify your own function step-by-step.";
  }

  if (normalized.includes("spring") || normalized.includes("api")) {
    return "For Spring Boot API debugging, verify controller mapping, request payload shape, validation errors, and CORS. Start by checking backend logs first, then network tab status codes in the frontend.";
  }

  return "I can explain the concept in plain language, then convert it into interview-ready points and a short practice task.";
};

const AIChat = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState(seededConversation);
  const messagesContainerRef = useRef(null);

  useEffect(() => {
    const container = messagesContainerRef.current;
    if (!container) {
      return;
    }

    container.scrollTo({
      top: container.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  const canSend = input.trim().length > 0;

  const submitPrompt = (promptText) => {
    const prompt = promptText.trim();
    if (!prompt) return;

    const userMessage = createMessage({ role: "user", text: prompt });
    const aiMessage = createMessage({
      role: "assistant",
      text: getReply(prompt),
    });

    setMessages((prev) => [...prev, userMessage, aiMessage]);
    setInput("");
  };

  const startNewChat = () => {
    setMessages([
      createMessage({
        role: "assistant",
        text: "New chat started. Ask me anything about DSA, React, or Spring Boot.",
      }),
    ]);
    setInput("");
  };

  const parsedMessages = useMemo(
    () =>
      messages.map((message) => ({
        ...message,
        parts: renderMarkdownParts(message.text),
      })),
    [messages],
  );

  return (
    <div className="bg-slate-50 min-h-full">
      <section className="max-w-5xl mx-auto bg-white border border-slate-200 shadow-sm rounded-2xl p-4 md:p-6">
        <header className="pb-4 border-b border-slate-200">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-2xl md:text-3xl font-bold text-slate-800">
                Adaptive Learning Assistant
              </h2>
            </div>
            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-50 text-emerald-700 text-xs font-medium">
              <Sparkles className="w-3.5 h-3.5" />
              Live Tutor
            </span>
          </div>

          <div className="flex flex-wrap gap-2 mt-4">
            <button
              onClick={startNewChat}
              className="px-4 py-2 rounded-full text-sm font-medium bg-emerald-50 text-emerald-700 hover:bg-emerald-100 transition-colors"
            >
              New Chat
            </button>
          </div>
        </header>

        <div
          ref={messagesContainerRef}
          className="h-[54vh] overflow-y-auto py-4 pr-1 space-y-4"
        >
          <AnimatePresence initial={false}>
            {parsedMessages.map((message) => (
              <motion.article
                key={message.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.2, ease: "easeOut" }}
                className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[92%] md:max-w-[85%] rounded-2xl px-4 py-3 ${
                    message.role === "user"
                      ? "bg-emerald-500 text-white"
                      : "bg-slate-100 text-slate-800"
                  }`}
                >
                  <div className="flex items-center gap-2 mb-2 text-xs font-semibold opacity-90">
                    {message.role === "assistant" ? (
                      <Bot className="w-3.5 h-3.5" />
                    ) : (
                      <User className="w-3.5 h-3.5" />
                    )}
                    {message.role === "assistant" ? "AI Tutor" : "You"}
                  </div>

                  <div className="space-y-3">
                    {message.parts.map((part, idx) => {
                      if (part.type === "code") {
                        return (
                          <pre
                            key={`${message.id}-part-${idx}`}
                            className="rounded-xl border border-slate-300 bg-slate-900 text-slate-100 p-3 overflow-x-auto text-[13px] leading-relaxed"
                          >
                            <code>{part.value}</code>
                          </pre>
                        );
                      }

                      return (
                        <p
                          key={`${message.id}-part-${idx}`}
                          className="text-sm leading-relaxed"
                          dangerouslySetInnerHTML={{
                            __html: formatInlineMarkdown(
                              escapeHtml(part.value),
                            ),
                          }}
                        />
                      );
                    })}
                  </div>
                </div>
              </motion.article>
            ))}
          </AnimatePresence>
        </div>

        <footer className="pt-4 border-t border-slate-200">
          <div className="flex flex-wrap gap-2 mb-3">
            {promptPills.map((pill) => (
              <button
                key={pill}
                onClick={() => submitPrompt(pill)}
                className="rounded-full border border-slate-200 bg-white hover:bg-slate-50 text-slate-600 px-3 py-1.5 text-xs font-medium inline-flex items-center gap-1.5"
              >
                <Lightbulb className="w-3.5 h-3.5 text-emerald-600" />
                {pill}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-3">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  submitPrompt(input);
                }
              }}
              placeholder="Ask anything about DSA, React, or Spring Boot"
              className="flex-1 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-800 placeholder:text-slate-500 outline-none focus:ring-2 focus:ring-emerald-500/35 focus:border-emerald-500"
            />
            <button
              onClick={() => submitPrompt(input)}
              disabled={!canSend}
              className="w-11 h-11 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white flex items-center justify-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </footer>
      </section>
    </div>
  );
};

export default AIChat;
