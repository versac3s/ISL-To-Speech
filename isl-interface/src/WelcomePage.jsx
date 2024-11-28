import PropTypes from 'prop-types';
import './WelcomePage.css';
import peopleImage from './assets/people.png';
const WelcomePage = ({ onClick }) => {
    return (
        <div className="home_page" onClick={onClick}>
            <h1>Talking Hands</h1>
            <p className="description">
                This platform is designed to facilitate seamless communication by converting text to voice and voice to text, helping bridge the gap in language accessibility.
                <br />
                <span>Click anywhere to get started!</span>
            </p>
            <img src={peopleImage} alt="Welcome Illustration" />
        </div>
    );
};

WelcomePage.propTypes = {
    onClick: PropTypes.func.isRequired,
};

export default WelcomePage;
