import apiClient from './apiClient';

export const postService = {
  getPosts: (params = {}) => apiClient.get('/api/posts', { params }),
  getPost: (id) => apiClient.get(`/api/posts/${id}`),
  createPost: (data) => apiClient.post('/api/posts', data),
  updatePost: (id, data) => apiClient.put(`/api/posts/${id}`, data),
  deletePost: (id, password) => apiClient.delete(`/api/posts/${id}`, { data: { password } }),
};