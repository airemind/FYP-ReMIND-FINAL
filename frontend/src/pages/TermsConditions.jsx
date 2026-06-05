import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import '../styles/TermsConditions.css';
import logoLight from '../assets/images/logo-light.png';
import logoDark from '../assets/images/logo-dark.png';
import { FiMoon, FiSun } from 'react-icons/fi';

const TermsConditions = () => {
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  /* continue navigation */

  const handleAccept = () => {
    navigate('/login');
  };

  return (
    <div className="page">
      {/* header */}

      <header className="header">
        <div className="logo">
          <img
            src={theme === 'dark' ? logoDark : logoLight}
            alt="ReMIND Logo"
            className="logo-image"
          />
          <span className="logo-text">ReMIND</span>
        </div>
        <div className="header-actions">
          <div className="theme-toggle-container" onClick={toggleTheme}>
            {theme === 'light' ? (
              <FiMoon className="theme-toggle-icon" />
            ) : (
              <FiSun className="theme-toggle-icon sun" />
            )}
          </div>
        </div>
      </header>

      {/* main */}

      <main className="content">
        <h2 className="title center-title">Terms & Conditions</h2>

        <ol className="terms-list centered-list">
          <li>User must login to start using the app.</li>
          <li>
            Please cooperate what you are required to perform. If you are new
            <span className="link" onClick={() => navigate('/signup')}>
              <u>
                <b>Get Started</b>
              </u>
            </span>
            here.
          </li>
          <li>We apologize in advance if you face any inconvenience, as this is beta version.</li>
          <li>Your personal information will be fully secured and end-to-end encrypted.</li>
          <li>AI can make mistakes, please double check before reaching any final conclusion.</li>
        </ol>

        <div className="terms-warning">
          By using our product, you hereby accept our above mentioned
          <span className="highlight">Terms & Conditions</span>.
        </div>

        {/* go to login page */}

        <button className="login-button bottom-login" onClick={handleAccept}>
          Continue to Login
        </button>
      </main>

      {/* help */}

      <div className="help-button">?</div>
    </div>
  );
};
export default TermsConditions;
