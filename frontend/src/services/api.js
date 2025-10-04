import axios from 'axios'

const API_BASE_URL = '/api'

class APIClient {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add session ID to requests
    this.client.interceptors.request.use((config) => {
      const sessionId = localStorage.getItem('session_id')
      if (sessionId) {
        config.headers['X-Session-ID'] = sessionId
      }
      return config
    })
  }

  // Auth endpoints
  async createSession() {
    const response = await this.client.post('/auth/session')
    const { session_id } = response.data
    localStorage.setItem('session_id', session_id)
    return response.data
  }

  async storeAPIKeys(keys) {
    return this.client.post('/auth/keys', keys)
  }

  async getKeysStatus() {
    return this.client.get('/auth/keys/status')
  }

  // Template endpoints
  async generateTemplate(templateData) {
    return this.client.post('/templates/generate', templateData)
  }

  async getTemplateTypes() {
    return this.client.get('/templates/types')
  }

  async getFeatures() {
    return this.client.get('/templates/features')
  }

  // Notion endpoints
  async initOAuth(data) {
    return this.client.post('/notion/oauth/init', data)
  }

  async importTemplate(data) {
    return this.client.post('/notion/import', data)
  }

  async listWorkspaces() {
    return this.client.get('/notion/workspaces')
  }
}

export default new APIClient()
