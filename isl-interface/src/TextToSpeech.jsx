import PropTypes from 'prop-types';

const TextToSpeech = ({ text }) => {
    const handleSpeak = () => {
        if (!text.trim()) return;
        const speech = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(speech);
    };

    return (
        <button onClick={handleSpeak}>
            Speak
        </button>
    );
};

TextToSpeech.propTypes = {
    text: PropTypes.string.isRequired,
};

export default TextToSpeech;
