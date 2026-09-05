import axios, { type AxiosError, type AxiosRequestConfig } from 'axios'

const ACCESS_TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'
export const USER_KEY = 'auth_user'

export const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

export const tokenStore = {
  getAccessToken: (): string | null => localStorage.getItem(ACCESS_TOKEN_KEY),
  getRefreshToken: (): string | null => localStorage.getItem(REFRESH_TOKEN_KEY),
  setTokens: (access: string, refresh: string): void => {
    localStorage.setItem(ACCESS_TOKEN_KEY, access)
    localStorage.setItem(REFRESH_TOKEN_KEY, refresh)
  },
  clear: (): void => {
    localStorage.removeItem(ACCESS_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
  },
}

interface RefreshResponse {
  access_token: string
  refresh_token: string
  user: User
}

let isRefreshing = false
let refreshQueue: Array<(token: string | null) => void> = []

apiClient.interceptors.request.use((config) => {
  const token = tokenStore.getAccessToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config as (AxiosRequestConfig & { _retry?: boolean }) | undefined
    if (!original || error.response?.status !== 401 || original._retry) {
      return Promise.reject(error)
    }
    if (original.url?.includes('/auth/refresh')) {
      tokenStore.clear()
      return Promise.reject(error)
    }

    original._retry = true

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        refreshQueue.push((token) => {
          if (token) {
            original.headers = { ...original.headers, Authorization: `Bearer ${token}` }
            resolve(apiClient(original))
          } else {
            reject(error)
          }
        })
      })
    }

    isRefreshing = true
    const refreshToken = tokenStore.getRefreshToken()

    try {
      const { data } = await apiClient.post<RefreshResponse>('/auth/refresh', {
        refresh_token: refreshToken,
      })
      tokenStore.setTokens(data.access_token, data.refresh_token)
      localStorage.setItem(USER_KEY, JSON.stringify(data.user))
      refreshQueue.forEach((cb) => cb(data.access_token))
      refreshQueue = []
      original.headers = { ...original.headers, Authorization: `Bearer ${data.access_token}` }
      return apiClient(original)
    } catch (refreshError) {
      tokenStore.clear()
      refreshQueue.forEach((cb) => cb(null))
      refreshQueue = []
      if (typeof window !== 'undefined') {
        window.location.href = '/login'
      }
      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  },
)

export interface User {
  id: string
  email: string
  first_name: string | null
  last_name: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}