import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [url, setUrl] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleUrlChange = (event) => {
    setUrl(event.target.value);
  };

  const handleDownload = async (event) => {
    event.preventDefault(); // Prevents page refresh on form submission
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/download/', 
        { url: url }, 
        { headers: { 'Content-Type': 'application/json' } }
      );
      setVideoUrl(response.data.video_url);  // Assuming backend sends video URL
    } catch (error) {
      setError('Download failed. Please try again.');
      console.error('Download error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Instagram Video Downloader</h1>
      <form onSubmit={handleDownload}>
        <input
          type="text"
          value={url}
          onChange={handleUrlChange}
          placeholder="Enter Instagram video URL"
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Downloading...' : 'Download'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {videoUrl && (
        <div>
          <h2>Download Link</h2>
          <a href={videoUrl} download>
            Click here to download
          </a>
        </div>
      )}
    </div>
  );
}

export default App;
