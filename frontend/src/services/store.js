import { create } from 'zustand'

const useStore = create((set) => ({
  // Session
  sessionId: localStorage.getItem('session_id') || null,
  setSessionId: (id) => {
    localStorage.setItem('session_id', id)
    set({ sessionId: id })
  },

  // API Keys
  apiKeysConfigured: {
    openrouter: false,
    notion: false,
  },
  setAPIKeysConfigured: (keys) => set({ apiKeysConfigured: keys }),

  // Template
  generatedTemplate: null,
  setGeneratedTemplate: (template) => set({ generatedTemplate: template }),

  // Loading states
  isGenerating: false,
  setIsGenerating: (loading) => set({ isGenerating: loading }),

  isImporting: false,
  setIsImporting: (loading) => set({ isImporting: loading }),
}))

export default useStore
