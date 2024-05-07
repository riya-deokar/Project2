import React, { useState } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import './App.css';

// Function to fetch links for a keyword
async function fetchKeywordLinks(keyword) {
    const responses = await Promise.all([
        fetch(`/api/search/wikipedia?keyword=${keyword}`),
        fetch(`/api/search/nytimes?keyword=${keyword}`)
    ]);

    const data = await Promise.all(responses.map(res => res.json()));
    return { wikipedia: data[0].result, nytimes: data[1].result };
}

function App() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [selectedFileName, setSelectedFileName] = useState(''); // State for file name
    const [uploadStatus, setUploadStatus] = useState('');
    const [documentText, setDocumentText] = useState('');
    const [sentiment, setSentiment] = useState('');
    const [keywords, setKeywords] = useState([]); // State for keywords
    const [showLogin, setShowLogin] = useState(true);
    const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')));
    const [keywordLinks, setKeywordLinks] = useState({ wikipedia: '', nytimes: '' });

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            setSelectedFile(file);
            setSelectedFileName(file.name); // Set file name in state
        } else {
            setSelectedFile(null);
            setSelectedFileName(''); // Clear file name
        }
        setUploadStatus('');
        setDocumentText('');
        setSentiment('');
        setKeywords([]);
        setKeywordLinks({ wikipedia: '', nytimes: '' }); // Clear links when a new file is selected
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

    const fetchLinksForKeywords = async (keywords) => {
        // Fetch links for each keyword and set the results
        for (let keyword of keywords) {
            const links = await fetchKeywordLinks(keyword);
            setKeywordLinks(prev => ({
                wikipedia: links.wikipedia || prev.wikipedia,
                nytimes: links.nytimes || prev.nytimes
            }));
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
                    <button className="logout-button" onClick={handleLogout}>Logout</button>
                    <div className="file-input-container">
                        <label className="custom-file-button">
                            Choose File
                            <input className="file-input" type="file" onChange={handleFileChange} />
                        </label>
                        <span className="file-name">{selectedFileName}</span> {/* Display file name */}
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
                                        <li key={index}>
                                            {keyword}
                                            {keywordLinks.wikipedia && (
                                                <a href={keywordLinks.wikipedia} target="_blank" rel="noopener noreferrer"> (Wikipedia)</a>
                                            )}
                                            {keywordLinks.nytimes && (
                                                <a href={keywordLinks.nytimes} target="_blank" rel="noopener noreferrer"> (NYTimes)</a>
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
