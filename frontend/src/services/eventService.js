import apiClient from './apiClient';

export const eventService = {
  getEvents: (params = {}) => apiClient.get('/api/events', { params }),
  getEvent: (id) => apiClient.get(`/api/events/${id}`),
};