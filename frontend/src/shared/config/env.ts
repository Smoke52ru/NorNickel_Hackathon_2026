function trimTrailingSlash(url: string): string {
  return url.replace(/\/+$/, '')
}

/** Базовый URL API: из VITE_API_URL или /api (dev-прокси Vite). */
export const API_BASE_URL = trimTrailingSlash(import.meta.env.VITE_API_URL || '/api')

export const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'
