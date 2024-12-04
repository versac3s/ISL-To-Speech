function updateDetectedLetter() {
  fetch("/detected_text")
    .then((response) => response.json())
    .then((data) => {
      const detectedLetterElement = document.getElementById("detected-letter");
      detectedLetterElement.textContent = data.detected_text;
    })
    .catch((error) => console.error("Error fetching detected text:", error));
}

function resetDetectedText() {
  fetch("/reset_detected_text", { method: "POST" })
    .then((response) => {
      if (response.ok) {
        const detectedLetterElement =
          document.getElementById("detected-letter");
        detectedLetterElement.textContent = "-";
      } else {
        console.error("Failed to reset detected text");
      }
    })
    .catch((error) => console.error("Error resetting detected text:", error));
}

function deleteLastLetter() {
  fetch("/delete_last_letter", { method: "POST" })
    .then((response) => response.json())
    .then((data) => {
      if (data.detected_text !== undefined) {
        const detectedLetterElement =
          document.getElementById("detected-letter");
        detectedLetterElement.textContent = data.detected_text;
      } else {
        console.error("Error deleting letter:", data.error);
      }
    })
    .catch((error) => console.error("Error deleting last letter:", error));
}

function stopLiveFeed() {
  fetch("/stop_live_feed", { method: "POST" })
    .then((response) => {
      if (response.ok) {
        const videoElement = document.getElementById("video");
        videoElement.src = "";
      } else {
        console.error("Failed to stop live feed");
      }
    })
    .catch((error) => console.error("Error stopping live feed:", error));
}
function addSpace() {
  fetch("/add_space", { method: "POST" })
    .then((response) => {
      if (response.ok) {
        console.log("Space added to detected text");
      } else {
        console.error("Failed to add space");
      }
    })
    .catch((error) => console.error("Error adding space:", error));
}

document.addEventListener("keydown", function (event) {
  if (event.code === "Space") {
    addSpace();
  }
});

function readDetectedText() {
  const detectedLetterElement = document.getElementById("detected-letter");
  const textToRead = detectedLetterElement.textContent;

  if (textToRead && textToRead !== "-") {
    const speech = new SpeechSynthesisUtterance(textToRead);
    speech.lang = "en-US";
    speech.rate = 1;
    speechSynthesis.speak(speech);
  } else {
    console.warn("No text available to read.");
  }
}

setInterval(updateDetectedLetter, 500);
