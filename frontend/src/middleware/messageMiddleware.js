import axiosInstance from './axiosInstance';

// get message
export const getMessages = async (chatId) => {
  const response = await axiosInstance.get(`/messages/${chatId}`);
  return response.data;
};

// send message
export const sendMessageApi = async (chatId, data) => {
  const response = await axiosInstance.post(`/messages/${chatId}`, data);
  return response.data;
};
