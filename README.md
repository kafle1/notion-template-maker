# 🚀 Notion Template Maker

> A modern, production-ready web application for generating customized Notion templates using AI.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)

A beautiful, simple web application for generating customized Notion templates using AI. Create professional templates with just a few clicks using natural language descriptions.

## ✨ Features

- 🤖 **AI-Powered Generation** - Create sophisticated Notion templates using OpenRouter AI
- 🔐 **Notion Integration** - Direct integration with Notion API using Internal Integration
- 📦 **One-Click Import** - Import templates directly to your Notion workspace
- 🎨 **Modern UI** - Beautiful, responsive interface built with React and Tailwind CSS
- ⚡ **Fast & Efficient** - Async FastAPI backend for optimal performance
- 🐳 **Docker Ready** - Full containerization support for easy deployment

## 🏗️ Architecture

\`\`\`
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Components  │  │    Pages     │  │   Services   │      │
│  │  (UI/UX)     │  │  (Routes)    │  │  (API/State) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │     API      │  │   Services   │  │    Models    │      │
│  │   (Routes)   │  │  (Business)  │  │   (Data)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↕ API Calls
┌─────────────────────────────────────────────────────────────┐
│              External Services                               │
│  ┌──────────────┐                    ┌──────────────┐       │
│  │  OpenRouter  │                    │    Notion    │       │
│  │     API      │                    │     API      │       │
│  └──────────────┘                    └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
\`\`\`

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenRouter API Key
- Notion Internal Integration Secret

### Installation

\`\`\`bash
# Clone repository
git clone https://github.com/kafle1/notion-template-maker.git
cd notion-template-maker

# Install dependencies and start
make install && make dev
\`\`\`

**That's it!** The application will be running at:
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

## 📋 Available Commands

\`\`\`bash
make help              # Show all commands
make install           # Install all dependencies
make dev              # Run full stack application
make dev-backend      # Run only backend
make dev-frontend     # Run only frontend
make build            # Build for production
make lint             # Run code linters
make format           # Format code
make clean            # Clean artifacts
make docker-up        # Start with Docker
make docker-down      # Stop Docker containers
\`\`\`

## 🔧 Configuration

### 1. Copy Environment Template

\`\`\`bash
cp .env.example .env
\`\`\`

### 2. Configure API Keys

Edit \`.env\`:

\`\`\`env
# Required
OPENROUTER_API_KEY=your_openrouter_api_key_here
NOTION_INTEGRATION_SECRET=secret_your_notion_integration_secret_here

# Optional
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO
\`\`\`

### 3. Get API Keys

#### OpenRouter API Key

1. Sign up at [OpenRouter](https://openrouter.ai/)
2. Navigate to [API Keys](https://openrouter.ai/keys)
3. Create a new API key
4. Copy and paste into \`.env\`

#### Notion Internal Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Click **"+ New integration"**
3. Give it a name (e.g., "Template Maker")
4. Select your workspace
5. Set capabilities:
   - ✅ Read content
   - ✅ Insert content
   - ✅ Update content
6. Copy the **"Internal Integration Secret"**
7. Paste into \`.env\`

**Important**: Share your Notion pages with the integration:
- Open page in Notion → "•••" menu → "Add connections" → Select your integration

## 🐳 Docker Deployment

\`\`\`bash
# Build and start
make docker-build
make docker-up

# View logs
make docker-logs

# Stop
make docker-down
\`\`\`

## 📁 Project Structure

\`\`\`
notion-template-maker/
├── backend/                 # FastAPI backend
│   ├── main.py             # Application entry
│   ├── api/routes/         # API endpoints
│   ├── clients/            # External API clients
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── pages/          # Page components
│   │   └── services/       # API & state
│   ├── Dockerfile
│   └── nginx.conf
├── Makefile               # Build automation
├── docker-compose.yml     # Container config
└── .env.example           # Environment template
\`\`\`

## 🛠️ Development

### Backend

\`\`\`bash
make dev-backend           # Run backend only
black backend/             # Format code
flake8 backend/            # Lint code
\`\`\`

### Frontend

\`\`\`bash
make dev-frontend          # Run frontend only
cd frontend && npm run build  # Build for production
cd frontend && npm run lint   # Lint code
\`\`\`

## 📚 API Documentation

Visit http://localhost:8000/api/docs for interactive API documentation.

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| \`/api/auth/session\` | POST | Create session |
| \`/api/auth/keys\` | POST | Store API keys |
| \`/api/templates/generate\` | POST | Generate template |
| \`/api/notion/import\` | POST | Import to Notion |

## 🎯 Usage

1. **Configure API Keys**
   - Click settings icon (⚙️)
   - Enter OpenRouter API key
   - Enter Notion Integration Secret
   - Save

2. **Generate Template**
   - Select template type
   - Enter title and description
   - Choose complexity level
   - Select features
   - Click "Generate Template"

3. **Import to Notion**
   - Review generated template
   - Click "Import to Notion"
   - Template created in your workspace

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create feature branch (\`git checkout -b feature/AmazingFeature\`)
3. Commit changes (\`git commit -m 'Add AmazingFeature'\`)
4. Push to branch (\`git push origin feature/AmazingFeature\`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python framework
- [React](https://reactjs.org/) - UI library
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
- [Notion API](https://developers.notion.com/) - Notion integration
- [OpenRouter](https://openrouter.ai/) - AI model routing
- [Vite](https://vitejs.dev/) - Build tool

## 📞 Support

- 🐛 [Report Issues](https://github.com/kafle1/notion-template-maker/issues)
- 💬 [Discussions](https://github.com/kafle1/notion-template-maker/discussions)
- 📧 Email: support@notiontemplate.com

## 🗺️ Roadmap

- [x] AI-powered template generation
- [x] Notion Internal Integration
- [x] Docker deployment
- [ ] Template marketplace
- [ ] Batch generation
- [ ] Custom AI models
- [ ] Template versioning
- [ ] Multi-language support

## 🔒 Security

See [SECURITY.md](SECURITY.md) for security practices and vulnerability reporting.

---

<p align="center">
  <strong>Made with ❤️ for the Notion community</strong>
</p>

<p align="center">
  <a href="https://github.com/kafle1/notion-template-maker">⭐ Star us on GitHub</a>
</p>
