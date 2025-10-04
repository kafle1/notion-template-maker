# 🚀 Notion Template Maker# 🚀 Notion Template Maker



> A modern web application for generating customized Notion templates using AI.> A modern web application for generating customized Notion templates using AI.



[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)



A beautiful, simple web application for generating customized Notion templates using AI. Create professional templates with just a few clicks using natural language descriptions.A beautiful, simple web application for generating customized Notion templates using AI. Create professional templates with just a few clicks using natural language descriptions.



## ✨ Features## ✨ Features



- 🤖 **AI-Powered Generation** - Create sophisticated Notion templates using OpenRouter AI- 🤖 **AI-Powered Generation** - Create sophisticated Notion templates using OpenRouter AI

- 🔐 **Notion Integration** - Direct integration with Notion API using Internal Integration- 🔐 **Notion Integration** - Direct integration with Notion API using Internal Integration

- 📦 **One-Click Import** - Import templates directly to your Notion workspace- 📦 **One-Click Import** - Import templates directly to your Notion workspace

- 🎨 **Modern UI** - Beautiful, responsive interface built with React and Tailwind CSS- 🎨 **Modern UI** - Beautiful, responsive interface built with React and Tailwind CSS

- ⚡ **Fast & Efficient** - Async FastAPI backend for optimal performance- ⚡ **Fast & Efficient** - Async FastAPI backend for optimal performance

- 🐳 **Docker Ready** - Full containerization support for easy deployment- 🐳 **Docker Ready** - Full containerization support for easy deployment



## 🚀 Quick Start## 🏗️ Architecture



### Prerequisites\`\`\`

┌─────────────────────────────────────────────────────────────┐

- Python 3.11+│                     Frontend (React)                         │

- Node.js 18+│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │

- OpenRouter API Key│  │  Components  │  │    Pages     │  │   Services   │      │

- Notion Internal Integration Secret│  │  (UI/UX)     │  │  (Routes)    │  │  (API/State) │      │

│  └──────────────┘  └──────────────┘  └──────────────┘      │

### Installation└─────────────────────────────────────────────────────────────┘

                            ↕ HTTP/REST

```bash┌─────────────────────────────────────────────────────────────┐

# Clone repository│                     Backend (FastAPI)                        │

git clone https://github.com/kafle1/notion-template-maker.git│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │

cd notion-template-maker│  │     API      │  │   Services   │  │    Models    │      │

│  │   (Routes)   │  │  (Business)  │  │   (Data)     │      │

# Install dependencies and start│  └──────────────┘  └──────────────┘  └──────────────┘      │

make install && make dev└─────────────────────────────────────────────────────────────┘

```                            ↕ API Calls

┌─────────────────────────────────────────────────────────────┐

**That's it!** The application will be running at:│              External Services                               │

- **Frontend**: http://localhost:5173│  ┌──────────────┐                    ┌──────────────┐       │

- **Backend**: http://localhost:8000│  │  OpenRouter  │                    │    Notion    │       │

- **API Docs**: http://localhost:8000/api/docs│  │     API      │                    │     API      │       │

│  └──────────────┘                    └──────────────┘       │

## 📋 Available Commands└─────────────────────────────────────────────────────────────┘

\`\`\`

```bash

make help              # Show all commands## 🚀 Quick Start

make install           # Install all dependencies

make dev              # Run full stack application### Prerequisites

make dev-backend      # Run only backend

make dev-frontend     # Run only frontend- Python 3.11+

make build            # Build for production- Node.js 18+

make lint             # Run code linters- OpenRouter API Key

make format           # Format code- Notion Internal Integration Secret

make clean            # Clean artifacts

make docker-up        # Start with Docker### Installation

make docker-down      # Stop Docker containers

```\`\`\`bash

# Clone repository

## 🔧 Configurationgit clone https://github.com/kafle1/notion-template-maker.git

cd notion-template-maker

### 1. Copy Environment Template

# Install dependencies and start

```bashmake install && make dev

cp .env.example .env\`\`\`

```

**That's it!** The application will be running at:

### 2. Configure API Keys- **Frontend**: http://localhost:5173

- **Backend**: http://localhost:8000

Edit `.env`:- **API Docs**: http://localhost:8000/api/docs



```env## 📋 Available Commands

# Required

OPENROUTER_API_KEY=your_openrouter_api_key_here\`\`\`bash

NOTION_INTEGRATION_SECRET=your_notion_integration_secret_heremake help              # Show all commands

make install           # Install all dependencies

# Optionalmake dev              # Run full stack application

APP_ENV=developmentmake dev-backend      # Run only backend

DEBUG=truemake dev-frontend     # Run only frontend

LOG_LEVEL=INFOmake build            # Build for production

```make lint             # Run code linters

make format           # Format code

### 3. Get API Keysmake clean            # Clean artifacts

make docker-up        # Start with Docker

#### OpenRouter API Keymake docker-down      # Stop Docker containers

\`\`\`

1. Sign up at [OpenRouter](https://openrouter.ai/)

2. Navigate to [API Keys](https://openrouter.ai/keys)## 🔧 Configuration

3. Create a new API key

4. Copy and paste into `.env`### 1. Copy Environment Template



#### Notion Internal Integration\`\`\`bash

cp .env.example .env

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)\`\`\`

2. Click **"+ New integration"**

3. Give it a name (e.g., "Template Maker")### 2. Configure API Keys

4. Select your workspace

5. Set capabilities:Edit \`.env\`:

   - ✅ Read content

   - ✅ Insert content\`\`\`env

   - ✅ Update content```env

6. Copy the **"Internal Integration Secret"**# Required

7. Paste into `.env`OPENROUTER_API_KEY=your_openrouter_api_key_here

NOTION_INTEGRATION_SECRET=your_notion_integration_secret_here

**Important**: Share your Notion pages with the integration:

- Open page in Notion → "•••" menu → "Add connections" → Select your integration# Optional

APP_ENV=development

## 🎯 UsageDEBUG=true

LOG_LEVEL=INFO

1. **Configure API Keys**```

   - Click settings icon (⚙️)\`\`\`

   - Enter OpenRouter API key

   - Enter Notion Integration Secret### 3. Get API Keys

   - Save

#### OpenRouter API Key

2. **Generate Template**

   - Select template type1. Sign up at [OpenRouter](https://openrouter.ai/)

   - Enter title and description2. Navigate to [API Keys](https://openrouter.ai/keys)

   - Choose complexity level3. Create a new API key

   - Select features4. Copy and paste into \`.env\`

   - Click "Generate Template"

#### Notion Internal Integration

3. **Import to Notion**

   - Review generated template1. Go to [Notion Integrations](https://www.notion.so/my-integrations)

   - Click "Import to Notion"2. Click **"+ New integration"**

   - Template created in your workspace3. Give it a name (e.g., "Template Maker")

4. Select your workspace

## 🤝 Contributing5. Set capabilities:

   - ✅ Read content

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.   - ✅ Insert content

   - ✅ Update content

1. Fork the repository6. Copy the **"Internal Integration Secret"**

2. Create feature branch (`git checkout -b feature/amazing-feature`)7. Paste into \`.env\`

3. Commit changes (`git commit -m 'Add amazing-feature'`)

4. Push to branch (`git push origin feature/amazing-feature`)**Important**: Share your Notion pages with the integration:

5. Open Pull Request- Open page in Notion → "•••" menu → "Add connections" → Select your integration



## 📝 License## 🐳 Docker Deployment



This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.\`\`\`bash

# Build and start

---make docker-build

make docker-up

<p align="center">

  <strong>Made with ❤️ for the Notion community</strong># View logs

</p>make docker-logs



<p align="center"># Stop

  <a href="https://github.com/kafle1/notion-template-maker">⭐ Star us on GitHub</a>make docker-down

</p>\`\`\`

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
