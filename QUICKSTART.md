# Quick Start Guide

Get up and running in 5 minutes.

## Prerequisites

- Python 3.11+
- Node.js 18+
- OpenRouter API Key
- Notion Internal Integration Secret

## Installation

```bash
# Clone repository
git clone https://github.com/kafle1/notion-template-maker.git
cd notion-template-maker

# Install and run
make install && make dev
```

## Configuration

1. **Copy environment file:**
```bash
cp .env.example .env
```

2. **Add your API keys to `.env`:**
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
NOTION_INTEGRATION_SECRET=your_notion_integration_secret_here
```

3. **Get API keys:**

**OpenRouter:** https://openrouter.ai/keys

**Notion Integration:** https://www.notion.so/my-integrations
- Create new integration
- Copy the Internal Integration Secret
- Share Notion pages with your integration

## Usage

Application runs at:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

## Docker

```bash
make docker-build
make docker-up
```

## Common Commands

```bash
make help              # Show all commands
make dev              # Run full stack
make dev-backend      # Backend only
make dev-frontend     # Frontend only
make lint             # Run linters
make format           # Format code
make clean            # Clean artifacts
```

## Troubleshooting

**Port already in use:**
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:5173 | xargs kill -9  # Frontend
```

**Module not found:**
```bash
make clean && make install
```

For more details, see [README.md](README.md).
