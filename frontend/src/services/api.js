import axios from 'axios';

// Create axios instance
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${process.env.REACT_APP_API_URL || 'http://localhost:8000/api'}/auth/token/refresh/`, {
            refresh: refreshToken,
          });
          
          const { access } = response.data;
          localStorage.setItem('access_token', access);
          
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Clear auth data and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_data');
        
        // Only redirect if we're not already on login page
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  // Use standard JWT token endpoint for login
  login: async (credentials) => {
    try {
      console.log('Attempting login with credentials:', { username: credentials.username });
      const response = await api.post('/auth/login/', credentials);
      console.log('Login response:', response.data);
      // Transform the response to match expected format
      return {
        user: response.data.user,
        tokens: {
          access: response.data.tokens.access,
          refresh: response.data.tokens.refresh
        }
      };
    } catch (error) {
      console.error('Login API error:', error.response?.data || error.message);
      throw error;
    }
  },
  register: (userData) => api.post('/auth/register/', userData).then(res => res.data),
  logout: (data) => api.post('/auth/logout/', data).then(res => res.data),
  refreshToken: (data) => api.post('/auth/token/refresh/', data).then(res => res.data),
  getProfile: async () => {
    try {
      const response = await api.get('/auth/profile/');
      console.log('Profile response:', response.data);
      return response.data;
    } catch (error) {
      console.error('Get profile error:', error.response?.data || error.message);
      throw error;
    }
  },
  updateProfile: (profileData) => api.patch('/auth/profile/', profileData).then(res => res.data),
  changePassword: (passwordData) => api.post('/auth/change-password/', passwordData).then(res => res.data),
  getDashboardData: () => api.get('/auth/dashboard/').then(res => res.data),
};

// Invoice API
export const invoiceAPI = {
  upload: (formData) => api.post('/invoices/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }).then(res => res.data),
  getAll: (params) => api.get('/invoices/', { params }).then(res => res.data),
  getById: (id) => api.get(`/invoices/${id}/`).then(res => res.data),
  getStatus: (id) => api.get(`/invoices/${id}/status/`).then(res => res.data),
  reprocess: (id) => api.post(`/invoices/${id}/reprocess/`).then(res => res.data),
  delete: (id) => api.delete(`/invoices/${id}/delete/`).then(res => res.data),
  getStatistics: () => api.get('/invoices/statistics/').then(res => res.data),
  getMaterials: () => api.get('/invoices/materials/').then(res => res.data),
  getSuppliers: () => api.get('/invoices/suppliers/').then(res => res.data),
};

// Analytics API
export const analyticsAPI = {
  getCarbonScore: (params) => api.get('/analytics/carbon-score/', { params }).then(res => res.data),
  getBreakdown: (params) => api.get('/analytics/breakdown/', { params }).then(res => res.data),
  getTimeline: (params) => api.get('/analytics/timeline/', { params }).then(res => res.data),
  getMaterialBreakdown: (params) => api.get('/analytics/material-breakdown/', { params }).then(res => res.data),
  getSupplierBreakdown: (params) => api.get('/analytics/supplier-breakdown/', { params }).then(res => res.data),
};

// Recommendations API
export const recommendationsAPI = {
  getAll: (params) => api.get('/recommendations/', { params }).then(res => res.data),
  getByCategory: (category) => api.get(`/recommendations/${category}/`).then(res => res.data),
  markAsImplemented: (id) => api.post(`/recommendations/${id}/implement/`).then(res => res.data),
  getPriority: () => api.get('/recommendations/priority/').then(res => res.data),
};

// Simulations API
export const simulationsAPI = {
  runWhatIf: (scenario) => api.post('/simulations/what-if/', scenario).then(res => res.data),
  getScenarios: () => api.get('/simulations/scenarios/').then(res => res.data),
  saveScenario: (scenario) => api.post('/simulations/save/', scenario).then(res => res.data),
  getHistory: () => api.get('/simulations/history/').then(res => res.data),
};

export default api; 