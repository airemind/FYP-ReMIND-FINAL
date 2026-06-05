import { useEffect, useRef, useState } from 'react';
import { FiMenu, FiMoon, FiSun, FiUser } from 'react-icons/fi';
import { useTheme } from '../context/ThemeContext';
import '../styles/Topbar.css';
import ProfileDropdown from './ProfileDropdown';

const Topbar = ({ toggleMobileSidebar }) => {
  const { theme, toggleTheme } = useTheme();
  const [open, setOpen] = useState(false);
  const profileRef = useRef();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (profileRef.current && !profileRef.current.contains(event.target)) {
        setOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className="topbar">
      <div className="topbar-right">
        {/*  Mobile menu */}
        <div className="topbar-icon-wrapper mobile-menu-btn" onClick={toggleMobileSidebar}>
          <FiMenu className="topbar-icon" />
        </div>

        {/* theme */}

        <div className="topbar-icon-wrapper" onClick={toggleTheme}>
          {theme === 'light' ? (
            <FiMoon className="topbar-icon" />
          ) : (
            <FiSun className="topbar-icon sun" />
          )}
        </div>

        {/* profile */}

        <div className="profile-container" ref={profileRef}>
          <div className="topbar-icon-wrapper" onClick={() => setOpen(!open)}>
            <FiUser className="topbar-icon" />
          </div>
          {open && <ProfileDropdown />}
        </div>
      </div>
    </div>
  );
};

export default Topbar;
