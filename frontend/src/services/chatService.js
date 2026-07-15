import apiClient from './apiClient';

export const chatService = {
  sendMessage: (message, context = '') =>
    apiClient.post('/api/chat', {
      message: context
        ? `이전 대화 내용입니다. 이를 참고해 현재 질문에 답변하세요.\n${context}\n\n현재 사용자 질문: ${message}`
        : message,
    }),
};
