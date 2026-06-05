import api from './axiosInstance';

export const processMemory = async ({ userPrompt, imageFile, audioFile, chatId, userId }) => {
  try {
    const formData = new FormData();

    /* user id */

    formData.append('user_id', userId);

    /* prompt */

    if (userPrompt) {
      formData.append('user_prompt', userPrompt);
    }

    /* chat */

    if (chatId) {
      formData.append('chat_id', String(chatId));
    }

    /* image */

    if (imageFile) {
      formData.append('image', imageFile);
    }

    /* audio */

    if (audioFile) {
      formData.append('audio', audioFile);
    }
    const response = await api.post('/memory/process', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
};
