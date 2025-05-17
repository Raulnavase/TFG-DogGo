import axios from 'axios'

const baseURL = 'http://127.0.0.1:5000/auth'

const api = axios.create({
  baseURL: baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const post = (url, data) => api.post(url, data)
export const get = (url) => api.get(url)

export default api
