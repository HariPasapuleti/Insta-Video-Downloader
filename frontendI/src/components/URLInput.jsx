import React, { useState } from "react";
import "./URLInput.css";

const URLInput = ({ onSearch, loading }) => {
  const [url, setUrl] = useState("");

  const handleChange = (event) => {
    setUrl(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!url.trim()) {
      return;
    }
    onSearch(url.trim());
  };

  return (
    <div className="url-input">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={url}
          onChange={handleChange}
          placeholder="Enter Instagram Video URL"
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </form>
    </div>
  );
};

export default URLInput;
