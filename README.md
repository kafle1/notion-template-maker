# 🚀 Notion Template Maker# 🚀 Notion Template Maker# 🚀 Notion Template Maker# Notion Template Maker



> A modern, production-ready web application for generating customized Notion templates using AI.



[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)> A modern, production-ready web application for generating customized Notion templates using AI.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)> A modern, production-ready web application for generating customized Notion templates using AI.A beautiful, simple web application for generating customized Notion templates using AI. Create professional templates with just a few clicks using natural language descriptions.

## ✨ Features

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

- 🤖 **AI-Powered Generation** - Create sophisticated Notion templates using OpenRouter AI

- 🔐 **Notion Integration** - Direct integration with Notion API using Internal Integration[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)

- 📦 **One-Click Import** - Import templates directly to your Notion workspace

- 🎨 **Modern UI** - Beautiful, responsive interface built with React and Tailwind CSS[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)

- ⚡ **Fast & Efficient** - Async FastAPI backend for optimal performance

- 🐳 **Docker Ready** - Full containerization support for easy deployment[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)![Notion Template Maker](https://img.shields.io/badge/Notion-Template%20Maker-blue?style=for-the-badge&logo=notion)



## 🏗️ Architecture## ✨ Features



```[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)![Python](https://img.shields.io/badge/Python-3.8+-green?style=flat-square&logo=python)

Frontend (React + Vite)  ←→  Backend (FastAPI)  ←→  External APIs

   ↓                              ↓                    ↓- 🤖 **AI-Powered Template Generation** - Create sophisticated Notion templates using OpenRouter AI

Components & Pages            Services & Routes     OpenRouter + Notion

```- 🔐 **Notion Integration** - Direct integration with Notion API using Internal Integration[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red?style=flat-square&logo=streamlit)



## 🚀 Quick Start- 📦 **Direct Import** - One-click import templates directly to your Notion workspace



### Prerequisites- 🎨 **Modern UI** - Beautiful, responsive interface built with React and Tailwind CSS[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)![OpenRouter](https://img.shields.io/badge/OpenRouter-API-orange?style=flat-square)



- Python 3.11+- ⚡ **Fast & Efficient** - Async FastAPI backend for optimal performance

- Node.js 18+

- OpenRouter API Key- 🐳 **Docker Ready** - Full containerization support for easy deployment

- Notion Internal Integration Secret

- 🧪 **Well Tested** - Comprehensive test suite with unit, integration, and contract tests

### Installation

## ✨ Features## ✨ Features

```bash

# Clone repository## 🏗️ Architecture

git clone https://github.com/yourusername/notion-template-maker.git

cd notion-template-maker



# Install dependencies and start```

make install && make dev

```┌─────────────────────────────────────────────────────────────┐- 🤖 **AI-Powered Template Generation** - Create sophisticated Notion templates using OpenRouter AI- 🤖 **AI-Powered Generation**: Uses advanced AI models to create custom Notion templates



**That's it!** The application will be running at:│                     Frontend (React)                         │

- **Frontend**: http://localhost:5173

- **Backend**: http://localhost:8000│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │- 🔐 **Secure OAuth Integration** - Seamless Notion workspace authentication- 🎨 **Beautiful UI**: Clean, modern interface built with Streamlit

- **API Docs**: http://localhost:8000/api/docs

│  │  Components  │  │    Pages     │  │   Services   │      │

## 📋 Available Commands

│  │  (UI/UX)     │  │  (Routes)    │  │  (API/State) │      │- 📦 **Direct Import** - One-click import templates directly to your Notion workspace- 🔐 **Secure Authentication**: OAuth integration with Notion for secure access

```bash

make help              # Show all commands│  └──────────────┘  └──────────────┘  └──────────────┘      │

make install           # Install all dependencies

make dev              # Run full stack application└─────────────────────────────────────────────────────────────┘- 🎨 **Modern UI** - Beautiful, responsive interface built with React and Tailwind CSS- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

make dev-backend      # Run only backend

make dev-frontend     # Run only frontend                            ↕ HTTP/REST

make build            # Build for production

make lint             # Run code linters┌─────────────────────────────────────────────────────────────┐- ⚡ **Fast & Efficient** - Async FastAPI backend for optimal performance- ⚡ **Fast Generation**: Optimized for <60 second template creation

make format           # Format code

make clean            # Clean artifacts│                     Backend (FastAPI)                        │

make docker-up        # Start with Docker

make docker-down      # Stop Docker containers│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │- 🐳 **Docker Ready** - Full containerization support for easy deployment- 🛡️ **Input Validation**: Comprehensive validation and sanitization

```

│  │     API      │  │   Services   │  │    Models    │      │

## 🔧 Configuration

│  │   (Routes)   │  │  (Business)  │  │   (Data)     │      │- 🧪 **Well Tested** - Comprehensive test suite with unit, integration, and contract tests- 📊 **Progress Tracking**: Real-time progress indicators during generation

### 1. Copy Environment Template

│  └──────────────┘  └──────────────┘  └──────────────┘      │

```bash

cp .env.example .env└─────────────────────────────────────────────────────────────┘- 🔄 **Session Management**: Secure session handling with encryption

```

                            ↕ API Calls

### 2. Configure API Keys

┌─────────────────────────────────────────────────────────────┐## 🏗️ Architecture- 📝 **Template Preview**: Live preview of generated templates

Edit `.env`:

│              External Services                               │

```env

# Required│  ┌──────────────┐                    ┌──────────────┐       │- 📤 **Easy Export**: Direct export to Notion workspaces

OPENROUTER_API_KEY=your_openrouter_api_key_here

NOTION_INTEGRATION_SECRET=secret_your_notion_integration_secret_here│  │  OpenRouter  │                    │    Notion    │       │



# Optional│  │     API      │                    │     API      │       │```

APP_ENV=development

DEBUG=true│  └──────────────┘                    └──────────────┘       │

LOG_LEVEL=INFO

```└─────────────────────────────────────────────────────────────┘┌─────────────────────────────────────────────────────────────┐## 🚀 Quick Start



### 3. Get API Keys```



#### OpenRouter API Key│                     Frontend (React)                         │



1. Sign up at [OpenRouter](https://openrouter.ai/)## 🚀 Quick Start

2. Navigate to [API Keys](https://openrouter.ai/keys)

3. Create a new API key│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │### Prerequisites

4. Copy and paste into `.env`

### Prerequisites

#### Notion Internal Integration

│  │  Components  │  │    Pages     │  │   Services   │      │

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)

2. Click **"+ New integration"**- Python 3.11+

3. Give it a name (e.g., "Template Maker")

4. Select your workspace- Node.js 18+│  │  (UI/UX)     │  │  (Routes)    │  │  (API/State) │      │- Python 3.8 or higher

5. Set capabilities:

   - ✅ Read content- npm or pnpm

   - ✅ Insert content

   - ✅ Update content- OpenRouter API Key│  └──────────────┘  └──────────────┘  └──────────────┘      │- A Notion account

6. Copy the **"Internal Integration Secret"**

7. Paste into `.env`- Notion Internal Integration Secret



**Important**: Share your Notion pages with the integration:└─────────────────────────────────────────────────────────────┘- An OpenRouter API key ([Get one here](https://openrouter.ai/keys))

- Open page in Notion → "•••" menu → "Add connections" → Select your integration

### One-Command Setup

## 🐳 Docker Deployment

                            ↕ HTTP/REST

```bash

# Build and start```bash

make docker-build

make docker-up# Clone repository┌─────────────────────────────────────────────────────────────┐### Installation



# View logsgit clone https://github.com/yourusername/notion-template-maker.git

make docker-logs

cd notion-template-maker│                     Backend (FastAPI)                        │

# Stop

make docker-down

```

# Install and run│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │#### Option 1: Using Makefile (Recommended)

## 📁 Project Structure

make install && make dev

```

notion-template-maker/```│  │     API      │  │   Services   │  │    Models    │      │

├── backend/                 # FastAPI backend

│   ├── main.py             # Application entry

│   ├── api/routes/         # API endpoints

│   └── DockerfileThat's it! The application will be running at:│  │   (Routes)   │  │  (Business)  │  │   (Data)     │      │```bash

├── frontend/               # React frontend

│   ├── src/- **Frontend**: http://localhost:5173

│   │   ├── components/     # UI components

│   │   ├── pages/          # Page components- **Backend**: http://localhost:8000│  └──────────────┘  └──────────────┘  └──────────────┘      │git clone https://github.com/yourusername/notion-template-maker.git

│   │   └── services/       # API & state

│   ├── Dockerfile- **API Docs**: http://localhost:8000/api/docs

│   └── nginx.conf

├── src/                    # Shared modules└─────────────────────────────────────────────────────────────┘cd notion-template-maker

│   ├── api/                # API clients

│   ├── models/             # Data models## 📋 Available Commands

│   └── services/           # Business logic

├── Makefile               # Build automation                            ↕ API Callsmake dev

├── docker-compose.yml     # Container config

└── .env.example           # Environment templateRun `make help` to see all available commands:

```

┌─────────────────────────────────────────────────────────────┐```

## 🛠️ Development

```bash

### Backend

make install        # Install all dependencies (backend + frontend)│              External Services                               │

```bash

make dev-backend           # Run backend onlymake dev           # Run full stack application

black src/ backend/        # Format code

flake8 src/ backend/       # Lint codemake build         # Build frontend for production│  ┌──────────────┐                    ┌──────────────┐       │This single command will:

```

make test          # Run all tests with coverage

### Frontend

make lint          # Run code linters (Black, Flake8, ESLint)│  │  OpenRouter  │                    │    Notion    │       │- Install all Python dependencies

```bash

make dev-frontend          # Run frontend onlymake format        # Format code automatically

cd frontend && npm run build  # Build for production

cd frontend && npm run lint   # Lint codemake clean         # Clean build artifacts and cache│  │     API      │                    │     API      │       │- Run the Streamlit application

```

make docker-up     # Start with Docker Compose

## 📚 API Documentation

make docker-down   # Stop Docker containers│  └──────────────┘                    └──────────────┘       │

Visit http://localhost:8000/api/docs for interactive API documentation.

```

### Key Endpoints

└─────────────────────────────────────────────────────────────┘#### Option 2: Manual Installation

| Endpoint | Method | Description |

|----------|--------|-------------|## 🔧 Configuration

| `/api/auth/session` | POST | Create session |

| `/api/auth/keys` | POST | Store API keys |```

| `/api/templates/generate` | POST | Generate template |

| `/api/notion/import` | POST | Import to Notion |### 1. Copy Environment Template



## 🎯 Usage1. **Clone the repository**



1. **Configure API Keys**```bash

   - Click settings icon (⚙️)

   - Enter OpenRouter API keycp .env.example .env## 🚀 Quick Start   ```bash

   - Enter Notion Integration Secret

   - Save```



2. **Generate Template**   git clone https://github.com/yourusername/notion-template-maker.git

   - Select template type

   - Enter title and description### 2. Configure API Keys

   - Choose complexity level

   - Select features### Prerequisites   cd notion-template-maker

   - Click "Generate Template"

Edit `.env` with your actual values:

3. **Import to Notion**

   - Review generated template   ```

   - Click "Import to Notion"

   - Template created in your workspace```env



## 🤝 Contributing# Required: OpenRouter API for AI generation- Python 3.11+



Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.OPENROUTER_API_KEY=your_openrouter_api_key_here



1. Fork the repository- Node.js 18+2. **Create a virtual environment**

2. Create feature branch (`git checkout -b feature/AmazingFeature`)

3. Commit changes (`git commit -m 'Add AmazingFeature'`)# Required: Notion Internal Integration Secret

4. Push to branch (`git push origin feature/AmazingFeature`)

5. Open Pull RequestNOTION_INTEGRATION_SECRET=secret_your_notion_integration_secret_here- npm or pnpm   ```bash



## 📝 License



This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.# Optional: Environment settings   python -m venv venv



## 🙏 AcknowledgmentsAPP_ENV=development



- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python frameworkDEBUG=true### One-Command Setup   source venv/bin/activate  # On Windows: venv\Scripts\activate

- [React](https://reactjs.org/) - UI library

- [Tailwind CSS](https://tailwindcss.com/) - CSS frameworkLOG_LEVEL=INFO

- [Notion API](https://developers.notion.com/) - Notion integration

- [OpenRouter](https://openrouter.ai/) - AI model routing```   ```

- [Vite](https://vitejs.dev/) - Build tool



## 📞 Support

### Getting API Keys```bash

- 🐛 [Report Issues](https://github.com/yourusername/notion-template-maker/issues)

- 💬 [Discussions](https://github.com/yourusername/notion-template-maker/discussions)

- 📧 Email: support@notiontemplate.com

#### OpenRouter API Key# Clone repository3. **Install dependencies**

## 🗺️ Roadmap



- [x] AI-powered template generation

- [x] Notion Internal Integration1. Sign up at [OpenRouter](https://openrouter.ai/)git clone https://github.com/yourusername/notion-template-maker.git   ```bash

- [x] Docker deployment

- [ ] Template marketplace2. Navigate to your [API Keys](https://openrouter.ai/keys)

- [ ] Batch generation

- [ ] Custom AI models3. Create a new API keycd notion-template-maker   pip install -r requirements.txt

- [ ] Template versioning

- [ ] Multi-language support4. Copy and paste into `.env`



## 🔒 Security   ```



See [SECURITY.md](SECURITY.md) for security practices and vulnerability reporting.#### Notion Internal Integration Secret



---# Install and run



<p align="center">1. Go to [Notion Integrations](https://www.notion.so/my-integrations)

  <strong>Made with ❤️ for the Notion community</strong>

</p>2. Click **"+ New integration"**make install && make dev4. **Set up environment variables**



<p align="center">3. Give it a name (e.g., "Template Maker")

  <a href="https://github.com/yourusername/notion-template-maker">⭐ Star us on GitHub</a>

</p>4. Select the workspace```   ```bash


5. Set capabilities:

   - ✅ Read content   cp .env.example .env

   - ✅ Insert content

   - ✅ Update contentThat's it! The application will be running at:   ```

6. Copy the **"Internal Integration Secret"**

7. Paste into `.env` file- **Frontend**: http://localhost:5173



**Important**: After creating the integration, you must **share your Notion pages/databases** with the integration:- **Backend**: http://localhost:8000   Edit `.env` with your API keys:

- Open the page in Notion

- Click the "•••" menu → "Add connections"- **API Docs**: http://localhost:8000/api/docs   ```env

- Select your integration

   OPENROUTER_API_KEY=your_openrouter_api_key_here

## 🐳 Docker Deployment

## 📋 Available Commands   NOTION_CLIENT_ID=your_notion_client_id

```bash

# Build containers   NOTION_CLIENT_SECRET=your_notion_client_secret

make docker-build

Run `make help` to see all available commands:   SECRET_KEY=your_secret_key_for_sessions

# Start application

make docker-up   ```



# View logs```bash

make docker-logs

make install        # Install all dependencies### Running the Application

# Stop application

make docker-downmake dev           # Run full stack application

```

make build         # Build frontend for production```bash

Access the application at http://localhost:5173

make test          # Run all testsstreamlit run app.py

## 📁 Project Structure

make lint          # Run code linters```

```

notion-template-maker/make format        # Format code

├── backend/                 # FastAPI backend

│   ├── main.py             # Application entry pointmake clean         # Clean build artifactsThe application will be available at `http://localhost:8501`

│   ├── api/                # API routes

│   │   └── routes/         # Endpoint definitionsmake docker-up     # Start with Docker

│   │       ├── auth.py     # Authentication routes

│   │       ├── templates.py # Template generationmake docker-down   # Stop Docker containers### Makefile Commands

│   │       └── notion.py   # Notion integration

│   └── Dockerfile          # Backend container```

├── frontend/               # React frontend

│   ├── src/The project includes a comprehensive Makefile for easy development:

│   │   ├── components/     # React components

│   │   │   ├── Header.jsx## 🔧 Configuration

│   │   │   ├── APIConfigModal.jsx

│   │   │   ├── TemplateForm.jsx```bash

│   │   │   └── TemplatePreview.jsx

│   │   ├── pages/          # Page components1. Copy the environment template:# Quick start (install + run)

│   │   │   └── HomePage.jsx

│   │   └── services/       # API client & state```bashmake dev

│   │       ├── api.js      # Axios API client

│   │       └── store.js    # Zustand state managementcp .env.example .env

│   ├── Dockerfile          # Frontend container

│   └── nginx.conf          # Production server config```# Install dependencies only

├── src/                    # Shared Python modules

│   ├── api/                # External API clientsmake install

│   │   ├── notion_client.py    # Notion API wrapper

│   │   └── openrouter_client.py # OpenRouter AI client2. Configure your API keys in `.env`:

│   ├── models/             # Data models

│   │   └── template.py     # Template data structures```env# Run the application only

│   └── services/           # Business logic

│       ├── template_generator.py   # AI generation# Requiredmake run

│       ├── template_validator.py   # Validation

│       ├── notion_import_service.py # Notion importOPENROUTER_API_KEY=your_openrouter_api_key

│       ├── session_manager.py      # Session handling

│       └── logging_service.py      # Logging utilitiesNOTION_CLIENT_ID=your_notion_client_id# Run tests

├── tests/                  # Test suite

│   ├── unit/              # Unit testsNOTION_CLIENT_SECRET=your_notion_client_secretmake test

│   ├── integration/       # Integration tests

│   └── contract/          # API contract tests

├── Makefile               # Build automation

├── docker-compose.yml     # Container orchestration# Optional# Format code

├── requirements-backend.txt # Python dependencies

└── .env.example           # Environment templateAPP_ENV=developmentmake format

```

DEBUG=true

## 🧪 Testing

LOG_LEVEL=INFO# Run linting

```bash

# Run all tests with coverage```make lint

make test



# Run specific test suites

pytest tests/unit -v              # Unit tests### Getting API Keys# Clean up cache files

pytest tests/integration -v       # Integration tests

pytest tests/contract -v          # Contract testsmake clean



# With HTML coverage report1. **OpenRouter API Key**: Sign up at [OpenRouter](https://openrouter.ai/)

pytest --cov=src --cov-report=html

open htmlcov/index.html2. **Notion OAuth**: Create an integration at [Notion Developers](https://www.notion.so/my-integrations)# Show all available commands

```

make help

## 🛠️ Development

## 🐳 Docker Deployment```

### Backend Development



```bash

# Run backend only```bash## 📖 Usage

make dev-backend

# Build and start containers

# Format Python code

black src/ backend/make docker-build### 1. Configure API Keys



# Lint Python codemake docker-up

flake8 src/ backend/ --max-line-length=88

```1. Open the application in your browser



### Frontend Development# View logs2. In the sidebar, enter your OpenRouter API key



```bashmake docker-logs3. Click "Connect with Notion OAuth" to authorize the app

# Run frontend only

make dev-frontend



# Build for production# Stop containers### 2. Create a Template

cd frontend && npm run build

make docker-down

# Lint React code

cd frontend && npm run lint```1. Fill in the template requirements:

```

   - **Title**: Name of your template

### Code Quality

## 📁 Project Structure   - **Description**: What the template is for

```bash

# Format all code   - **Sections**: Main sections to include

make format

```   - **Properties**: Custom properties for databases

# Run all linters

make lintnotion-template-maker/



# Run all checks├── backend/                 # FastAPI backend2. Click "Generate Template"

make check

```│   ├── main.py             # Application entry point



## 📚 API Documentation│   ├── api/                # API routes### 3. Preview and Export



When running the backend, visit these URLs:│   │   └── routes/         # Endpoint definitions



- **Swagger UI**: http://localhost:8000/api/docs│   └── Dockerfile          # Backend container1. Review the generated template in the preview section

- **ReDoc**: http://localhost:8000/api/redoc

- **Health Check**: http://localhost:8000/health├── frontend/               # React frontend2. Click "Export to Notion" to import it into your workspace



### Key Endpoints│   ├── src/



| Endpoint | Method | Description |│   │   ├── components/     # React components## 🏗️ Architecture

|----------|--------|-------------|

| `/api/auth/session` | POST | Create new session |│   │   ├── pages/          # Page components

| `/api/auth/keys` | POST | Store API keys |

| `/api/auth/keys/status` | GET | Check API key configuration |│   │   └── services/       # API client & state```

| `/api/templates/generate` | POST | Generate AI template |

| `/api/templates/types` | GET | Get available template types |│   ├── Dockerfile          # Frontend containersrc/

| `/api/notion/import` | POST | Import template to Notion |

| `/api/notion/workspaces` | GET | List accessible workspaces |│   └── nginx.conf          # Production server config├── api/                 # API client implementations



## 🎯 Usage Guide├── src/                    # Shared Python modules│   ├── openrouter_client.py



### 1. Configure API Keys│   ├── api/                # External API clients│   └── notion_client.py



- Click the **settings icon** in the header│   ├── models/             # Data models├── services/           # Business logic services

- Enter your **OpenRouter API key** (required)

- Enter your **Notion Integration Secret** (optional, for import)│   └── services/           # Business logic│   ├── template_generator.py

- Click **Save Configuration**

├── tests/                  # Test suite│   ├── session_manager.py

### 2. Generate Template

│   ├── unit/              # Unit tests│   ├── logging_service.py

- Select a **template type** (e.g., Project Management, Knowledge Base)

- Enter a **title** for your template│   ├── integration/       # Integration tests│   └── error_handler.py

- Add a **description** of what you need

- Choose **complexity level** (Simple, Moderate, Complex)│   └── contract/          # API contract tests├── ui/                 # UI components

- Select **features** you want included

- Click **"Generate Template"**├── Makefile               # Build automation│   ├── api_config.py



### 3. Review & Customize├── docker-compose.yml     # Container orchestration│   ├── template_input.py



- Review the generated template structure└── requirements-backend.txt # Python dependencies│   ├── template_preview.py

- Check pages, databases, and properties

- View template statistics```│   └── progress_indicator.py



### 4. Import to Notion├── models/             # Data models



- Click **"Import to Notion"** (requires Notion Integration)## 🧪 Testing│   ├── template.py

- The template will be created in your Notion workspace

- Or click **"Download JSON"** to save locally│   └── user.py



## 🤝 Contributing```bash└── utils/              # Utility functions



Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.# Run all tests    └── input_validator.py



### Development Workflowmake test```



1. Fork the repository

2. Create your feature branch (`git checkout -b feature/AmazingFeature`)

3. Make your changes# Run specific test suites## 🔧 Configuration

4. Run tests (`make test`)

5. Format code (`make format`)pytest tests/unit -v

6. Commit changes (`git commit -m 'Add some AmazingFeature'`)

7. Push to branch (`git push origin feature/AmazingFeature`)pytest tests/integration -v### Environment Variables

8. Open a Pull Request

pytest tests/contract -v

## 📝 License

| Variable | Description | Required |

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# With coverage|----------|-------------|----------|

## 🙏 Acknowledgments

pytest --cov=src --cov-report=html| `OPENROUTER_API_KEY` | Your OpenRouter API key | Yes |

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework

- [React](https://reactjs.org/) - UI library```| `NOTION_CLIENT_ID` | Notion OAuth client ID | Yes |

- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework

- [Notion API](https://developers.notion.com/) - Notion integration| `NOTION_CLIENT_SECRET` | Notion OAuth client secret | Yes |

- [OpenRouter](https://openrouter.ai/) - AI model routing

- [Vite](https://vitejs.dev/) - Frontend build tool## 🛠️ Development| `SECRET_KEY` | Secret key for session encryption | Yes |

- [Zustand](https://github.com/pmndrs/zustand) - State management

- [Framer Motion](https://www.framer.com/motion/) - Animation library| `DEBUG` | Enable debug mode | No |



## 📞 Support### Backend Development



- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/notion-template-maker/issues)### Notion Integration Setup

- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/notion-template-maker/discussions)

- 📧 **Email**: support@notiontemplate.com```bash

- 📖 **Documentation**: [Wiki](https://github.com/yourusername/notion-template-maker/wiki)

# Run backend only1. Go to [Notion Developers](https://developers.notion.com/)

## 🗺️ Roadmap

make dev-backend2. Create a new integration

- [x] AI-powered template generation

- [x] Notion Internal Integration support3. Copy the Client ID and Client Secret

- [x] Docker deployment

- [x] Comprehensive testing# Format code4. Add your redirect URI: `http://localhost:8501` (for development)

- [ ] Template marketplace

- [ ] Batch template generationblack src/ backend/

- [ ] Custom AI model selection

- [ ] Template versioning## 🧪 Testing

- [ ] Multi-language support

- [ ] Template sharing & collaboration# Run linter



## 🔒 Securityflake8 src/ backend/Run the test suite:



Please read [SECURITY.md](SECURITY.md) for security practices and reporting vulnerabilities.```



## 📊 Status```bash



![Build Status](https://img.shields.io/github/workflow/status/yourusername/notion-template-maker/CI-CD)### Frontend Development# Unit tests

![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

![Coverage](https://img.shields.io/badge/coverage-85%25-green)pytest tests/unit/

![License](https://img.shields.io/badge/license-MIT-blue)

```bash

---

# Run frontend only# Integration tests

<p align="center">

  <strong>Made with ❤️ for the Notion community</strong>make dev-frontendpytest tests/integration/

</p>



<p align="center">

  <a href="https://github.com/yourusername/notion-template-maker">⭐ Star us on GitHub</a> •# Build for production# All tests

  <a href="https://github.com/yourusername/notion-template-maker/issues">🐛 Report Bug</a> •

  <a href="https://github.com/yourusername/notion-template-maker/discussions">💡 Request Feature</a>cd frontend && npm run buildpytest

</p>

```

# Lint

cd frontend && npm run lint## 📊 Performance

```

- **Generation Time**: <60 seconds for most templates

## 📚 API Documentation- **Cache Hit Ratio**: >80% for repeated requests

- **Memory Usage**: <100MB during normal operation

When running the backend, visit http://localhost:8000/api/docs for interactive API documentation (Swagger UI).- **Concurrent Users**: Supports up to 10 simultaneous generations



### Key Endpoints## 🔒 Security



| Endpoint | Method | Description |- **Session Encryption**: All session data is encrypted using Fernet

|----------|--------|-------------|- **Input Sanitization**: All user inputs are validated and sanitized

| `/api/auth/session` | POST | Create session |- **OAuth Security**: Secure OAuth 2.0 flow with state validation

| `/api/auth/keys` | POST | Store API keys |- **API Key Protection**: Keys are never stored in plain text

| `/api/templates/generate` | POST | Generate template |- **Rate Limiting**: Built-in rate limiting for API calls

| `/api/notion/import` | POST | Import to Notion |

| `/api/oauth/callback` | GET | OAuth callback |## 🤝 Contributing



## 🎯 Usage Guide1. Fork the repository

2. Create a feature branch: `git checkout -b feature/amazing-feature`

1. **Configure API Keys**3. Commit your changes: `git commit -m 'Add amazing feature'`

   - Click settings icon in header4. Push to the branch: `git push origin feature/amazing-feature`

   - Enter your OpenRouter API key (required)5. Open a Pull Request

   - Optionally add Notion OAuth token

### Development Setup

2. **Generate Template**

   - Select template type```bash

   - Enter title and description# Install development dependencies

   - Choose complexity levelpip install -r requirements-dev.txt

   - Select features

   - Click "Generate Template"# Run linting

black .

3. **Import to Notion**flake8 .

   - Review generated template

   - Click "Import to Notion"# Run tests

   - Select workspacepytest

   - Confirm import

# Start development server with auto-reload

## 🤝 Contributingstreamlit run app.py --server.headless true

```

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 API Documentation

1. Fork the repository

2. Create your feature branch (`git checkout -b feature/AmazingFeature`)### TemplateGenerator

3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)

4. Push to the branch (`git push origin feature/AmazingFeature`)```python

5. Open a Pull Requestfrom src.services.template_generator import TemplateGenerator



### Development Guidelinesgenerator = TemplateGenerator()

template = generator.generate_template({

- Follow existing code style    'title': 'Project Management',

- Add tests for new features    'description': 'A template for managing projects',

- Update documentation as needed    'sections': ['Overview', 'Tasks', 'Timeline'],

- Ensure all tests pass before submitting PR    'properties': ['Status', 'Priority', 'Assignee']

})

## 📝 License```



This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.### NotionClient



## 🙏 Acknowledgments```python

from src.api.notion_client import NotionClient

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework

- [React](https://reactjs.org/) - UI libraryclient = NotionClient(api_key='your_notion_token')

- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS frameworkpage = client.create_page(title='New Page', content_blocks=[])

- [Notion API](https://developers.notion.com/) - Notion integration```

- [OpenRouter](https://openrouter.ai/) - AI model routing

- [Vite](https://vitejs.dev/) - Frontend build tool## 🐛 Troubleshooting

- [Zustand](https://github.com/pmndrs/zustand) - State management

### Common Issues

## 📞 Support

**"OpenRouter API key invalid"**

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/notion-template-maker/issues)- Verify your API key is correct

- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/notion-template-maker/discussions)- Check that your OpenRouter account has credits

- 📧 **Email**: support@notiontemplate.com

**"Notion OAuth failed"**

## 🗺️ Roadmap- Ensure your redirect URI is correctly set in Notion

- Check that your Notion integration has the required permissions

- [ ] Add more template types

- [ ] Support for custom AI models**"Template generation timeout"**

- [ ] Template sharing marketplace- Try simplifying your template requirements

- [ ] Batch template generation- Check your internet connection

- [ ] Advanced customization options- The app will automatically retry with optimized settings

- [ ] Template versioning

- [ ] Multi-language support**"Session expired"**

- Refresh the page and re-enter your API keys

---- Check that your browser allows cookies



<p align="center">Made with ❤️ by the Notion Template Maker team</p>### Debug Mode

<p align="center">

  <a href="https://github.com/yourusername/notion-template-maker">⭐ Star us on GitHub</a>Enable debug mode by setting `DEBUG=true` in your `.env` file for detailed logging.

</p>

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Notion](https://notion.so) for the amazing productivity platform
- [OpenRouter](https://openrouter.ai) for providing access to multiple AI models
- [Streamlit](https://streamlit.io) for the fantastic web app framework
- [Anthropic](https://anthropic.com) and [OpenAI](https://openai.com) for the AI models

## 📞 Support

- 📧 Email: support@notiontemplatemaker.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/notion-template-maker/issues)
- 📖 Docs: [Full Documentation](https://docs.notiontemplatemaker.com)

---

Made with ❤️ for the Notion community
