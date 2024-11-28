import { useState } from 'react';
import WelcomePage from './WelcomePage';
import MainPage from './MainPage';

function App() {
    const [currentPage, setCurrentPage] = useState('welcome');
    // Navigate to the main page
    const handleWelcomeClick = () => setCurrentPage('main');

    return (
        <div>
            {currentPage === 'welcome' ? (
                <WelcomePage onClick={handleWelcomeClick} />
            ) : (
                <MainPage />
            )}
        </div>
    );
}

export default App;
