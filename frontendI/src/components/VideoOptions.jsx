import React, { useState, useEffect } from 'react';
import './VideoOptions.css';

const VideoOptions = ({ onDownload, thumbnail, caption }) => {
  const [thumbnailError, setThumbnailError] = useState(false);
  const [thumbnailLoaded, setThumbnailLoaded] = useState(false);

  useEffect(() => {
    if (thumbnail) {
      console.log('Thumbnail URL received:', thumbnail);
      console.log('Thumbnail URL type:', typeof thumbnail);
      console.log('Thumbnail URL length:', thumbnail.length);
      setThumbnailError(false);
      setThumbnailLoaded(false);
    }
  }, [thumbnail]);

  const handleThumbnailError = (error) => {
    console.error('Thumbnail loading error:', error);
    console.error('Error target:', error.target);
    console.error('Error type:', error.type);
    console.error('Current thumbnail URL:', thumbnail);
    setThumbnailError(true);
    setThumbnailLoaded(true);
  };

  const handleThumbnailLoad = () => {
    console.log('Thumbnail loaded successfully');
    setThumbnailLoaded(true);
  };

  const getThumbnailSrc = () => {
    if (!thumbnail) return '';
    
    // Check if it's a base64 image
    if (thumbnail.startsWith('data:image')) {
      return thumbnail;
    }
    
    // Check if it's a URL
    if (thumbnail.startsWith('http')) {
      return thumbnail;
    }
    
    // If it's neither, log the issue
    console.error('Invalid thumbnail format:', thumbnail);
    return '';
  };

  return (
    <div className="video-options">
      {thumbnail && !thumbnailError && (
        <div className="thumbnail-container">
          {!thumbnailLoaded && (
            <div className="thumbnail-loading">
              <div className="loading-spinner"></div>
              <p>Loading thumbnail...</p>
            </div>
          )}
          <img 
            src={getThumbnailSrc()} 
            alt="Video thumbnail" 
            className="video-thumbnail"
            onError={handleThumbnailError}
            onLoad={handleThumbnailLoad}
            style={{ display: thumbnailLoaded ? 'block' : 'none' }}
          />
        </div>
      )}
      {thumbnailError && (
        <div className="thumbnail-error">
          <p>Thumbnail preview not available</p>
        </div>
      )}
      {caption && <p className="video-caption">{caption}</p>}
      <button onClick={onDownload} className="download-button">
        Download Video
      </button>
    </div>
  );
};

export default VideoOptions;
