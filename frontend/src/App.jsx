import { useState, useEffect, useRef, useCallback } from "react";

/* ─── Markdown-lite renderer ─────────────────────────────────────────────── */
function renderMarkdown(text) {
  const lines = text.split("\n");
  const elements = [];
  let i = 0;
  let keyCount = 0;
  const k = () => keyCount++;

  while (i < lines.length) {
    const line = lines[i];

    // Code block
    if (line.startsWith("```")) {
      const lang = line.slice(3).trim();
      const codeLines = [];
      i++;
      while (i < lines.length && !lines[i].startsWith("```")) {
        codeLines.push(lines[i]);
        i++;
      }
      elements.push(
        <div key={k()} style={{ position: "relative", margin: "12px 0" }}>
          {lang && (
            <div
              style={{
                background: "#1a2744",
                color: "#64b5f6",
                fontSize: 11,
                padding: "4px 12px",
                borderRadius: "6px 6px 0 0",
                fontFamily: "'JetBrains Mono', monospace",
                letterSpacing: 1,
                borderTop: "1px solid #2d4a7a",
                borderLeft: "1px solid #2d4a7a",
                borderRight: "1px solid #2d4a7a",
              }}
            >
              {lang}
            </div>
          )}
          <pre
            style={{
              background: "#0d1b2e",
              color: "#e2e8f0",
              padding: "14px 16px",
              borderRadius: lang ? "0 6px 6px 6px" : 6,
              overflowX: "auto",
              fontSize: 13,
              lineHeight: 1.7,
              margin: 0,
              border: "1px solid #2d4a7a",
              fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
            }}
          >
            <code>{codeLines.join("\n")}</code>
          </pre>
        </div>,
      );
      i++;
      continue;
    }

    // Table
    if (line.includes("|") && lines[i + 1]?.includes("---")) {
      const headers = line
        .split("|")
        .filter((c) => c.trim())
        .map((c) => c.trim());
      i += 2;
      const rows = [];
      while (i < lines.length && lines[i].includes("|")) {
        rows.push(
          lines[i]
            .split("|")
            .filter((c) => c.trim())
            .map((c) => c.trim()),
        );
        i++;
      }
      elements.push(
        <div key={k()} style={{ overflowX: "auto", margin: "10px 0" }}>
          <table
            style={{ borderCollapse: "collapse", width: "100%", fontSize: 13 }}
          >
            <thead>
              <tr>
                {headers.map((h, hi) => (
                  <th
                    key={hi}
                    style={{
                      background: "#1a2744",
                      color: "#64b5f6",
                      padding: "8px 14px",
                      border: "1px solid #2d4a7a",
                      textAlign: "left",
                      fontWeight: 600,
                      fontFamily: "'Outfit', sans-serif",
                    }}
                  >
                    {inlineRender(h)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, ri) => (
                <tr
                  key={ri}
                  style={{ background: ri % 2 === 0 ? "#0d1827" : "#111f35" }}
                >
                  {row.map((cell, ci) => (
                    <td
                      key={ci}
                      style={{
                        padding: "7px 14px",
                        border: "1px solid #1e3358",
                        color: "#c8d8f0",
                        fontSize: 13,
                      }}
                    >
                      {inlineRender(cell)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>,
      );
      continue;
    }

    // H2
    if (line.startsWith("## ")) {
      elements.push(
        <h2
          key={k()}
          style={{
            color: "#60a5fa",
            fontSize: 16,
            fontWeight: 700,
            margin: "6px 0 10px",
            fontFamily: "'Outfit', sans-serif",
            letterSpacing: 0.3,
            borderBottom: "1px solid #1e3358",
            paddingBottom: 6,
          }}
        >
          {inlineRender(line.slice(3))}
        </h2>,
      );
      i++;
      continue;
    }

    // H3
    if (line.startsWith("### ")) {
      elements.push(
        <h3
          key={k()}
          style={{
            color: "#93c5fd",
            fontSize: 14,
            fontWeight: 600,
            margin: "8px 0 6px",
            fontFamily: "'Outfit', sans-serif",
          }}
        >
          {inlineRender(line.slice(4))}
        </h3>,
      );
      i++;
      continue;
    }

    // HR
    if (line.trim() === "---") {
      elements.push(
        <hr
          key={k()}
          style={{
            border: "none",
            borderTop: "1px solid #1e3358",
            margin: "10px 0",
          }}
        />,
      );
      i++;
      continue;
    }

    // List item
    if (line.match(/^[-•]\s/)) {
      const items = [];
      while (i < lines.length && lines[i].match(/^[-•]\s/)) {
        items.push(lines[i].replace(/^[-•]\s/, ""));
        i++;
      }
      elements.push(
        <ul key={k()} style={{ margin: "6px 0", paddingLeft: 20 }}>
          {items.map((item, ii) => (
            <li
              key={ii}
              style={{
                color: "#c8d8f0",
                fontSize: 13.5,
                marginBottom: 3,
                lineHeight: 1.5,
              }}
            >
              {inlineRender(item)}
            </li>
          ))}
        </ul>,
      );
      continue;
    }

    // Numbered list
    if (line.match(/^\d+\.\s/)) {
      const items = [];
      while (i < lines.length && lines[i].match(/^\d+\.\s/)) {
        items.push(lines[i].replace(/^\d+\.\s/, ""));
        i++;
      }
      elements.push(
        <ol key={k()} style={{ margin: "6px 0", paddingLeft: 22 }}>
          {items.map((item, ii) => (
            <li
              key={ii}
              style={{
                color: "#c8d8f0",
                fontSize: 13.5,
                marginBottom: 3,
                lineHeight: 1.5,
              }}
            >
              {inlineRender(item)}
            </li>
          ))}
        </ol>,
      );
      continue;
    }

    // Empty line
    if (!line.trim()) {
      elements.push(<div key={k()} style={{ height: 6 }} />);
      i++;
      continue;
    }

    // Paragraph
    elements.push(
      <p
        key={k()}
        style={{
          color: "#c8d8f0",
          fontSize: 13.5,
          lineHeight: 1.65,
          margin: "4px 0",
        }}
      >
        {inlineRender(line)}
      </p>,
    );
    i++;
  }
  return elements;
}

function inlineRender(text) {
  if (!text) return null;
  const parts = text.split(/(\*\*.*?\*\*|`.*?`|\*.*?\*)/g);
  return parts.map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**"))
      return (
        <strong key={i} style={{ color: "#93c5fd", fontWeight: 700 }}>
          {part.slice(2, -2)}
        </strong>
      );
    if (part.startsWith("`") && part.endsWith("`"))
      return (
        <code
          key={i}
          style={{
            background: "#0d1b2e",
            color: "#67e8f9",
            padding: "1px 6px",
            borderRadius: 4,
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: "0.9em",
            border: "1px solid #1e3a5a",
          }}
        >
          {part.slice(1, -1)}
        </code>
      );
    if (part.startsWith("*") && part.endsWith("*"))
      return (
        <em key={i} style={{ color: "#a5b4fc" }}>
          {part.slice(1, -1)}
        </em>
      );
    return part;
  });
}

/* ─── Icons ──────────────────────────────────────────────────────────────── */
const SendIcon = () => (
  <svg
    width="18"
    height="18"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2.2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <line x1="22" y1="2" x2="11" y2="13" />
    <polygon points="22 2 15 22 11 13 2 9 22 2" />
  </svg>
);
const BotIcon = () => (
  <svg
    width="16"
    height="16"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <rect x="3" y="11" width="18" height="10" rx="2" />
    <circle cx="12" cy="5" r="2" />
    <line x1="12" y1="7" x2="12" y2="11" />
    <line x1="8" y1="15" x2="8" y2="17" />
    <line x1="16" y1="15" x2="16" y2="17" />
  </svg>
);
const UserIcon = () => (
  <svg
    width="16"
    height="16"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
    <circle cx="12" cy="7" r="4" />
  </svg>
);
const SparkIcon = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4L12 17l-6.2 4.3 2.4-7.4L2 9.4h7.6z" />
  </svg>
);

/* ─── Typing indicator ───────────────────────────────────────────────────── */
function TypingDots() {
  return (
    <div
      style={{
        display: "flex",
        gap: 5,
        alignItems: "center",
        padding: "4px 0",
      }}
    >
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          style={{
            width: 7,
            height: 7,
            borderRadius: "50%",
            background: "#60a5fa",
            animation: `dotBounce 1.2s ease-in-out ${i * 0.2}s infinite`,
          }}
        />
      ))}
    </div>
  );
}

/* ─── Main App ───────────────────────────────────────────────────────────── */
export default function StudyBot() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: "bot",
      text: "Hello! 👋 I'm **StudyBot**, your NLP course assistant.\n\nI can help you with:\n- **Edit Distance & Spell Correction** (Lecture 3)\n- **Regular Expressions** (Lecture 2)\n- **Tokenization & Preprocessing** (Lecture 2)\n- **NLTK Code Examples** and Lab tasks\n- **NLP Career Guidance**\n\nWhat would you like to explore?",
      suggestions: [
        "What is NLP?",
        "Explain edit distance",
        "Show regex examples",
        "NLP career path",
      ],
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [connected, setConnected] = useState(null);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  // Check backend connectivity
  useEffect(() => {
    fetch("/api/health")
      .then((r) => r.json())
      .then(() => setConnected(true))
      .catch(() => setConnected(false));
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = useCallback(
    async (text) => {
      const msg = (text || input).trim();
      if (!msg || loading) return;
      setInput("");

      const userMsg = {
        id: Date.now(),
        role: "user",
        text: msg,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, userMsg]);
      setLoading(true);

      try {
        const res = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: msg }),
        });
        const data = await res.json();
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now() + 1,
            role: "bot",
            text: data.message,
            suggestions: data.suggestions || [],
            intent: data.intent,
            confidence: data.confidence,
            timestamp: new Date(),
          },
        ]);
      } catch {
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now() + 1,
            role: "bot",
            text: "⚠️ Can't reach the backend. Make sure Flask is running:\n```bash\npython app.py\n```",
            suggestions: [],
            timestamp: new Date(),
          },
        ]);
      }
      setLoading(false);
      inputRef.current?.focus();
    },
    [input, loading],
  );

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const fmt = (ts) =>
    ts.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  /* ── Styles ─────────────────────────────────────────────────────────────── */
  const s = {
    wrap: {
      height: "100vh",
      width: "100vw",
      background: "#060d1a",
      display: "flex",
      flexDirection: "column",
      alignItems: "stretch",
      justifyContent: "stretch",
      padding: 0,
      overflow: "hidden",
      backgroundImage:
        "radial-gradient(ellipse at 20% 50%, rgba(30,80,160,0.12) 0%, transparent 60%), radial-gradient(ellipse at 80% 20%, rgba(59,130,246,0.08) 0%, transparent 50%)",
      fontFamily: "'Outfit', 'Segoe UI', sans-serif",
    },
    card: {
      width: "100%",
      maxWidth: "100%",
      background: "rgba(10,18,35,0.97)",
      border: "none",
      borderRadius: 0,
      boxShadow: "none",
      display: "flex",
      flexDirection: "column",
      overflow: "hidden",
      height: "100vh",
      flex: 1,
    },
    header: {
      padding: "18px 24px",
      background: "linear-gradient(135deg, #0a1628 0%, #0f1f3d 100%)",
      borderBottom: "1px solid #1e3358",
      display: "flex",
      alignItems: "center",
      gap: 14,
      flexShrink: 0,
    },
    botAvatar: {
      width: 40,
      height: 40,
      borderRadius: 12,
      background: "linear-gradient(135deg, #1e40af, #3b82f6)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      color: "#fff",
      flexShrink: 0,
      boxShadow: "0 0 16px rgba(59,130,246,0.4)",
    },
    headerInfo: { flex: 1 },
    headerTitle: {
      color: "#e2e8f0",
      fontSize: 16,
      fontWeight: 700,
      margin: 0,
      letterSpacing: 0.3,
    },
    headerSub: { color: "#64748b", fontSize: 12, marginTop: 1 },
    statusDot: {
      width: 8,
      height: 8,
      borderRadius: "50%",
      background:
        connected === true
          ? "#22c55e"
          : connected === false
            ? "#ef4444"
            : "#f59e0b",
      boxShadow: connected === true ? "0 0 8px #22c55e" : "none",
    },
    statusText: { color: "#64748b", fontSize: 11, marginLeft: 6 },
    tags: { display: "flex", gap: 6 },
    tag: {
      background: "#1e3358",
      color: "#60a5fa",
      fontSize: 10,
      fontWeight: 600,
      padding: "3px 8px",
      borderRadius: 20,
      letterSpacing: 0.5,
      border: "1px solid #2d4a7a",
    },
    msgArea: {
      flex: 1,
      overflowY: "auto",
      padding: "20px 20px",
      scrollbarWidth: "thin",
      scrollbarColor: "#1e3358 transparent",
    },
    msgRow: (role) => ({
      display: "flex",
      gap: 10,
      marginBottom: 18,
      flexDirection: role === "user" ? "row-reverse" : "row",
      alignItems: "flex-start",
    }),
    avatar: (role) => ({
      width: 32,
      height: 32,
      borderRadius: 10,
      flexShrink: 0,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      background:
        role === "bot"
          ? "linear-gradient(135deg, #1e40af, #3b82f6)"
          : "linear-gradient(135deg, #1e3a5f, #2d5a8e)",
      color: "#fff",
      marginTop: 2,
      boxShadow: role === "bot" ? "0 0 12px rgba(59,130,246,0.25)" : "none",
      border: role === "bot" ? "1px solid #3b82f6" : "1px solid #2d4a7a",
    }),
    bubble: (role) => ({
      maxWidth: "83%",
      background:
        role === "bot"
          ? "linear-gradient(160deg, #0d1f3d 0%, #0a1628 100%)"
          : "linear-gradient(160deg, #1a3a6b 0%, #163161 100%)",
      border: role === "bot" ? "1px solid #1e3358" : "1px solid #2d5a9e",
      borderRadius:
        role === "bot" ? "4px 14px 14px 14px" : "14px 4px 14px 14px",
      padding: "12px 16px",
      boxShadow:
        role === "bot"
          ? "0 2px 12px rgba(0,0,0,0.3)"
          : "0 2px 12px rgba(0,0,50,0.4)",
    }),
    userText: { color: "#bfdbfe", fontSize: 14, lineHeight: 1.55 },
    meta: (role) => ({
      display: "flex",
      alignItems: "center",
      gap: 6,
      marginTop: 6,
      flexDirection: role === "user" ? "row-reverse" : "row",
    }),
    time: { color: "#374f6b", fontSize: 11 },
    intentBadge: {
      background: "#0d1b2e",
      border: "1px solid #1e3358",
      color: "#475569",
      fontSize: 10,
      padding: "1px 6px",
      borderRadius: 10,
      fontFamily: "'JetBrains Mono', monospace",
    },
    suggWrap: { display: "flex", flexWrap: "wrap", gap: 7, marginTop: 12 },
    suggBtn: {
      background: "rgba(30,51,88,0.6)",
      border: "1px solid #2d4a7a",
      color: "#93c5fd",
      fontSize: 12,
      padding: "5px 12px",
      borderRadius: 20,
      cursor: "pointer",
      display: "flex",
      alignItems: "center",
      gap: 5,
      transition: "all 0.15s",
      fontFamily: "'Outfit', sans-serif",
    },
    inputArea: {
      padding: "14px 20px 18px",
      background: "#060d1a",
      borderTop: "1px solid #1e3358",
      flexShrink: 0,
    },
    inputRow: {
      display: "flex",
      gap: 10,
      alignItems: "flex-end",
      background: "#0a1628",
      border: "1px solid #1e3358",
      borderRadius: 14,
      padding: "10px 14px",
      transition: "border-color 0.2s",
    },
    textarea: {
      flex: 1,
      background: "transparent",
      border: "none",
      outline: "none",
      color: "#e2e8f0",
      fontSize: 14,
      resize: "none",
      fontFamily: "'Outfit', sans-serif",
      lineHeight: 1.5,
      minHeight: 22,
      maxHeight: 120,
    },
    sendBtn: (canSend) => ({
      width: 38,
      height: 38,
      borderRadius: 10,
      border: "none",
      background: canSend
        ? "linear-gradient(135deg, #1d4ed8, #3b82f6)"
        : "#1e3358",
      color: canSend ? "#fff" : "#374f6b",
      cursor: canSend ? "pointer" : "not-allowed",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      flexShrink: 0,
      transition: "all 0.2s",
      boxShadow: canSend ? "0 0 16px rgba(59,130,246,0.35)" : "none",
    }),
    hint: { color: "#374f6b", fontSize: 11, marginTop: 8, textAlign: "center" },
    typingRow: {
      display: "flex",
      gap: 10,
      alignItems: "flex-start",
      marginBottom: 16,
    },
  };

  const canSend = input.trim().length > 0 && !loading;

  return (
    <div style={s.wrap}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html, body, #root { height: 100%; width: 100%; overflow: hidden; background: #060d1a; }
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #1e3358; border-radius: 3px; }
        @keyframes dotBounce {
          0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
          30% { transform: translateY(-6px); opacity: 1; }
        }
        @keyframes fadeSlide {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .msg-enter { animation: fadeSlide 0.25s ease-out; }
        .sugg-btn:hover {
          background: rgba(59,130,246,0.15) !important;
          border-color: #3b82f6 !important;
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(59,130,246,0.2);
        }
        .send-btn:hover:not(:disabled) { transform: scale(1.05); }
        .input-row:focus-within { border-color: #3b82f6 !important; box-shadow: 0 0 0 3px rgba(59,130,246,0.1); }
      `}</style>

      <div style={s.card}>
        {/* ── Header ── */}
        <div style={s.header}>
          <div style={s.botAvatar}>
            <BotIcon />
          </div>
          <div style={s.headerInfo}>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <p style={s.headerTitle}>StudyBot</p>
              <div style={{ display: "flex", alignItems: "center" }}>
                <div style={s.statusDot} />
                <span style={s.statusText}>
                  {connected === null
                    ? "connecting..."
                    : connected
                      ? "online"
                      : "offline"}
                </span>
              </div>
            </div>
            <p style={s.headerSub}>NLP Course Assistant · NUTECH AI-23</p>
          </div>
          <div style={s.tags}>
            <span style={s.tag}>NLTK</span>
            <span style={s.tag}>Python</span>
            <span style={s.tag}>NLP</span>
          </div>
        </div>

        {/* ── Messages ── */}
        <div style={s.msgArea}>
          {messages.map((msg) => (
            <div key={msg.id} className="msg-enter" style={s.msgRow(msg.role)}>
              <div style={s.avatar(msg.role)}>
                {msg.role === "bot" ? <BotIcon /> : <UserIcon />}
              </div>
              <div>
                <div style={s.bubble(msg.role)}>
                  {msg.role === "bot" ? (
                    <div>{renderMarkdown(msg.text)}</div>
                  ) : (
                    <p style={s.userText}>{msg.text}</p>
                  )}
                </div>

                <div style={s.meta(msg.role)}>
                  <span style={s.time}>{fmt(msg.timestamp)}</span>
                  {msg.intent && msg.intent !== "unknown" && (
                    <span style={s.intentBadge}>#{msg.intent}</span>
                  )}
                </div>

                {/* Quick suggestions */}
                {msg.role === "bot" && msg.suggestions?.length > 0 && (
                  <div style={s.suggWrap}>
                    {msg.suggestions.map((s_, si) => (
                      <button
                        key={si}
                        className="sugg-btn"
                        style={s.suggBtn}
                        onClick={() => sendMessage(s_)}
                      >
                        <SparkIcon />
                        {s_}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Typing indicator */}
          {loading && (
            <div style={s.typingRow} className="msg-enter">
              <div style={s.avatar("bot")}>
                <BotIcon />
              </div>
              <div style={{ ...s.bubble("bot"), padding: "12px 16px" }}>
                <TypingDots />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* ── Input ── */}
        <div style={s.inputArea}>
          <div className="input-row" style={s.inputRow}>
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKey}
              placeholder="Ask about edit distance, regex, tokenization..."
              style={s.textarea}
              rows={1}
              disabled={loading}
            />
            <button
              className="send-btn"
              style={s.sendBtn(canSend)}
              onClick={() => sendMessage()}
              disabled={!canSend}
            >
              <SendIcon />
            </button>
          </div>
          <p style={s.hint}>Press Enter to send · Shift+Enter for new line</p>
        </div>
      </div>
    </div>
  );
}
