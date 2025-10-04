import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, Settings } from 'lucide-react'
import toast from 'react-hot-toast'
import APIClient from '../services/api'
import useStore from '../services/store'
import Header from '../components/Header'
import APIConfigModal from '../components/APIConfigModal'
import TemplateForm from '../components/TemplateForm'
import TemplatePreview from '../components/TemplatePreview'

export default function HomePage() {
  const [showConfigModal, setShowConfigModal] = useState(false)
  const {
    sessionId,
    setSessionId,
    apiKeysConfigured,
    setAPIKeysConfigured,
    generatedTemplate,
    isGenerating,
  } = useStore()

  useEffect(() => {
    initializeSession()
  }, [])

  useEffect(() => {
    console.log('apiKeysConfigured changed:', apiKeysConfigured)
  }, [apiKeysConfigured])

  const initializeSession = async () => {
    try {
      if (!sessionId) {
        console.log('Creating new session...')
        const { session_id } = await APIClient.createSession()
        console.log('Session created:', session_id)
        setSessionId(session_id)
      } else {
        console.log('Using existing session:', sessionId)
      }
      
      // Always check keys status
      try {
        console.log('Checking keys status...')
        const { data } = await APIClient.getKeysStatus()
        console.log('Keys status:', data)
        setAPIKeysConfigured({
          openrouter: data.openrouter_configured,
          notion: data.notion_configured,
        })
      } catch (error) {
        console.error('Failed to check keys status:', error)
      }
    } catch (error) {
      console.error('Session initialization failed:', error)
      toast.error('Failed to initialize session')
    }
  }

  const handleOpenConfig = () => {
    setShowConfigModal(true)
  }

  const handleCloseConfig = async () => {
    setShowConfigModal(false)
    // Re-check keys status after closing modal
    try {
      console.log('Re-checking keys status after modal close...')
      const { data } = await APIClient.getKeysStatus()
      console.log('Keys status after close:', data)
      setAPIKeysConfigured({
        openrouter: data.openrouter_configured,
        notion: data.notion_configured,
      })
      console.log('State updated with:', {
        openrouter: data.openrouter_configured,
        notion: data.notion_configured,
      })
    } catch (error) {
      console.error('Failed to check keys status:', error)
    }
  }

  return (
    <div className="min-h-screen">
      <Header onOpenConfig={handleOpenConfig} apiKeysConfigured={apiKeysConfigured} />

      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Hero Section */}
        {!generatedTemplate && !apiKeysConfigured.openrouter && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-12"
          >
            <div className="flex justify-center mb-6">
              <div className="relative">
                <div className="absolute inset-0 bg-primary-500 blur-3xl opacity-20 rounded-full" />
                <Sparkles className="w-20 h-20 text-primary-600 relative" />
              </div>
            </div>

            <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
              AI-Powered Notion Templates
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
              Generate beautiful, customized Notion templates in seconds using advanced AI.
              No manual setup required.
            </p>

            <button
              onClick={handleOpenConfig}
              className="bg-primary-600 hover:bg-primary-700 text-white px-8 py-4 rounded-lg text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200 flex items-center gap-2 mx-auto"
            >
              <Settings className="w-5 h-5" />
              Get Started
            </button>
          </motion.div>
        )}

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Template Form */}
          {apiKeysConfigured.openrouter && (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <TemplateForm />
            </motion.div>
          )}

          {/* Template Preview */}
          {generatedTemplate && (
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <TemplatePreview />
            </motion.div>
          )}
        </div>
      </main>

      {/* API Config Modal */}
      <APIConfigModal
        isOpen={showConfigModal}
        onClose={handleCloseConfig}
      />
    </div>
  )
}
