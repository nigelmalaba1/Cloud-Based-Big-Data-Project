import React, { useState } from "react";
import "./App.css";

function App() {
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [downloadLink, setDownloadLink] = useState(null);

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setDownloadLink(null);
    // Call your back-end API to trigger the processing
    
    const response = await fetch("http://localhost:5000/generate_ppt", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ user_input: userInput }),
});

     const result = await response.json();
     if (result.success) {
  setDownloadLink("http://localhost:5000/download_ppt?pptx_filename=" + result.pptx_filename);
}
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>Text to PowerPoint</h1>
      <textarea
        placeholder="Enter your text here"
        value={userInput}
        onChange={handleInputChange}
      ></textarea>
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Processing..." : "Generate PowerPoint"}
      </button>
      {downloadLink && (
        <a href={downloadLink} download="generated_presentation.pptx">
          Download PowerPoint
        </a>
      )}
    </div>
  );
}

export default App;
