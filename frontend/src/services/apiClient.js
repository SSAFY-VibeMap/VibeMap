const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function buildUrl(url, params) {
  const target = new URL(url, API_BASE_URL);

  if (params && typeof params === 'object') {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        target.searchParams.append(key, String(value));
      }
    });
  }

  return target.toString();
}

async function readErrorMessage(response) {
  try {
    const payload = await response.json();
    return payload?.detail || payload?.message || 'Request failed';
  } catch {
    return 'Request failed';
  }
}

async function request(url, options = {}) {
  const { params, data, headers, ...fetchOptions } = options;
  const response = await fetch(buildUrl(url, params), {
    ...fetchOptions,
    headers: {
      'Content-Type': 'application/json',
      ...(headers || {}),
    },
    body: data !== undefined ? JSON.stringify(data) : fetchOptions.body,
  });

  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

const apiClient = {
  get: (url, options = {}) => request(url, { ...options, method: 'GET' }),
  post: (url, data, options = {}) => request(url, { ...options, method: 'POST', data }),
  put: (url, data, options = {}) => request(url, { ...options, method: 'PUT', data }),
  delete: (url, options = {}) => request(url, { ...options, method: 'DELETE' }),
};

export { API_BASE_URL };
export default apiClient;