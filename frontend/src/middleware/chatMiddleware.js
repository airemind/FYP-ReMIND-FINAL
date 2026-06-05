import axiosInstance from './axiosInstance';

// get chats
export const getChats = async () => {
  const response = await axiosInstance.get('/chats/');
  return response.data;
};

// create chats
export const createChat = async (data = {}) => {
  const response = await axiosInstance.post('/chats/', data);
  return response.data;
};

// delete chat
export const deleteChatById = async (chatId) => {
  const response = await axiosInstance.delete(`/chats/${chatId}`);
  return response.data;
};

// rename chat
export const renameChatById = async (chatId, data) => {
  const response = await axiosInstance.patch(`/chats/${chatId}`, data);
  return response.data;
};
