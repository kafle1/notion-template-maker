import { useState, useEffect } from 'react'
import { Loader2, Sparkles } from 'lucide-react'
import toast from 'react-hot-toast'
import APIClient from '../services/api'
import useStore from '../services/store'

export default function TemplateForm() {
  const [formData, setFormData] = useState({
    template_type: 'general',
    title: 'Generated Template',
    description: '',
    features: [],
    complexity: 'medium',
    include_database: true,
    include_pages: true,
  })

  const { isGenerating, setIsGenerating, setGeneratedTemplate } = useStore()

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!formData.description.trim()) {
      toast.error('Please describe what you want the template to do')
      return
    }

    setIsGenerating(true)
    try {
      const { data } = await APIClient.generateTemplate(formData)
      setGeneratedTemplate(data)
      toast.success('Template generated successfully!')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to generate template')
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
        <Sparkles className="w-6 h-6 text-primary-600" />
        Generate Template
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            What do you want to create?
          </label>
          <textarea
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            placeholder="Describe your template requirements in detail. For example: 'Create a project management dashboard with tasks, milestones, and team members tracking'..."
            rows={6}
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white resize-none"
          />
        </div>

        <button
          type="submit"
          disabled={isGenerating}
          className="w-full bg-primary-600 hover:bg-primary-700 text-white py-3 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {isGenerating ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Generating Your Template...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              Generate Template
            </>
          )}
        </button>
      </form>
    </div>
  )
}
