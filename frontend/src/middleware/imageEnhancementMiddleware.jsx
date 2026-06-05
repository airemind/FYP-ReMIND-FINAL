import api from './axiosInstance';

export const enhanceImage = async (imageFile) => {
  try {
    const formData = new FormData();
    formData.append('file', imageFile);
    const response = await api.post('/image-ai/enhance', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      timeout: 0
    });
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
};
