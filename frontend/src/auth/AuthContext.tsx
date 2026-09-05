import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import { useMutation } from '@tanstack/react-query'

import { authApi } from '../api/auth'
import { tokenStore, type User, USER_KEY } from '../api/client'

interface AuthContextValue {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

function getStoredUser(): User | null {
  const raw = localStorage.getItem(USER_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw) as User
  } catch {
    return null
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(() => getStoredUser())
  const [isLoading, setIsLoading] = useState<boolean>(false)

  const loginMutation = useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      authApi.login(email, password),
    onSuccess: (data) => {
      tokenStore.setTokens(data.access_token, data.refresh_token)
      localStorage.setItem(USER_KEY, JSON.stringify(data.user))
      setUser(data.user)
    },
  })

  const logoutMutation = useMutation({
    mutationFn: () => authApi.logout(),
    onSettled: () => {
      tokenStore.clear()
      setUser(null)
    },
  })

  useEffect(() => {
    if (!tokenStore.getAccessToken()) return
    setIsLoading(true)
    authApi
      .getCurrentUser()
      .then((currentUser) => {
        localStorage.setItem(USER_KEY, JSON.stringify(currentUser))
        setUser(currentUser)
      })
      .catch(() => {
        tokenStore.clear()
        setUser(null)
      })
      .finally(() => setIsLoading(false))
  }, [])

  const login = useCallback(
    async (email: string, password: string) => {
      await loginMutation.mutateAsync({ email, password })
    },
    [loginMutation],
  )

  const logout = useCallback(async () => {
    if (tokenStore.getAccessToken()) {
      await logoutMutation.mutateAsync()
    } else {
      tokenStore.clear()
      setUser(null)
    }
  }, [logoutMutation])

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isAuthenticated: !!tokenStore.getAccessToken(),
      isLoading,
      login,
      logout,
    }),
    [user, isLoading, login, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}