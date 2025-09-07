# Notion Template Maker

A beautiful, simple web application for generating customized Notion templates using AI. Create professional templates with just a few clicks using natural language descriptions.

![Notion Template Maker](https://img.shields.io/badge/Notion-Template%20Maker-blue?style=for-the-badge&logo=notion)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red?style=flat-square&logo=streamlit)
![OpenRouter](https://img.shields.io/badge/OpenRouter-API-orange?style=flat-square)

## ✨ Features

- 🤖 **AI-Powered Generation**: Uses advanced AI models to create custom Notion templates
- 🎨 **Beautiful UI**: Clean, modern interface built with Streamlit
- 🔐 **Secure Authentication**: OAuth integration with Notion for secure access
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- ⚡ **Fast Generation**: Optimized for <60 second template creation
- 🛡️ **Input Validation**: Comprehensive validation and sanitization
- 📊 **Progress Tracking**: Real-time progress indicators during generation
- 🔄 **Session Management**: Secure session handling with encryption
- 📝 **Template Preview**: Live preview of generated templates
- 📤 **Easy Export**: Direct export to Notion workspaces

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A Notion account
- An OpenRouter API key ([Get one here](https://openrouter.ai/keys))

### Installation

#### Option 1: Using Makefile (Recommended)

```bash
git clone https://github.com/yourusername/notion-template-maker.git
cd notion-template-maker
make dev
```

This single command will:
- Install all Python dependencies
- Run the Streamlit application

#### Option 2: Manual Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/notion-template-maker.git
   cd notion-template-maker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your API keys:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   NOTION_CLIENT_ID=your_notion_client_id
   NOTION_CLIENT_SECRET=your_notion_client_secret
   SECRET_KEY=your_secret_key_for_sessions
   ```

### Running the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### Makefile Commands

The project includes a comprehensive Makefile for easy development:

```bash
# Quick start (install + run)
make dev

# Install dependencies only
make install

# Run the application only
make run

# Run tests
make test

# Format code
make format

# Run linting
make lint

# Clean up cache files
make clean

# Show all available commands
make help
```

## 📖 Usage

### 1. Configure API Keys

1. Open the application in your browser
2. In the sidebar, enter your OpenRouter API key
3. Click "Connect with Notion OAuth" to authorize the app

### 2. Create a Template

1. Fill in the template requirements:
   - **Title**: Name of your template
   - **Description**: What the template is for
   - **Sections**: Main sections to include
   - **Properties**: Custom properties for databases

2. Click "Generate Template"

### 3. Preview and Export

1. Review the generated template in the preview section
2. Click "Export to Notion" to import it into your workspace

## 🏗️ Architecture

```
src/
├── api/                 # API client implementations
│   ├── openrouter_client.py
│   └── notion_client.py
├── services/           # Business logic services
│   ├── template_generator.py
│   ├── session_manager.py
│   ├── logging_service.py
│   └── error_handler.py
├── ui/                 # UI components
│   ├── api_config.py
│   ├── template_input.py
│   ├── template_preview.py
│   └── progress_indicator.py
├── models/             # Data models
│   ├── template.py
│   └── user.py
└── utils/              # Utility functions
    └── input_validator.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | Yes |
| `NOTION_CLIENT_ID` | Notion OAuth client ID | Yes |
| `NOTION_CLIENT_SECRET` | Notion OAuth client secret | Yes |
| `SECRET_KEY` | Secret key for session encryption | Yes |
| `DEBUG` | Enable debug mode | No |

### Notion Integration Setup

1. Go to [Notion Developers](https://developers.notion.com/)
2. Create a new integration
3. Copy the Client ID and Client Secret
4. Add your redirect URI: `http://localhost:8501` (for development)

## 🧪 Testing

Run the test suite:

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# All tests
pytest
```

## 📊 Performance

- **Generation Time**: <60 seconds for most templates
- **Cache Hit Ratio**: >80% for repeated requests
- **Memory Usage**: <100MB during normal operation
- **Concurrent Users**: Supports up to 10 simultaneous generations

## 🔒 Security

- **Session Encryption**: All session data is encrypted using Fernet
- **Input Sanitization**: All user inputs are validated and sanitized
- **OAuth Security**: Secure OAuth 2.0 flow with state validation
- **API Key Protection**: Keys are never stored in plain text
- **Rate Limiting**: Built-in rate limiting for API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
black .
flake8 .

# Run tests
pytest

# Start development server with auto-reload
streamlit run app.py --server.headless true
```

## 📝 API Documentation

### TemplateGenerator

```python
from src.services.template_generator import TemplateGenerator

generator = TemplateGenerator()
template = generator.generate_template({
    'title': 'Project Management',
    'description': 'A template for managing projects',
    'sections': ['Overview', 'Tasks', 'Timeline'],
    'properties': ['Status', 'Priority', 'Assignee']
})
```

### NotionClient

```python
from src.api.notion_client import NotionClient

client = NotionClient(api_key='your_notion_token')
page = client.create_page(title='New Page', content_blocks=[])
```

## 🐛 Troubleshooting

### Common Issues

**"OpenRouter API key invalid"**
- Verify your API key is correct
- Check that your OpenRouter account has credits

**"Notion OAuth failed"**
- Ensure your redirect URI is correctly set in Notion
- Check that your Notion integration has the required permissions

**"Template generation timeout"**
- Try simplifying your template requirements
- Check your internet connection
- The app will automatically retry with optimized settings

**"Session expired"**
- Refresh the page and re-enter your API keys
- Check that your browser allows cookies

### Debug Mode

Enable debug mode by setting `DEBUG=true` in your `.env` file for detailed logging.

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
