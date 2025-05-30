import axios from 'axios'

const BASE_URL = 'http://localhost:5000'
// const BASE_URL = 'https://85ml2msw-5000.uks1.devtunnels.ms'

const authApi = axios.create({
  baseURL: `${BASE_URL}/auth`,
  headers: {
    'Content-Type': 'application/json',
  },
})

const dogsApi = axios.create({
  baseURL: `${BASE_URL}/dogs`,
  headers: {
    'Content-Type': 'application/json',
  },
})

const adsApi = axios.create({
  baseURL: `${BASE_URL}/advertisements`,
  headers: {
    'Content-Type': 'application/json',
  },
})

const requestsApi = axios.create({
  baseURL: `${BASE_URL}/requests`,
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
addTokenInterceptor(requestsApi)

export const authPost = (url, data) => authApi.post(url, data)
export const authDelete = (url) => authApi.delete(url)
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

export const requestsPost = (url, data, config = {}) =>
  requestsApi.request({ ...config, url, data, method: 'POST' })
export const requestsGet = (url) => requestsApi.get(url)
export const requestsPatch = (url, data, config = {}) =>
  requestsApi.request({ ...config, url, data, method: 'PATCH' })

export default authApi
