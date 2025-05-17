import axios from 'axios'

const baseURL = 'http://127.0.0.1:5000/auth'

const api = axios.create({
  baseURL: baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const post = (url, data) => api.post(url, data)

export default api
