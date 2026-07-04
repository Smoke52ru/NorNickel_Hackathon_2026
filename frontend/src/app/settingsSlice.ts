import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import {
  DEFAULT_FILTERS,
  type SearchFilters,
} from '@/shared/types/filters'

export type ThemeMode = 'light' | 'dark'

export interface GraphPanelState {
  open: boolean
  focusedNodeId: string | null
  focusedEdgeId: string | null
}

export interface SettingsState {
  theme: ThemeMode
  filters: SearchFilters
  graphPanel: GraphPanelState
  filtersPanelOpen: boolean
}

const THEME_STORAGE_KEY = 'kickout-theme'

function loadTheme(): ThemeMode {
  if (typeof window === 'undefined') return 'light'
  const stored = localStorage.getItem(THEME_STORAGE_KEY)
  return stored === 'dark' ? 'dark' : 'light'
}

const initialState: SettingsState = {
  theme: loadTheme(),
  filters: DEFAULT_FILTERS,
  graphPanel: {
    open: false,
    focusedNodeId: null,
    focusedEdgeId: null,
  },
  filtersPanelOpen: false,
}

const settingsSlice = createSlice({
  name: 'settings',
  initialState,
  reducers: {
    setTheme(state, action: PayloadAction<ThemeMode>) {
      state.theme = action.payload
      localStorage.setItem(THEME_STORAGE_KEY, action.payload)
    },
    toggleTheme(state) {
      const next = state.theme === 'light' ? 'dark' : 'light'
      state.theme = next
      localStorage.setItem(THEME_STORAGE_KEY, next)
    },
    setFilters(state, action: PayloadAction<SearchFilters>) {
      state.filters = action.payload
    },
    resetFilters(state) {
      state.filters = DEFAULT_FILTERS
    },
    openGraphPanel(
      state,
      action: PayloadAction<{ nodeId?: string } | undefined>,
    ) {
      state.graphPanel.open = true
      state.graphPanel.focusedNodeId = action.payload?.nodeId ?? null
      state.graphPanel.focusedEdgeId = null
    },
    closeGraphPanel(state) {
      state.graphPanel.open = false
      state.graphPanel.focusedNodeId = null
      state.graphPanel.focusedEdgeId = null
    },
    setFocusedNode(state, action: PayloadAction<string | null>) {
      state.graphPanel.focusedNodeId = action.payload
    },
    openFiltersPanel(state) {
      state.filtersPanelOpen = true
    },
    closeFiltersPanel(state) {
      state.filtersPanelOpen = false
    },
  },
})

export const {
  setTheme,
  toggleTheme,
  setFilters,
  resetFilters,
  openGraphPanel,
  closeGraphPanel,
  setFocusedNode,
  openFiltersPanel,
  closeFiltersPanel,
} = settingsSlice.actions

export default settingsSlice.reducer
