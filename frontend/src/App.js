import React, { useState, useCallback, useRef, useEffect } from 'react';
import Dropzone from 'react-dropzone';
import axios from 'axios';
import { Send, Upload, BarChart3, FileText, Image, Bot, Zap, TrendingUp, Database, Building2, Sparkles, Activity } from 'lucide-react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Welcome to Zanvar Group's Intelligent Analytics Platform! 🚀\n\nI'm your AI-powered data analysis assistant, designed to help you unlock insights from your manufacturing and quality control data.\n\n✨ **What I can do for you:**\n• 📊 Create professional charts and visualizations\n• 📈 Analyze quality control data and rejection patterns\n• 🔍 Provide detailed statistical insights\n• 📋 Generate comprehensive reports\n• 🎯 Suggest process improvements\n\n**Get started:** Upload your CSV, Excel, or PDF files and ask me anything about your data!",
      sender: 'bot',
      timestamp: new Date().toISOString()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const onDrop = useCallback(async (acceptedFiles) => {
    setIsLoading(true);
    try {
      for (const file of acceptedFiles) {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await axios.post('http://localhost:5000/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        
        setUploadedFiles(prev => [...prev, {
          name: file.name,
          size: file.size,
          type: file.type,
          info: response.data.file_info
        }]);
        
        // Add upload confirmation message
        const uploadMessage = {
          id: Date.now(),
          text: `File "${file.name}" uploaded successfully! ${response.data.message}`,
          sender: 'bot',
          timestamp: new Date().toISOString(),
          fileInfo: response.data.file_info
        };
        
        setMessages(prev => [...prev, uploadMessage]);
      }
    } catch (err) {
      console.error('Upload failed:', err);
      const errorMessage = {
        id: Date.now(),
        text: 'Sorry, there was an error uploading your file. Please try again.',
        sender: 'bot',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const sendMessage = async () => {
    if (!inputText.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: inputText,
      sender: 'user',
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/api/chat', {
        message: inputText,
        files: uploadedFiles.map(f => f.name)
      });

      const botMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        sender: 'bot',
        timestamp: response.data.timestamp
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error('Chat failed:', err);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const getFileIcon = (fileName) => {
    const extension = fileName.split('.').pop().toLowerCase();
    if (['csv', 'xlsx', 'xls'].includes(extension)) {
      return <BarChart3 className="w-4 h-4 text-green-500" />;
    } else if (extension === 'pdf') {
      return <FileText className="w-4 h-4 text-red-500" />;
    } else {
      return <Image className="w-4 h-4 text-blue-500" />;
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-zanvar-light to-blue-50 font-inter">
      {/* Enhanced Sidebar */}
      <div className="w-80 bg-gradient-to-b from-zanvar-dark to-zanvar-primary text-white shadow-zanvar">
        {/* Header */}
        <div className="p-6 border-b border-blue-800">
          <div className="flex items-center space-x-3 mb-2">
            <div className="w-10 h-10 bg-gradient-gold rounded-lg flex items-center justify-center">
              <Building2 className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold">Zanvar Group</h1>
              <p className="text-xs text-blue-200">Industries Analytics</p>
            </div>
          </div>
          <div className="flex items-center space-x-2 text-sm">
            <Bot className="w-4 h-4 text-accent-gold" />
            <span className="text-blue-100">Intelligent Chatbot</span>
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="p-4 border-b border-blue-800">
          <h3 className="text-sm font-semibold mb-3 text-blue-200 flex items-center">
            <Sparkles className="w-4 h-4 mr-2" />
            QUICK ACTIONS
          </h3>
          <div className="space-y-2">
            <button 
              onClick={() => setInputText("Show me top 5 rejection reasons")}
              className="w-full text-left text-xs bg-blue-800 hover:bg-blue-700 p-2 rounded transition-colors"
            >
              📊 Top rejection analysis
            </button>
            <button 
              onClick={() => setInputText("Create a pie chart of defect types")}
              className="w-full text-left text-xs bg-blue-800 hover:bg-blue-700 p-2 rounded transition-colors"
            >
              🥧 Defect distribution chart
            </button>
            <button 
              onClick={() => setInputText("Calculate rejection percentage")}
              className="w-full text-left text-xs bg-blue-800 hover:bg-blue-700 p-2 rounded transition-colors"
            >
              📈 Quality metrics
            </button>
          </div>
        </div>
        
        {/* Uploaded Files */}
        <div className="p-4 border-b border-blue-800">
          <h3 className="text-sm font-semibold mb-3 text-blue-200 flex items-center">
            <Database className="w-4 h-4 mr-2" />
            DATA SOURCES ({uploadedFiles.length})
          </h3>
          {uploadedFiles.length === 0 ? (
            <div className="text-center py-4">
              <Activity className="w-8 h-8 mx-auto text-blue-400 mb-2" />
              <p className="text-xs text-blue-300">No data uploaded yet</p>
              <p className="text-xs text-blue-400">Upload files to get started</p>
            </div>
          ) : (
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {uploadedFiles.map((file, index) => (
                <div key={index} className="bg-blue-800/50 p-3 rounded-lg">
                  <div className="flex items-center space-x-2 mb-1">
                    {getFileIcon(file.name)}
                    <span className="text-xs font-medium truncate flex-1">{file.name}</span>
                  </div>
                  <p className="text-xs text-blue-300">{formatFileSize(file.size)}</p>
                </div>
              ))}
            </div>
          )}
        </div>
        
        {/* Enhanced File Upload Zone */}
        <div className="p-4">
          <Dropzone onDrop={onDrop} multiple={true} accept={{
            'text/csv': ['.csv'],
            'application/vnd.ms-excel': ['.xls'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
            'application/pdf': ['.pdf'],
            'image/*': ['.png', '.jpg', '.jpeg', '.gif']
          }}>
            {({ getRootProps, getInputProps, isDragActive }) => (
              <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all duration-300 ${
                  isDragActive 
                    ? 'border-accent-gold bg-yellow-500/10 scale-105' 
                    : 'border-blue-500 hover:border-accent-gold hover:bg-blue-900/20'
                }`}
              >
                <input {...getInputProps()} />
                <div className="space-y-3">
                  <div className={`w-12 h-12 mx-auto rounded-lg flex items-center justify-center ${
                    isDragActive ? 'bg-gradient-gold' : 'bg-blue-700'
                  }`}>
                    <Upload className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-white">
                      {isDragActive ? 'Drop files here!' : 'Upload Data Files'}
                    </p>
                    <p className="text-xs text-blue-300 mt-1">
                      CSV, Excel, PDF, Images
                    </p>
                  </div>
                </div>
              </div>
            )}
          </Dropzone>
        </div>

        {/* Footer */}
        <div className="absolute bottom-0 left-0 right-0 p-4 bg-zanvar-dark">
          <div className="text-center">
            <p className="text-xs text-blue-300">Powered by</p>
            <p className="text-sm font-bold text-accent-gold">Zanvar Intelligence</p>
          </div>
        </div>
      </div>

      {/* Enhanced Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="bg-white border-b border-gray-200 p-4 shadow-sm">
          <div className="flex items-center justify-between max-w-4xl mx-auto">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-zanvar rounded-lg flex items-center justify-center">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-zanvar-dark">Zanvar Analytics Assistant</h2>
                <p className="text-sm text-text-muted">Ready to analyze your data</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm text-text-muted">Online</span>
            </div>
          </div>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          <div className="max-w-4xl mx-auto space-y-6">
            {messages.map((message) => (
              <div key={message.id} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-3xl rounded-2xl shadow-chat ${
                  message.sender === 'user' 
                    ? 'bg-gradient-zanvar text-white ml-12' 
                    : 'bg-white border border-gray-200 mr-12'
                }`}>
                  {message.sender === 'bot' && (
                    <div className="flex items-center space-x-3 p-4 pb-2 border-b border-gray-100">
                      <div className="w-8 h-8 bg-gradient-zanvar rounded-full flex items-center justify-center">
                        <Bot className="w-4 h-4 text-white" />
                      </div>
                      <div>
                        <p className="font-semibold text-zanvar-dark">Zanvar Assistant</p>
                        <p className="text-xs text-text-muted">AI Analytics Expert</p>
                      </div>
                    </div>
                  )}
                  
                  <div className="p-4">
                    {/* Enhanced message rendering with chart support */}
                    {(() => {
                      // Check for markdown-style image syntax first: ![Chart](data:image/png;base64,...)
                      const markdownImageRegex = /!\[.*?\]\((data:image\/png;base64,[A-Za-z0-9+/=]+)\)/;
                      const markdownMatch = message.text && message.text.match(markdownImageRegex);
                      
                      if (markdownMatch) {
                        const imageData = markdownMatch[1];
                        const textWithoutImage = message.text.replace(markdownImageRegex, '').trim();
                        
                        return (
                          <div>
                            {textWithoutImage && (
                              <div className="mb-4">
                                <p className="whitespace-pre-wrap leading-relaxed">{textWithoutImage}</p>
                              </div>
                            )}
                            <div className="bg-gray-50 p-4 rounded-xl">
                              <img 
                                src={imageData} 
                                alt="Generated Chart" 
                                className="max-w-full h-auto rounded-lg shadow-lg mx-auto border border-gray-200"
                                style={{ maxHeight: '500px' }}
                              />
                            </div>
                          </div>
                        );
                      }
                      
                      // Check for direct base64 image data
                      const imageRegex = /data:image\/png;base64,[A-Za-z0-9+/=]+/;
                      const match = message.text && message.text.match(imageRegex);
                      
                      if (match) {
                        const imageData = match[0];
                        const textWithoutImage = message.text.replace(imageRegex, '').trim();
                        
                        return (
                          <div>
                            {textWithoutImage && (
                              <div className="mb-4">
                                <p className="whitespace-pre-wrap leading-relaxed">{textWithoutImage}</p>
                              </div>
                            )}
                            <div className="bg-gray-50 p-4 rounded-xl">
                              <img 
                                src={imageData} 
                                alt="Generated Chart" 
                                className="max-w-full h-auto rounded-lg shadow-lg mx-auto border border-gray-200"
                                style={{ maxHeight: '500px' }}
                              />
                            </div>
                          </div>
                        );
                      }
                      
                      // No image found, display regular text with enhanced formatting
                      return <p className="whitespace-pre-wrap leading-relaxed">{message.text}</p>;
                    })()}
                    
                    {message.fileInfo && (
                      <div className="mt-4 p-3 bg-gray-50 rounded-lg border border-gray-200">
                        <p className="text-sm font-semibold text-zanvar-dark mb-2">📋 File Analysis Summary</p>
                        <pre className="text-xs text-gray-600 overflow-x-auto">
                          {JSON.stringify(message.fileInfo, null, 2)}
                        </pre>
                      </div>
                    )}
                    
                    <p className="text-xs mt-3 opacity-70">
                      {new Date(message.timestamp).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white border border-gray-200 p-6 rounded-2xl shadow-chat mr-12">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-gradient-zanvar rounded-full flex items-center justify-center">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-zanvar-primary rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-zanvar-secondary rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                        <div className="w-2 h-2 bg-accent-gold rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      </div>
                      <span className="text-zanvar-dark">Analyzing your data...</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Enhanced Input Area */}
        <div className="bg-white border-t border-gray-200 p-6">
          <div className="max-w-4xl mx-auto">
            <div className="flex items-end space-x-4">
              <div className="flex-1 relative">
                <textarea
                  ref={inputRef}
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask me anything about your data... (e.g., 'Show top 5 rejection reasons' or 'Create a pie chart')"
                  className="w-full p-4 pr-14 border-2 border-gray-200 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-zanvar-primary focus:border-transparent transition-colors"
                  rows={1}
                  style={{ minHeight: '52px', maxHeight: '120px' }}
                />
                <button
                  onClick={sendMessage}
                  disabled={!inputText.trim() || isLoading}
                  className="absolute right-3 bottom-3 w-10 h-10 bg-gradient-zanvar text-white rounded-lg hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
            <div className="flex items-center justify-between mt-4">
              <p className="text-xs text-text-muted">
                💡 Try: "Create charts", "Analyze quality data", "Calculate percentages"
              </p>
              <div className="flex items-center space-x-2 text-xs text-text-muted">
                <TrendingUp className="w-4 h-4" />
                <span>Powered by Zanvar AI</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

