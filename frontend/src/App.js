import React, { useState } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedFileName, setSelectedFileName] = useState(''); // State for file name
  const [uploadStatus, setUploadStatus] = useState('');
  const [documentText, setDocumentText] = useState('');
  const [sentiment, setSentiment] = useState('');
  const [keywords, setKeywords] = useState([]); // State for keywords
  const [keywordLinks, setKeywordLinks] = useState({});
  const [showLogin, setShowLogin] = useState(true);
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')));

  const handleFileChange = (event) => {
      const file = event.target.files[0];
      if (file) {
          setSelectedFile(file);
          setSelectedFileName(file.name);
      } else {
          setSelectedFile(null);
          setSelectedFileName('');
      }
      setUploadStatus('');
      setDocumentText('');
      setSentiment('');
      setKeywords([]);
      setKeywordLinks({});
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
              fetchLinksForKeywords(data.keywords);
          } else {
              setUploadStatus('File upload failed: ' + (data.error || 'Unknown Error'));
          }
      } catch (error) {
          console.error('Error uploading file:', error);
          setUploadStatus('Error uploading file. Please try again.');
      }
  };

  async function fetchLinksForKeywords(keywords) {
    let links = {};
    for (let keyword of keywords) {
        let nytimesURL = await fetchNYTimes(keyword);
        links[keyword] = {
            wikipedia: await fetchWikipedia(keyword),
            nytimes: nytimesURL
        };
    }
    setKeywordLinks(links);
};

async function fetchNYTimes(keyword) {
    const url = `/api/search/nytimes?keyword=${encodeURIComponent(keyword)}`;
    let response = await fetch(url);
    let data = await response.json();
    if (data.response.docs.length > 0) {
        return data.response.docs[0].web_url;
    } else {
        // Fallback search with a modified keyword or a broader term
        const fallbackKeyword = modifyKeywordForFallback(keyword);
        response = await fetch(`/api/search/nytimes?keyword=${encodeURIComponent(fallbackKeyword)}`);
        data = await response.json();
        return data.response.docs.length > 0 ? data.response.docs[0].web_url : '';
    }
}

async function fetchWikipedia(keyword) {
    const response = await fetch(`/api/search/wikipedia?keyword=${encodeURIComponent(keyword)}`);
    const data = await response.json();
    return data.result || '';
}

function modifyKeywordForFallback(keyword) {
    // Implement logic to modify the keyword for a fallback search
    // This could be simplifying the term, using a synonym, or removing specifics
    return keyword + ' general'; // Example modification
}

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
                  <button className="logout-button" onClick={handleLogout}>Logout</button>
                  <div className="file-input-container">
                      <label className="custom-file-button">
                          Choose File
                          <input className="file-input" type="file" onChange={handleFileChange} />
                      </label>
                      <span className="file-name">{selectedFileName}</span>
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
                              <ul className="keywords-list">
                                  {Object.entries(keywordLinks).map(([keyword, links]) => (
                                      <li key={keyword} className="keyword-item">
                                          <span className="keyword-text">{keyword}</span>
                                          {links.wikipedia && (
                                              <a href={links.wikipedia} target="_blank" rel="noopener noreferrer" className="keyword-link wikipedia-link">
                                                  (Wikipedia)
                                              </a>
                                          )}
                                          {links.nytimes ? (
                                            <a href={links.nytimes} target="_blank" rel="noopener noreferrer" className="keyword-link nyt-link">
                                              (NYTimes)
                                            </a>
                                          ) : (
                                            <span className="no-link">No NYTimes data. <a href={`https://www.nytimes.com/search?query=${keyword}`}>Search manually.</a></span>
                                          )}
                                      </li>
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
