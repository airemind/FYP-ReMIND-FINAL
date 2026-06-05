import { createContext, useContext, useEffect, useState } from 'react';
import { loginUser, logoutUser, saveToken, googleLogin } from '../middleware/authMiddleware';
import { getCurrentUser } from '../middleware/userMiddleware';

const AuthContext = createContext();
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  /* load user on refresh */

  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        setLoading(false);
        return;
      }
      try {
        const userData = await getCurrentUser();
        setUser(userData);
      } catch (error) {
        console.error(error);
        localStorage.removeItem('token');
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, []);

  /* normal login */

  const login = async (data) => {
    try {
      const response = await loginUser(data);
      const token = response?.access_token || response?.token;
      if (!token) {
        throw new Error('Token not received.');
      }
      saveToken(token);
      const userData = await getCurrentUser();
      setUser(userData);
      return response;
    } catch (error) {
      console.error(error);
      throw error;
    }
  };

  /* google login */

  const loginWithGoogle = async (data) => {
    try {
      const response = await googleLogin(data);
      const token = response?.access_token;
      if (!token) {
        throw new Error('Token not received.');
      }
      saveToken(token);
      const userData = await getCurrentUser();
      setUser(userData);
      return response;
    } catch (error) {
      console.error(error);
      throw error;
    }
  };

  /* logout */

  const logout = async () => {
    try {
      await logoutUser();
    } catch (error) {
      console.error(error);
    } finally {
      localStorage.removeItem('token');

      setUser(null);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        setUser,
        loading,
        login,
        loginWithGoogle,
        logout,
        setUser
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
export const useAuth = () => useContext(AuthContext);
