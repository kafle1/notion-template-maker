import { useState } from 'react'
import { FileText, Database, Upload, Download, Loader2 } from 'lucide-react'
import toast from 'react-hot-toast'
import APIClient from '../services/api'
import useStore from '../services/store'

export default function TemplatePreview() {
  const { generatedTemplate, isImporting, setIsImporting } = useStore()
  const [activeTab, setActiveTab] = useState('overview')

  if (!generatedTemplate) return null

  const { template_data, metadata } = generatedTemplate

  const handleImport = async () => {
    setIsImporting(true)
    try {
      await APIClient.importTemplate({ template_data })
      toast.success('Template imported successfully!')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to import template')
    } finally {
      setIsImporting(false)
    }
  }

  const handleDownload = () => {
    const blob = new Blob([JSON.stringify(template_data, null, 2)], {
      type: 'application/json',
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${metadata.template_type || 'template'}.json`
    a.click()
    URL.revokeObjectURL(url)
    toast.success('Template downloaded!')
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
        Template Preview
      </h2>

      <div className="flex gap-2 mb-4 border-b border-gray-200 dark:border-gray-700">
        {['overview', 'pages', 'databases'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === tab
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      <div className="mb-6">
        {activeTab === 'overview' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <div className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-primary-600" />
                <span className="font-medium">Pages</span>
              </div>
              <span className="text-2xl font-bold text-primary-600">
                {template_data.pages?.length || 0}
              </span>
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <div className="flex items-center gap-2">
                <Database className="w-5 h-5 text-primary-600" />
                <span className="font-medium">Databases</span>
              </div>
              <span className="text-2xl font-bold text-primary-600">
                {template_data.databases?.length || 0}
              </span>
            </div>
          </div>
        )}

        {activeTab === 'pages' && (
          <div className="space-y-2">
            {template_data.pages?.map((page, index) => (
              <div
                key={index}
                className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg"
              >
                <h3 className="font-medium text-gray-900 dark:text-white mb-2">
                  {page.title}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {page.content?.length || 0} content blocks
                </p>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'databases' && (
          <div className="space-y-2">
            {template_data.databases?.map((db, index) => (
              <div
                key={index}
                className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg"
              >
                <h3 className="font-medium text-gray-900 dark:text-white mb-2">
                  {db.title}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {Object.keys(db.properties || {}).length} properties
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="flex gap-2">
        <button
          onClick={handleImport}
          disabled={isImporting}
          className="flex-1 bg-primary-600 hover:bg-primary-700 text-white py-3 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {isImporting ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Importing...
            </>
          ) : (
            <>
              <Upload className="w-5 h-5" />
              Import to Notion
            </>
          )}
        </button>

        <button
          onClick={handleDownload}
          className="px-6 py-3 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg font-semibold flex items-center gap-2"
        >
          <Download className="w-5 h-5" />
          Download
        </button>
      </div>
    </div>
  )
}
