import React, { useState } from "react";
import Header from "./components/Header";
import URLInput from "./components/URLInput";
import VideoOptions from "./components/VideoOptions";
import LoadingSpinner from "./components/LoadingSpinner";

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [videoReady, setVideoReady] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [thumbnail, setThumbnail] = useState("");
  const [caption, setCaption] = useState("");

  // Get API URL from environment variable or use default
  const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

  const handleSearch = async (url) => {
    try {
      setLoading(true);
      setError("");
      setVideoReady(false);
      setThumbnail("");
      setCaption("");
      
      const response = await fetch(`${API_URL}/api/download/`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({ url }),
      });
  
      const data = await response.json();
  
      if (!response.ok) {
        throw new Error(data.error || `HTTP error! Status: ${response.status}`);
      }
  
      if (data.message) {
        setDownloadUrl(data.message);
        setThumbnail(data.thumbnail || "");
        setCaption(data.caption || "");
        setVideoReady(true);
      } else {
        throw new Error("No video URL received");
      }
    } catch (error) {
      console.error("Error fetching video details:", error.message);
      if (error.message === "Failed to fetch") {
        setError("Unable to connect to the server. Please make sure the backend server is running.");
      } else {
        setError(error.message);
      }
      setVideoReady(false);
    } finally {
      setLoading(false);
    }
  };
  
  const handleDownload = () => {
    if (downloadUrl) {
      window.open(downloadUrl, "_blank");
    } else {
      setError("No video URL available for download.");
    }
  };

  const handleSignOut = () => {
    setIsLoggedIn(false);
  };

  return (
    <div className="app">
      <Header isLoggedIn={isLoggedIn} onSignOut={handleSignOut} />
      <div className="main-content">
        <URLInput onSearch={handleSearch} loading={loading} />
        {loading && <LoadingSpinner />}
        {error && <div className="error-message">{error}</div>}
        {videoReady && (
          <VideoOptions 
            onDownload={handleDownload} 
            thumbnail={thumbnail}
            caption={caption}
          />
        )}
      </div>
    </div>
  );
};

export default App;
