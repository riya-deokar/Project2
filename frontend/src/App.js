import './App.css';
import React, { useState } from 'react';
import Login from './components/Login'; // Ensure this path is correct
import Register from './components/Register'; // Ensure this path is correct

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [documentText, setDocumentText] = useState('');
  const [sentiment, setSentiment] = useState('');
  const [user, setUser] = useState(null); // State to manage user authentication
  const [showLogin, setShowLogin] = useState(true); // State to toggle between Login and Register

  const handleFileChange = (event) => {
    // Your existing file change handler
  };

  const handleUpload = async () => {
    // Your existing upload code
  };

  const handleLogin = async (email, password) => {
    // Your existing login handler
  };

  const handleRegister = async (email, password) => {
    // Your existing registration logic or similar to handleLogin but for registration
  };

  // Toggle between Login and Register view
  const toggleAuthView = () => setShowLogin(!showLogin);

  return (
    <div className="app-container">
      {!user ? (
        <>
          {showLogin ? (
            <Login onLogin={handleLogin} />
          ) : (
            <Register onRegister={handleRegister} />
          )}
          <button onClick={toggleAuthView}>
            {showLogin ? 'No account? Register here' : 'Have an account? Log in here'}
          </button>
        </>
      ) : (
        <>
          <input type="file" onChange={handleFileChange} />
          <button onClick={handleUpload}>Upload Document</button>
          {uploadStatus && <div className="status-message">{uploadStatus}</div>}
          {documentText && <div className="document-content"><strong>Document Text:</strong> {documentText}</div>}
          {sentiment && <div className="sentiment-result"><strong>Sentiment Analysis:</strong> {sentiment}</div>}
        </>
      )}
    </div>
  );
}

export default App;