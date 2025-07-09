import React, { useState, useRef, useEffect } from "react";
import { sendChatMessage } from '../api';

const AI_AVATAR = "https://lh3.googleusercontent.com/aida-public/AB6AXuB0wTJWIrhQLopY-NST5feHfVDAW3zt9fBCsOqMH7dKm-alsHLUuB-obdVAvz9OW9yvwXShnjqyZPb3peYkyp_0qmg-JRqwrsXXlIF5QsSKJlMOL5Fwvlq-uEZqhXC1WuviG7Cm9F1vDsxt6qlUw8djKsMXcvB6-dERLimymkLwinEZVAi8UyU6VUxAWxkkeODlqWnUihH0ssmhexrOAhW6FKxh1Ywgc3l4luHOALFzb0_UBMalrmXPiJsrnZUXOGuZEBbt3TBqXgY";
const USER_AVATAR = "https://lh3.googleusercontent.com/aida-public/AB6AXuCowg1gvXl3EKMwpawwVdqdaWLKixCbSbj3seHqsvId_ih8u-jW9o68SBfvHmr_GgkeWydQ4NMVasHaV6a_vmnEGFgC6UeBQs01IfTSXtrQkuAjUDYu2aR7AU01mCFwoUd4sJx0FgMX4bTLLXnfN30fJGKtY-qnwaowq5MAnUMC42DHZ1jpZkSzUGDjRX_NVQte3tUtxPscdaZopJZly8xlDcVtPCXjxg09Jo97XKwNvjcGvp0VaL4ZrRzxRja7mxJm7j5gcKkxURA";

const Chat = () => {
  const [messages, setMessages] = useState([
    {
      sender: "ai",
      name: "AI Assistant",
      avatar: AI_AVATAR,
      text: "Hi there! I'm ready to help you analyze your data. What would you like to know?",
    },
  ]);
  const [input, setInput] = useState("");
  const [showAnalytics, setShowAnalytics] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    // On mount, check localStorage for uploaded file info
    const fileInfo = localStorage.getItem('uploadedFile');
    if (fileInfo) {
      setUploadedFile(JSON.parse(fileInfo));
    }
  }, []);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;
    setError(null);
    const userMsg = {
      sender: "user",
      name: "You",
      avatar: USER_AVATAR,
      text: input,
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);
    try {
      const res = await sendChatMessage(input);
      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          name: "AI Assistant",
          avatar: AI_AVATAR,
          text: res.response || res.reply || "(No response from backend)",
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          name: "AI Assistant",
          avatar: AI_AVATAR,
          text: "Sorry, there was an error contacting the backend.",
        },
      ]);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative flex size-full min-h-screen flex-col bg-[#141a1f] dark group/design-root overflow-x-hidden" style={{ fontFamily: 'Inter, "Noto Sans", sans-serif' }}>
      {/* Analytics Drawer */}
      {showAnalytics && (
        <div className="fixed inset-0 z-40 flex justify-end bg-black/40">
          <div className="w-full max-w-md h-full bg-[#232b33] shadow-xl flex flex-col animate-slide-in-right">
            <div className="flex items-center justify-between px-6 py-4 border-b border-[#2b3640]">
              <span className="text-white text-lg font-bold">Data Analytics</span>
              <button
                className="text-[#9daebe] hover:text-white p-2 rounded-full transition-colors"
                onClick={() => setShowAnalytics(false)}
                aria-label="Close analytics panel"
              >
                <svg width="22" height="22" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" d="M18 6 6 18M6 6l12 12"/></svg>
              </button>
            </div>
            <div className="flex-1 flex flex-col items-center justify-center text-[#dce8f3] px-6">
              <span className="text-xl font-semibold mb-2">Analytics features coming soon</span>
              <p className="text-[#9daebe] text-center">Here you will be able to view charts, summaries, and insights about your uploaded data.</p>
            </div>
          </div>
          {/* Click outside to close */}
          <div className="flex-1" onClick={() => setShowAnalytics(false)} />
        </div>
      )}
      <div className="layout-container flex h-full grow flex-col">
        {/* Header */}
        <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#2b3640] px-10 py-3">
          <div className="flex items-center gap-4 text-white">
            <div className="size-4">
              {/* Logo SVG */}
              <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path fillRule="evenodd" clipRule="evenodd" d="M24 18.4228L42 11.475V34.3663C42 34.7796 41.7457 35.1504 41.3601 35.2992L24 42V18.4228Z" fill="currentColor"></path>
                <path fillRule="evenodd" clipRule="evenodd" d="M24 8.18819L33.4123 11.574L24 15.2071L14.5877 11.574L24 8.18819ZM9 15.8487L21 20.4805V37.6263L9 32.9945V15.8487ZM27 37.6263V20.4805L39 15.8487V32.9945L27 37.6263ZM25.354 2.29885C24.4788 1.98402 23.5212 1.98402 22.646 2.29885L4.98454 8.65208C3.7939 9.08038 3 10.2097 3 11.475V34.3663C3 36.0196 4.01719 37.5026 5.55962 38.098L22.9197 44.7987C23.6149 45.0671 24.3851 45.0671 25.0803 44.7987L42.4404 38.098C43.9828 37.5026 45 36.0196 45 34.3663V11.475C45 10.2097 44.2061 9.08038 43.0155 8.65208L25.354 2.29885Z" fill="currentColor"></path>
              </svg>
            </div>
            <h2 className="text-white text-lg font-bold leading-tight tracking-[-0.015em]">Zanvar Data Insights</h2>
          </div>
          <div className="flex flex-1 justify-end gap-8">
            <div className="flex items-center gap-9">
              {/* ...existing nav links... */}
            </div>
            <div className="flex gap-2 items-center">
              {/* ...existing buttons... */}
              <div
                className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10 cursor-pointer border-2 border-[#dce8f3] hover:border-[#4fd1c5] transition-colors"
                style={{ backgroundImage: `url('https://lh3.googleusercontent.com/aida-public/AB6AXuDYdyNgyyZJ4noBYbSowbQlmHmOoT39UUwlEC_T057UfEahdu0OnGFRFCxmREtADsrlfZR9KE8G8w0As4FIHwcpS0lJf4WTu3Z8h-g4OzroeQn7u_R18GyuHYiqffgV_Ego8eJ3ON9Z2cBdt1YRrHSWUWkh2_hFmrUczIs6zmWo5sKsTOXmroNtBKycJ3CTJ5_s8KzaCsq7iH00lmHZGqhl9HGn6fEQFRYjBUwGdGifsFqPzptMAhVi4O5TPHtzdIhvYg7XI9esHsA')` }}
                onClick={() => window.location.href = '/profile'}
                title="Go to Profile"
              ></div>
            </div>
          </div>
        </header>
        <div className="px-4 md:px-40 flex flex-1 justify-center py-5">
          <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
            <h2 className="text-white tracking-light text-[28px] font-bold leading-tight px-4 text-left pb-3 pt-5">Chat with your data</h2>
            {/* Chat history */}
            <div className="flex-1 overflow-y-auto px-2 md:px-4 py-2 space-y-2 scrollbar-hide hide-scrollbar no-scrollbar" style={{maxHeight: '75vh', scrollbarWidth: 'none', msOverflowStyle: 'none'}}>
              {/* Show uploaded file info in a small box */}
              {uploadedFile && (
                <div className="mb-2 flex justify-end">
                  <div className="bg-[#232b33] text-[#dce8f3] px-4 py-2 rounded-lg shadow text-xs max-w-xs border border-[#4fd1c5]">
                    <div className="font-semibold">Uploaded File</div>
                    <div>Name: {uploadedFile.filename}</div>
                    <div>Format: {uploadedFile.format}</div>
                  </div>
                </div>
              )}
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex items-end gap-3 p-2 ${msg.sender === "user" ? "justify-end flex-row-reverse" : ""}`}
                >
                  <div
                    className="bg-center bg-no-repeat aspect-square bg-cover rounded-full w-10 shrink-0"
                    style={{backgroundImage: `url('${msg.avatar}')`}}
                  ></div>
                  <div className={`flex flex-1 flex-col gap-1 ${msg.sender === "user" ? "items-end" : "items-start"}`}>
                    <p className={`text-[#9daebe] text-[13px] font-normal leading-normal max-w-[360px] ${msg.sender === "user" ? "text-right" : ""}`}>{msg.name}</p>
                    <p className={`text-base font-normal leading-normal flex max-w-[360px] rounded-xl px-4 py-3 ${msg.sender === "user" ? "bg-[#dce8f3] text-[#141a1f]" : "bg-[#2b3640] text-white"}`}>{msg.text}</p>
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex items-center gap-2 text-[#9daebe] px-4 py-2">
                  <span className="animate-pulse">AI Assistant is typing...</span>
                </div>
              )}
              {error && (
                <div className="text-red-400 px-4 py-2">{error}</div>
              )}
              <div ref={messagesEndRef} />
            </div>
            {/* Input Section */}
            <form className="flex items-center px-4 py-3 gap-3" onSubmit={handleSend} autoComplete="off">
              <label className="flex flex-col min-w-40 h-12 flex-1">
                <div className="flex w-full flex-1 items-stretch rounded-xl h-full">
                  <input
                    placeholder="Ask a question about your data..."
                    className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-white focus:outline-0 focus:ring-0 border-none bg-[#2b3640] focus:border-none h-full placeholder:text-[#9daebe] px-4 rounded-r-none border-r-0 pr-2 text-base font-normal leading-normal"
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) handleSend(e); }}
                    disabled={loading}
                  />
                  <div className="flex border-none bg-[#2b3640] items-center justify-center pr-4 rounded-r-xl border-l-0 !pr-2">
                    <div className="flex items-center gap-4 justify-end">
                      <div className="flex items-center gap-1">
                        <button
                          type="button"
                          className="flex items-center justify-center p-1.5 hover:bg-[#232b33] rounded-full transition-colors"
                          tabIndex={0}
                          onClick={() => setShowAnalytics(true)}
                          aria-label="Open data analytics panel"
                        >
                          <div className="text-[#9daebe]">
                            {/* Chart Icon */}
                            <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" fill="currentColor" viewBox="0 0 256 256">
                              <path d="M232,208a8,8,0,0,1-8,8H32a8,8,0,0,1-8-8V48a8,8,0,0,1,16,0v94.37L90.73,98a8,8,0,0,1,10.07-.38l58.81,44.11L218.73,90a8,8,0,1,1,10.54,12l-64,56a8,8,0,0,1-10.07.38L96.39,114.29,40,163.63V200H224A8,8,0,0,1,232,208Z" />
                            </svg>
                          </div>
                        </button>
                      </div>
                      <button type="submit" className="min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-8 px-4 bg-[#dce8f3] text-[#141a1f] text-sm font-medium leading-normal hidden md:block">
                        <span className="truncate">Send</span>
                      </button>
                    </div>
                  </div>
                </div>
              </label>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
