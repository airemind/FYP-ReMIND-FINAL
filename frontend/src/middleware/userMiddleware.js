import axiosInstance from './axiosInstance';
// current user
export const getCurrentUser = async () => {
  const response = await axiosInstance.get('/users/me');
  return response.data;
};
