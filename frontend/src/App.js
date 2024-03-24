import './App.css';
import React, { useState } from 'react';
import Login from './components/Login'; // Ensure this path is correct
import Register from './components/Register'; // Ensure this path is correct

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [documentText, setDocumentText] = useState('');
  const [sentiment, setSentiment] = useState('');
  const [showLogin, setShowLogin] = useState(true); // State to toggle between Login and Register
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user'))); // Load user from local storage


  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setUploadStatus('');
    setDocumentText('');
    setSentiment('');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('/api/upload/', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setUploadStatus('File uploaded successfully');
        setDocumentText(data.text); // Assuming the backend sends back the text
        setSentiment(data.sentiment); // Assuming the backend sends back the sentiment
      } else {
        setUploadStatus('File upload failed: ' + (data.error || 'Unknown Error'));
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadStatus('Error uploading file. Please try again.');
    }
  };

  const handleLogin = async (data) => {
    localStorage.setItem('user', JSON.stringify(data)); // Store user data in local storage
    setUser(data); // Set user state
  };

  const handleLogout = () => {
    localStorage.removeItem('user'); // Remove user data from local storage
    setUser(null); // Reset user state
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
          {/* Toggle between Login and Register */}
          {showLogin ? (
            <Login onLogin={handleLogin} />
          ) : (
            <Register onRegister={handleLogin} /> // Use the same handler for simplicity, adjust as necessary
          )}
          <button onClick={toggleAuthView}>
            {showLogin ? 'No account? Register here' : 'Have an account? Log in here'}
          </button>
        </>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
          {/* User is logged in, show content */}
          <button onClick={handleLogout}>Logout</button>
          <input type="file" onChange={handleFileChange} />
          <button onClick={handleUpload}>Upload Document</button>
          {uploadStatus && <div className="status-message">{uploadStatus}</div>}
          {documentText && <div className="document-content"><strong>Document Text:</strong> {documentText}</div>}
          {sentiment && <div className="sentiment-result"><strong>Sentiment Analysis:</strong> {sentiment}</div>}
        </div>
      )}
    </div>
  );



}

export default App;