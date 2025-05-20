import axios from 'axios'

const authApi = axios.create({
  baseURL: 'http://127.0.0.1:5000/auth',
  headers: {
    'Content-Type': 'application/json',
  },
})

const dogsApi = axios.create({
  baseURL: 'http://127.0.0.1:5000/dogs',
  headers: {
    'Content-Type': 'application/json',
  },
})

const adsApi = axios.create({
  baseURL: 'http://127.0.0.1:5000/advertisements',
  headers: {
    'Content-Type': 'application/json',
  },
})

const addTokenInterceptor = (instance) => {
  instance.interceptors.request.use((config) => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  })
}

addTokenInterceptor(authApi)
addTokenInterceptor(dogsApi)
addTokenInterceptor(adsApi)

export const authPost = (url, data) => authApi.post(url, data)
export const dogsPost = (url, data, config = {}) =>
  dogsApi.request({ ...config, url, data, method: 'POST' })
export const dogsGet = (url) => dogsApi.get(url)
export const dogsPut = (url, data) => dogsApi.put(url, data)
export const dogsDelete = (url) => dogsApi.delete(url)

export const adsPost = (url, data, config = {}) =>
  adsApi.request({ ...config, url, data, method: 'POST' })
export const adsGet = (url) => adsApi.get(url)
export const adsPut = (url, data) => adsApi.put(url, data)
export const adsDelete = (url) => adsApi.delete(url)
export const adsPatch = (url, data, config = {}) =>
  adsApi.request({ ...config, url, data, method: 'PATCH' })

export default authApi
