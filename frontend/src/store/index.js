import { create } from 'zustand'

export const useAuthStore = create((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,

  setUser: (user, token) => set({ user, token, isAuthenticated: !!token }),
  logout: () => set({ user: null, token: null, isAuthenticated: false }),
}))

export const useUploadStore = create((set) => ({
  currentStatement: null,
  statements: [],
  isLoading: false,

  setCurrentStatement: (statement) => set({ currentStatement: statement }),
  setStatements: (statements) => set({ statements }),
  setLoading: (loading) => set({ isLoading: loading }),
}))

export const useReportStore = create((set) => ({
  currentReport: null,
  reports: [],

  setCurrentReport: (report) => set({ currentReport: report }),
  setReports: (reports) => set({ reports }),
}))
