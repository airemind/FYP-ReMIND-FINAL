import React from 'react';
import { useAuth } from '../context/AuthContext';

const ProfileDropdown = () => {
  const { logout, user } = useAuth();
  return (
    <div className="profile-dropdown">
      <div className="profile-info">
        <p>
          <strong>{user?.username}</strong>
        </p>
        <p>Session ID: {user?.id}</p>
      </div>
      <div className="dropdown-item danger" onClick={logout}>
        Logout
      </div>
    </div>
  );
};

export default ProfileDropdown;
