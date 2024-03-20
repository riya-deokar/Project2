import React, { useState } from 'react';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
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

      if (response.ok) {
        alert('File uploaded successfully');
      } else {
        alert('File upload failed');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file. Please try again.');
    }
  };

  const style = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'column',
    height: '100vh',
  };

  const buttonStyle = {
    marginTop: '20px',
    padding: '10px 20px',
    fontSize: '16px',
    cursor: 'pointer',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
  };

  return (
    <div style={style}>
      <input type="file" onChange={handleFileChange} accept="application/pdf" />
      <button style={buttonStyle} onClick={handleUpload}>Upload PDF</button>
    </div>
  );
}

export default App;
