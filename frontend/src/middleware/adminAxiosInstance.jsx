import axios from 'axios';

const adminAxiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL,
  timeout: 10000
});

/* request interceptor */

adminAxiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin_token');
    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },

  (error) => {
    return Promise.reject(error);
  }
);

/* response interceptor */

adminAxiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (!error.response) {
      console.error('Network Error');
    }

    /* admin unauthorized */

    if (error.response?.status === 401) {
      localStorage.removeItem('admin_token');
      localStorage.removeItem('admin_data');
      if (window.location.pathname !== '/admin-portal') {
        window.location.href = '/admin-portal';
      }
    }
    if (error.response?.status === 500) {
      console.error('Server Error');
    }

    return Promise.reject(error);
  }
);

export default adminAxiosInstance;
