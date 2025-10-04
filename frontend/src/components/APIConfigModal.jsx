import { useState } from 'react'
import { X, Key } from 'lucide-react'
import toast from 'react-hot-toast'
import APIClient from '../services/api'
import useStore from '../services/store'

export default function APIConfigModal({ isOpen, onClose }) {
  const [openrouterKey, setOpenrouterKey] = useState('')
  const [notionToken, setNotionToken] = useState('')
  const [aiModel, setAiModel] = useState('deepseek/deepseek-chat-v3.1:free')
  const [loading, setLoading] = useState(false)
  const { setAPIKeysConfigured, apiKeysConfigured } = useStore()

  if (!isOpen) return null

  const handleSave = async () => {
    if (!openrouterKey.trim()) {
      toast.error('OpenRouter API key is required')
      return
    }

    if (!notionToken.trim()) {
      toast.error('Notion Integration Token is required to import templates')
      return
    }

    console.log('Saving API keys...', {
      openrouterKey: openrouterKey.substring(0, 20) + '...',
      notionToken: notionToken.substring(0, 20) + '...',
      aiModel: aiModel || 'default'
    })

    setLoading(true)
    try {
      const response = await APIClient.storeAPIKeys({
        openrouter_key: openrouterKey,
        notion_token: notionToken,
        ai_model: aiModel || undefined,
      })

      console.log('Full API keys save response:', response)
      console.log('Response data:', response.data)

      setAPIKeysConfigured({
        openrouter: response.data.openrouter_configured,
        notion: response.data.notion_configured,
      })
      
      console.log('Set API keys configured to:', {
        openrouter: response.data.openrouter_configured,
        notion: response.data.notion_configured,
      })

      toast.success('API keys saved successfully')
      
      // Wait a tiny bit to ensure state updates, then close
      setTimeout(() => {
        onClose()
      }, 100)
    } catch (error) {
      console.error('Failed to save API keys:', error)
      toast.error(error.response?.data?.detail || 'Failed to save API keys')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white dark:bg-gray-800 rounded-xl max-w-md w-full p-6 shadow-2xl">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            API Configuration
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Show status if keys are configured */}
        {apiKeysConfigured.openrouter && apiKeysConfigured.notion && (
          <div className="mb-4 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
            <p className="text-sm text-green-800 dark:text-green-200 flex items-center gap-2">
              <span className="w-2 h-2 bg-green-500 rounded-full"></span>
              API keys are configured and working
            </p>
          </div>
        )}

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              OpenRouter API Key *
            </label>
            <input
              type="password"
              name="openrouter_key"
              autoComplete="off"
              value={openrouterKey}
              onChange={(e) => setOpenrouterKey(e.target.value)}
              placeholder="sk-or-v1-..."
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
            />
            <p className="text-xs text-gray-500 mt-1">
              Get your key from{' '}
              <a
                href="https://openrouter.ai/keys"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary-600 hover:underline"
              >
                openrouter.ai
              </a>
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              AI Model (Optional)
            </label>
            <input
              type="text"
              name="ai_model"
              autoComplete="off"
              value={aiModel}
              onChange={(e) => setAiModel(e.target.value)}
              placeholder="deepseek/deepseek-chat-v3.1:free"
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
            />
            <p className="text-xs text-gray-500 mt-1">
              Default: deepseek/deepseek-chat-v3.1:free (Leave empty to use default)
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Notion Integration Token *
            </label>
            <input
              type="password"
              name="notion_token"
              autoComplete="off"
              value={notionToken}
              onChange={(e) => setNotionToken(e.target.value)}
              placeholder="secret_..."
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
            />
            <p className="text-xs text-gray-500 mt-1">
              <span className="font-semibold text-amber-600 dark:text-amber-400">Required for importing templates to Notion.</span>{' '}
              Get your token from{' '}
              <a
                href="https://www.notion.so/my-integrations"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary-600 hover:underline"
              >
                notion.so/my-integrations
              </a>
            </p>
          </div>

          <button
            onClick={handleSave}
            disabled={loading}
            className="w-full bg-primary-600 hover:bg-primary-700 text-white py-3 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <Key className="w-5 h-5" />
            {loading ? 'Saving...' : 'Save API Keys'}
          </button>
        </div>
      </div>
    </div>
  )
}
