import apiClient from './apiClient';

export const commentService = {
  createComment: (postId, data) => apiClient.post(`/api/posts/${postId}/comments`, data),
  updateComment: (postId, commentId, data) =>
    apiClient.put(`/api/posts/${postId}/comments/${commentId}`, data),
  deleteComment: (postId, commentId, password) =>
    apiClient.delete(`/api/posts/${postId}/comments/${commentId}`, { data: { password } }),
};