import React, { useState, useEffect, useRef } from "react";
import ReactDOM from "react-dom/client";
import "./styles.css";

const BACKEND_URL = "http://localhost:8000/save-memory";
const USER_ID = "user_123";

function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "👋 Welcome! What kind of life insurance plans are you looking for? Please enter your details like age, income, and goals." }
  ]);
  const [input, setInput] = useState("");
  const chatRef = useRef(null);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const newMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, newMsg]);
    setInput("");

    const loadingMsg = { sender: "bot", text: "⌛ Typing..." };
    setMessages((prev) => [...prev, loadingMsg]);

    try {
      const response = await fetch(BACKEND_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: USER_ID, text: input }),
      });
      const data = await response.json();
      const chunks = splitIntoChunks(data.ai_response || "Sorry, something went wrong.");
      setMessages((prev) => [
        ...prev.filter((m) => m.text !== "⌛ Typing..."),
        ...chunks.map((text) => ({ sender: "bot", text })),
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev.filter((m) => m.text !== "⌛ Typing..."),
        { sender: "bot", text: "⚠️ Error fetching response." },
      ]);
    }
  };

  const splitIntoChunks = (text, maxLength = 200) => {
    const sentences = text.split(/(?<=[.?!])\s+/);
    const chunks = [];
    let chunk = "";
    for (let sentence of sentences) {
      if ((chunk + sentence).length <= maxLength) {
        chunk += sentence + " ";
      } else {
        if (chunk) chunks.push(chunk.trim());
        chunk = sentence + " ";
      }
    }
    if (chunk) chunks.push(chunk.trim());
    return chunks;
  };

  useEffect(() => {
    // Do not auto scroll — keep layout static
  }, [messages]);

  return (
    <div>
      <h1>Life Insurance Chatbot</h1>
      <p>Your assistant for understanding insurance options</p>
      <div className="chat-area" ref={chatRef}>
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          placeholder="     Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
