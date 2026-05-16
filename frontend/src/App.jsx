import { useState } from "react";
import { SendHorizontal, TrainFront, User } from "lucide-react"; // Added User icon

function App() {
  const [userId] = useState("user_" + Math.random().toString(36).substring(7));
  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello 👋\nWelcome to Sri Lanka Railway Chatbot 🚆"
    }
  ]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = { sender: "user", text: message };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);

    try {
      const response = await fetch("https://sri-lanka-railway-nlp-chatbot-production.up.railway.app/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message, user_id: userId })
      });


      const data = await response.json();
      const botMessage = { sender: "bot", text: data.response };
      setMessages([...updatedMessages, botMessage]);
    } catch (error) {
      setMessages([
        ...updatedMessages,
        { sender: "bot", text: "Server connection failed ❌" }
      ]);
    }
    setMessage("");
  };

  return (
    <div className="bg-gray-100 h-screen flex justify-center items-center p-3">
      <div className="w-full max-w-md h-[95vh] bg-white rounded-3xl shadow-2xl flex flex-col overflow-hidden">
        
        {/* Header */}
        <div className="bg-blue-600 text-white p-4 flex items-center gap-3">
          <div className="bg-white text-blue-600 p-2 rounded-full">
            <TrainFront size={24} />
          </div>
          <div>
            <h1 className="font-bold text-lg">Railway Chatbot</h1>
            <p className="text-sm opacity-90">Sri Lanka Railways 🚆</p>
          </div>
        </div>

        {/* Messages Section */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex items-end gap-2 ${
                msg.sender === "user" ? "flex-row-reverse" : "flex-row"
              }`}
            >
              {/* Profile Icon */}
              <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center shadow-sm ${
                msg.sender === "user" ? "bg-blue-500 text-white" : "bg-white text-blue-600 border"
              }`}>
                {msg.sender === "user" ? <User size={16} /> : <TrainFront size={16} />}
              </div>

              {/* Message Bubble */}
              <div
                className={`max-w-[75%] px-4 py-3 rounded-2xl whitespace-pre-line text-sm shadow-sm ${
                  msg.sender === "user"
                    ? "bg-blue-600 text-white rounded-br-none"
                    : "bg-white text-gray-800 rounded-bl-none"
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
        </div>

        {/* Input Section */}
        <div className="p-3 border-t bg-white flex gap-2">
          <input
            type="text"
            placeholder="Ask about trains..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            className="flex-1 border rounded-full px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={sendMessage}
            className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-full transition"
          >
            <SendHorizontal size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;