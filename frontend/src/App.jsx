import React, { useEffect, useRef, useState } from "react";
import "./App.css";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

const API_URL = "http://127.0.0.1:8000";

const quickTools = [
  { icon: "▤", label: "Notepad", tool: "notepad" },
  { icon: "▦", label: "Calculator", tool: "calculator" },
  { icon: "◉", label: "Screenshot", tool: "screenshot" },
  { icon: "◎", label: "Web Search", tool: "web_search" },
  { icon: "▱", label: "File Explorer", tool: "file_explorer" },
  { icon: "▥", label: "System Info", tool: "system_info" },
];

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeTool, setActiveTool] = useState(null);
  const [listening, setListening] = useState(false);
  const [search, setSearch] = useState("");

  const textareaRef = useRef(null);
  const messagesEndRef = useRef(null);

  // ---------------------------------------------------------
  // Prevent browser ctrl-wheel zoom where possible
  // ---------------------------------------------------------

  useEffect(() => {
    const preventZoom = (event) => {
      if (event.ctrlKey) {
        event.preventDefault();
      }
    };

    window.addEventListener("wheel", preventZoom, {
      passive: false,
      capture: true,
    });

    return () => {
      window.removeEventListener("wheel", preventZoom, {
        capture: true,
      });
    };
  }, []);

  // ---------------------------------------------------------
  // Auto scroll
  // ---------------------------------------------------------

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  // ---------------------------------------------------------
  // Auto resize textarea
  // ---------------------------------------------------------

  const resizeTextarea = () => {
    const textarea = textareaRef.current;

    if (!textarea) {
      return;
    }

    textarea.style.height = "auto";

    textarea.style.height = `${Math.min(
      textarea.scrollHeight,
      160
    )}px`;
  };

  // ---------------------------------------------------------
  // Send message
  // ---------------------------------------------------------

  const sendMessage = async () => {
    const text = input.trim();

    if (!text || loading) {
      return;
    }

    // Show user's message immediately
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text,
      },
    ]);

    setInput("");

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: text,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            data.message ||
            "Server returned an error."
        );
      }

      console.log("Backend JSON:", data);

      const answer =
        data.response ??
        data.message ??
        data.result ??
        data.answer ??
        data.output ??
        "Task completed.";

      console.log("Answer shown in UI:", answer);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: String(answer),
        },
      ]);
    } catch (error) {
      console.error("Chat error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: `Connection error: ${error.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // ---------------------------------------------------------
  // Keyboard
  // ---------------------------------------------------------

  const handleKeyDown = (event) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      sendMessage();
    }
  };

  // ---------------------------------------------------------
  // Quick tools
  // ---------------------------------------------------------

  const runQuickTool = async (tool, label) => {
    if (activeTool || loading) {
      return;
    }

    setActiveTool(tool);

    try {
      const response = await fetch(
        `${API_URL}/quick-tool`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            tool,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            data.message ||
            `Unable to run ${label}.`
        );
      }

      const result =
        data.response ??
        data.message ??
        data.result ??
        data.answer ??
        `${label} completed successfully.`;

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: String(result),
        },
      ]);
    } catch (error) {
      console.error("Quick tool error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: `${label}: ${error.message}`,
        },
      ]);
    } finally {
      setActiveTool(null);
    }
  };

  // ---------------------------------------------------------
  // New chat
  // ---------------------------------------------------------

  const newChat = () => {
    setMessages([]);
    setInput("");

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  // ---------------------------------------------------------
  // Voice
  // ---------------------------------------------------------

  const startVoiceInput = () => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text:
            "Voice input is not supported by this browser.",
        },
      ]);

      return;
    }

    if (listening) {
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      setListening(true);
    };

    recognition.onresult = (event) => {
      const transcript =
        event.results?.[0]?.[0]?.transcript || "";

      setInput(transcript);

      requestAnimationFrame(resizeTextarea);
    };

    recognition.onerror = (event) => {
      console.error(
        "Speech recognition:",
        event.error
      );

      setListening(false);
    };

    recognition.onend = () => {
      setListening(false);
    };

    recognition.start();
  };

  // ---------------------------------------------------------
  // History
  // ---------------------------------------------------------

  const history = [
    {
      title: "Personal AI Assistant",
      time: "Just now",
    },
    {
      title: "Desktop Control",
      time: "Earlier",
    },
  ];

  const filteredHistory = history.filter((item) =>
    item.title
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  // ---------------------------------------------------------
  // Render
  // ---------------------------------------------------------

  return (
    <div className="eternity-app">

      {/* =====================================================
          SIDEBAR
          ===================================================== */}

      <aside className="left-sidebar">

        <div className="logo-area">

          <div className="logo-mark">
            E
          </div>

          <div className="logo-name">
            ETERNITY
          </div>

        </div>

        <button
          className="new-chat-button"
          onClick={newChat}
        >
          <span>+</span>
          New chat
        </button>

        <div className="sidebar-search">

          <span>⌕</span>

          <input
            value={search}
            onChange={(event) =>
              setSearch(event.target.value)
            }
            placeholder="Search"
          />

        </div>

        <div className="sidebar-section-title">
          Recent
        </div>

        <div className="history-list">

          {filteredHistory.map(
            (item, index) => (

              <button
                className="history-button"
                key={index}
              >

                <span className="history-dot">
                  •
                </span>

                <span className="history-info">

                  <span>
                    {item.title}
                  </span>

                  <small>
                    {item.time}
                  </small>

                </span>

              </button>

            )
          )}

        </div>

        <div className="sidebar-bottom">

          <div className="connection">
            <span className="connection-dot"></span>
            Local AI
          </div>

          <div className="sidebar-version">
            ETERNITY
          </div>

        </div>

      </aside>

      {/* =====================================================
          MAIN CONTENT
          ===================================================== */}

      <main className="workspace">

        {/* Header */}

        <header className="workspace-header">

          <div>

            <div className="workspace-title">
              ETERNITY
            </div>

            <div className="workspace-subtitle">
              Personal AI assistant
            </div>

          </div>

          <div className="header-status">
            <span></span>
            Online
          </div>

        </header>

        {/* Chat */}

        <section className="chat-area">

          {/* Empty state */}

          {messages.length === 0 && !loading ? (

            <div className="empty-state">

              <div className="cosmic-core">

                <div className="energy-glow"></div>

                <div className="core-ring ring-one"></div>

                <div className="core-ring ring-two"></div>

                <div className="core-ring ring-three"></div>

                <div className="core-hole"></div>

                <div className="core-light"></div>

                <div className="core-light light-two"></div>

              </div>

              <h1>
                How can I help?
              </h1>

              <p>
                Ask anything or tell ETERNITY
                what you want to do.
              </p>

            </div>

          ) : null}

          {/* Messages */}

          <div className="message-list">

            {messages.map(
              (message, index) => (

                <div
                  className={`chat-message ${
                    message.role === "user"
                      ? "user-message"
                      : "assistant-message"
                  }`}
                  key={index}
                >

                  <div className="message-avatar">

                    {message.role === "user"
                      ? "Y"
                      : "E"}

                  </div>

                  <div className="message-body">

                    <div className="message-author">

                      {message.role === "user"
                        ? "You"
                        : "ETERNITY"}

                    </div>

                    <div className="message-content">
                      <ReactMarkdown
                        components={{
                          code({ node, inline, className, children, ...props }) {
                            const match = /language-(\w+)/.exec(
                              className || ""
                            );

                            const codeText = String(children).replace(
                              /\n$/,
                              ""
                            );

                            if (!inline && match) {
                              const copyCode = async () => {
                                try {
                                  await navigator.clipboard.writeText(
                                    codeText
                                  );
                                } catch (error) {
                                  console.error(
                                    "Copy failed:",
                                    error
                                  );
                                }
                              };

                              return (
                                <div className="code-block-wrapper">
                                  <div className="code-block-header">
                                    <span>{match[1]}</span>

                                    <button
                                      className="copy-code-button"
                                      onClick={copyCode}
                                    >
                                      Copy
                                    </button>
                                  </div>

                                  <SyntaxHighlighter
                                    style={oneDark}
                                    language={match[1]}
                                    PreTag="div"
                                    customStyle={{
                                      margin: 0,
                                      borderRadius: 0,
                                      background: "transparent",
                                      padding: "18px",
                                      fontSize: "14px",
                                      lineHeight: "1.6",
                                    }}
                                    {...props}
                                  >
                                    {codeText}
                                  </SyntaxHighlighter>
                                </div>
                              );
                            }

                            return (
                              <code
                                className={className}
                                {...props}
                              >
                                {children}
                              </code>
                            );
                          },
                        }}
                      >
                        {message.text ?? ""}
                      </ReactMarkdown>
                    </div>


                  </div>

                </div>

              )
            )}

            {/* Loading */}

            {loading && (

              <div className="chat-message assistant-message">

                <div className="message-avatar">
                  E
                </div>

                <div className="message-body">

                  <div className="message-author">
                    ETERNITY
                  </div>

                  <div className="loading-dots">

                    <span></span>
                    <span></span>
                    <span></span>

                  </div>

                </div>

              </div>

            )}

            <div ref={messagesEndRef} />

          </div>

        </section>

        {/* Composer */}

        <div className="composer-wrapper">

          <div className="composer">

            <textarea
              ref={textareaRef}
              value={input}
              onChange={(event) => {
                setInput(event.target.value);
                resizeTextarea();
              }}
              onKeyDown={handleKeyDown}
              placeholder="Message ETERNITY..."
              rows={1}
              disabled={loading}
            />

            <div className="composer-actions">

              <button
                className={`composer-button ${
                  listening ? "active" : ""
                }`}
                onClick={startVoiceInput}
                disabled={loading}
                title="Voice input"
              >
                ◉
              </button>

              <button
                className="send-button"
                onClick={sendMessage}
                disabled={
                  loading ||
                  !input.trim()
                }
                title="Send"
              >
                ↑
              </button>

            </div>

          </div>

          <div className="composer-note">
            ETERNITY uses your local AI to process requests.
          </div>

        </div>

      </main>

      {/* =====================================================
          RIGHT PANEL
          ===================================================== */}

      <aside className="right-sidebar">

        <div className="right-heading">
          Workspace
        </div>

        {/* System */}

        <section className="panel-section">

          <div className="section-label">
            System
          </div>

          <div className="system-list">

            <div className="system-item">

              <span>
                Status
              </span>

              <strong>
                Online
              </strong>

            </div>

            <div className="system-item">

              <span>
                Engine
              </span>

              <strong>
                Ollama
              </strong>

            </div>

            <div className="system-item">

              <span>
                Model
              </span>

              <strong>
                llama3.2:3b
              </strong>

            </div>

            <div className="system-item">

              <span>
                Mode
              </span>

              <strong>
                Local
              </strong>

            </div>

          </div>

        </section>

        {/* Quick tools */}

        <section className="panel-section">

          <div className="section-label">
            Tools
          </div>

          <div className="tool-list">

            {quickTools.map(
              (item) => (

                <button
                  className="tool-button"
                  key={item.tool}
                  onClick={() =>
                    runQuickTool(
                      item.tool,
                      item.label
                    )
                  }
                  disabled={
                    loading ||
                    activeTool !== null
                  }
                >

                  <span className="tool-icon">
                    {item.icon}
                  </span>

                  <span>
                    {activeTool === item.tool
                      ? "Running..."
                      : item.label}
                  </span>

                </button>

              )
            )}

          </div>

        </section>

        {/* Capabilities */}

        <section className="panel-section">

          <div className="section-label">
            Capabilities
          </div>

          <div className="capability-list">

            <div>
              Conversation
            </div>

            <div>
              Desktop control
            </div>

            <div>
              Computer vision
            </div>

            <div>
              Web search
            </div>

          </div>

        </section>

      </aside>

    </div>
  );
}

export default App;