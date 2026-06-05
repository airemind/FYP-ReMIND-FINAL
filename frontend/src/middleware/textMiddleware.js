import axiosInstance from './axiosInstance';

/* text processing */

export const processTextChat = async (data) => {
  const response = await axiosInstance.post('/text-processing/chat', data);
  return response.data;
};

/* user history */

export const getUserHistory = async (userId) => {
  const response = await axiosInstance.get(`/text-processing/history/user/${userId}`);
  return response.data;
};

/* chat history */

export const getChatHistory = async (chatId) => {
  const response = await axiosInstance.get(`/text-processing/history/chat/${chatId}`);
  return response.data;
};

/* single conversation */

export const getConversation = async (conversationId) => {
  const response = await axiosInstance.get(`/text-processing/history/${conversationId}`);
  return response.data;
};
