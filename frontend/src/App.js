import React, { useState } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import './App.css';

function App() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState('');
    const [documentText, setDocumentText] = useState('');
    const [sentiment, setSentiment] = useState('');
    const [keywords, setKeywords] = useState([]); // New state for keywords
    const [showLogin, setShowLogin] = useState(true);
    const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')));

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
        setUploadStatus('');
        setDocumentText('');
        setSentiment('');
        setKeywords([]); // Clear keywords when a new file is selected
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
                setDocumentText(data.text);
                setSentiment(data.sentiment);
                setKeywords(data.keywords); // Update keywords from response
            } else {
                setUploadStatus('File upload failed: ' + (data.error || 'Unknown Error'));
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            setUploadStatus('Error uploading file. Please try again.');
        }
    };

    const handleLogin = async (data) => {
        localStorage.setItem('user', JSON.stringify(data));
        setUser(data);
    };

    const handleLogout = () => {
        localStorage.removeItem('user');
        setUser(null);
    };

    const toggleAuthView = () => setShowLogin(!showLogin);

    return (
      <div className="app-container">
          {!user ? (
              <>
                  {showLogin ? <Login onLogin={handleLogin} /> : <Register onRegister={handleLogin} />}
                  <button onClick={toggleAuthView}>
                      {showLogin ? 'No account? Register here' : 'Have an account? Log in here'}
                  </button>
              </>
          ) : (
              <div className="main-content">
                  <button onClick={handleLogout}>Logout</button>
                  <div className="file-input-container">
                      <input className="file-input" type="file" onChange={handleFileChange} />
                      <button className="upload-button" onClick={handleUpload}>Upload Document</button>
                  </div>
                  {uploadStatus && <div className="status-message">{uploadStatus}</div>}
                  <div className="document-keywords-container">
                      {documentText && (
                          <div className="document-content">
                              <strong>Document Text:</strong> {documentText}
                          </div>
                      )}
                      {keywords.length > 0 && (
                          <div className="keywords-section">
                              <strong>Keywords:</strong>
                              <ul>
                                  {keywords.map((keyword, index) => (
                                      <li key={index}>{keyword}</li>
                                  ))}
                              </ul>
                          </div>
                      )}
                  </div>
                  {sentiment && (
                      <div className="sentiment-result">
                          <strong>Sentiment Analysis:</strong> {sentiment}
                      </div>
                  )}
              </div>
          )}
      </div>
  );  
}

export default App;
