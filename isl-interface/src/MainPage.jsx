import { useState, useEffect } from 'react';

export default function MainPage() {
  const [detectedLetter, setDetectedLetter] = useState('-'); // State for detected letter

  // Function to fetch detected text from the server
  const fetchDetectedLetter = async () => {
    try {
      const response = await fetch('/detected_text'); // Replace with your actual endpoint
      const data = await response.json();
      setDetectedLetter(data.detected_text); // Update detected letter
    } catch (error) {
      console.error('Error fetching detected text:', error);
    }
  };

  // Periodically fetch detected letter
  useEffect(() => {
    const interval = setInterval(fetchDetectedLetter, 500); // Fetch every 500ms
    return () => clearInterval(interval); // Cleanup interval on component unmount
  }, []);

  return (
    <div style={{ textAlign: 'center', fontFamily: 'Arial, sans-serif' }}>
      <h1>Sign Language Gesture Detection</h1>
      <h3>
        Detected Letter: <span>{detectedLetter}</span>
      </h3>
      <img id="video" src="http://127.0.0.1:5000/video_feed" alt="Video Feed" />
    </div>
  );
}
