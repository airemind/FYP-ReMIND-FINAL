import adminAxiosInstance from './adminAxiosInstance';

/* admin login */

export const adminLogin = async (data) => {
  const response = await adminAxiosInstance.post('/admin/login', data);
  return response.data;
};

/* admin logout */

export const adminLogout = async () => {
  const response = await adminAxiosInstance.post('/admin/logout');
  return response.data;
};

/* analytics */

export const getAdminAnalytics = async () => {
  const response = await adminAxiosInstance.get('/admin/analytics');
  return response.data;
};

/* all users */

export const getAllUsers = async () => {
  const response = await adminAxiosInstance.get('/admin/users');
  return response.data;
};

/* disable */

export const disableUser = async (userId) => {
  const response = await adminAxiosInstance.patch(`/admin/users/${userId}/disable`);
  return response.data;
};

/* enable user */

export const enableUser = async (userId) => {
  const response = await adminAxiosInstance.patch(`/admin/users/${userId}/enable`);
  return response.data;
};

/* update user */

export const updateUser = async (userId, data) => {
  const response = await adminAxiosInstance.put(`/admin/users/${userId}`, data);
  return response.data;
};

/* delete user */

export const deleteUser = async (userId) => {
  const response = await adminAxiosInstance.delete(`/admin/users/${userId}`);
  return response.data;
};

/* all memories */

export const getAllMemories = async () => {
  const response = await adminAxiosInstance.get('/admin/memories');
  return response.data;
};

/* delete chat */

export const deleteChatAdmin = async (chatId) => {
  const response = await adminAxiosInstance.delete(`/admin/chats/${chatId}`);
  return response.data;
};

/* delete message */

export const deleteMessageAdmin = async (messageId) => {
  const response = await adminAxiosInstance.delete(`/admin/messages/${messageId}`);
  return response.data;
};

/* system data */

export const getSystemData = async () => {
  const response = await adminAxiosInstance.get('/admin/data');
  return response.data;
};

/* delete log */

export const deleteLog = async (logId) => {
  const response = await adminAxiosInstance.delete(`/admin/logs/${logId}`);
  return response.data;
};

/* clear cache */

export const clearCache = async () => {
  const response = await adminAxiosInstance.delete('/admin/cache/clear');
  return response.data;
};

/* all media */

export const getAllMedia = async () => {
  const response = await adminAxiosInstance.get('/admin/media');
  return response.data;
};

/* delete media */

export const deleteMedia = async (mediaId) => {
  const response = await adminAxiosInstance.delete(`/admin/media/${mediaId}`);
  return response.data;
};
