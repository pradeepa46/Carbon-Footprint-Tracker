import axios, { AxiosInstance, AxiosError } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiService {
  private axiosInstance: AxiosInstance

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add token to requests if available
    this.axiosInstance.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Handle response errors
    this.axiosInstance.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Clear auth data and redirect to login
          localStorage.removeItem('access_token')
          localStorage.removeItem('user_id')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  // Auth endpoints
  register(email: string, password: string, fullName: string) {
    return this.axiosInstance.post('/api/auth/register', {
      email,
      password,
      full_name: fullName,
    })
  }

  login(email: string, password: string) {
    return this.axiosInstance.post('/api/auth/login', {
      email,
      password,
    })
  }

  getCurrentUser() {
    return this.axiosInstance.get('/api/auth/me')
  }

  // Profile endpoints
  getProfile() {
    return this.axiosInstance.get('/api/profile')
  }

  updateProfile(data: any) {
    return this.axiosInstance.put('/api/profile', data)
  }

  // Emissions endpoints
  createEmission(data: any) {
    return this.axiosInstance.post('/api/emissions', data)
  }

  getEmissionHistory(skip = 0, limit = 50, category?: string) {
    return this.axiosInstance.get('/api/emissions/history', {
      params: { skip, limit, category },
    })
  }

  getEmissionBreakdown(year?: number, month?: number) {
    return this.axiosInstance.get('/api/emissions/breakdown', {
      params: { year, month },
    })
  }

  updateEmission(id: string, data: any) {
    return this.axiosInstance.put(`/api/emissions/${id}`, data)
  }

  deleteEmission(id: string) {
    return this.axiosInstance.delete(`/api/emissions/${id}`)
  }

  // Recommendations endpoints
  getRecommendations(limit = 5) {
    return this.axiosInstance.get('/api/recommendations', {
      params: { limit },
    })
  }
}

export default new ApiService()
