import React from "react";

const VideoOptions = ({ onDownload }) => {
  return (
    <div className="video-options">
      <p>Video ready for download!</p>
      <button onClick={onDownload}>Download Video</button>
    </div>
  );
};

export default VideoOptions;
