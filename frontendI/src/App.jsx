import React, { useState } from "react";
import Header from "./components/Header";
import URLInput from "./components/URLInput";
import VideoOptions from "./components/VideoOptions";

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [videoReady, setVideoReady] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState("");

  const handleSearch = async (url) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/download/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      const data = await response.json();
      console.log(data);
  
      // Check if the download was successful
      if (data.message) {
        setDownloadUrl(data.message); // Set the download URL
        setVideoReady(true); // Video is ready for download
      } else {
        console.error("Error: No video URL received.");
        setVideoReady(false);
      }
    } catch (error) {
      console.error("Error fetching video details:", error.message);
    }
  };
  
  const handleDownload = () => {
    if (downloadUrl) {
      window.open(downloadUrl, "_blank"); // Open video in new tab for download
    } else {
      alert("No video URL available for download.");
    }
  };

  const handleSignOut = () => {
    setIsLoggedIn(false);
  };

  return (
    <div className="app">
      <Header isLoggedIn={isLoggedIn} onSignOut={handleSignOut} />
      <URLInput onSearch={handleSearch} />
      {videoReady && <VideoOptions onDownload={handleDownload} />}
    </div>
  );
};

export default App;
