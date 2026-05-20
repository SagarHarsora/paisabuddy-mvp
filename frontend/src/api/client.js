import axios from 'axios'
import { useAuthStore } from '../store'

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000'

const client = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
client.interceptors.request.use((config) => {
  const { token } = useAuthStore.getState()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle response errors
client.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
    }
    throw error.response?.data || error
  }
)

export const apiClient = {
  // Auth
  requestOTP: (phone, language = 'en') =>
    client.post('/api/v1/auth/request-otp', { phone, language }),
  verifyOTP: (phone, otp) =>
    client.post('/api/v1/auth/verify-otp', { phone, otp }),

  // Upload
  uploadStatement: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return client.post('/api/v1/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  // Reports
  listReports: () => client.get('/api/v1/reports'),
  getReport: (statementId) => client.get(`/api/v1/reports/${statementId}`),

  // Health
  health: () => client.get('/api/v1/health'),
}

export default client
