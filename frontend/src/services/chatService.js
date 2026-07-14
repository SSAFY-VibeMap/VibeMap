import apiClient from './apiClient';

export const chatService = {
  sendMessage: (message) =>
    apiClient.post('/api/chat', {
      message,
    }),
};