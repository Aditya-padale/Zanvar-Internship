// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Upload from './pages/Upload';
import Chat from './pages/Chat';
import Profile from './pages/Profile'; // Import the Profile page component
// import other pages as you build them

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/profile" element={<Profile />} /> {/* Add the /profile route */}
        {/* Add more routes like this */}
        {/* <Route path="/pricing" element={<Pricing />} /> */}
        {/* <Route path="/resources" element={<Resources />} /> */}
      </Routes>
    </Router>
  );
}

export default App;
