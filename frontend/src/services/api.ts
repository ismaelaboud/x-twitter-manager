import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

console.log('API Base URL:', BASE_URL) // Debug log

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor for adding authentication token
api.interceptors.request.use(
  config => {
    console.log('API Request:', config.method, config.url, config.data) // Detailed logging
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// Response interceptor for logging
api.interceptors.response.use(
  response => {
    console.log('API Response:', response.data) // Detailed logging
    return response
  },
  error => {
    console.error('API Error:', error.response ? error.response.data : error.message)
    return Promise.reject(error)
  }
)

export const authService = {
  login: async (username: string, password: string) => {
    try {
      const response = await api.post('/auth/login', { username, password })
      return response.data
    } catch (error) {
      console.error('Login failed', error)
      throw error
    }
  },
  
  registerAccount: async (accountDetails: any) => {
    try {
      console.log('Registering account:', accountDetails) // Debug log
      const response = await api.post('/accounts/register', accountDetails)
      console.log('Registration response:', response.data) // Debug log
      return response.data
    } catch (error) {
      console.error('Account registration failed', error)
      throw error
    }
  }
}

export const tweetService = {
  scheduleTweet: async (tweetData: any) => {
    try {
      const response = await api.post('/tweets/schedule', tweetData)
      return response.data
    } catch (error) {
      console.error('Tweet scheduling failed', error)
      throw error
    }
  }
}

export default api
