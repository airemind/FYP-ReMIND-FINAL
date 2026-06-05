import axiosInstance from './axiosInstance';

// save profile setup
export const saveProfileSetup = async (data) => {
  const response = await axiosInstance.post('/profiles/setup', data);
  return response.data;
};
