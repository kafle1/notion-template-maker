# Quickstart Guide: Notion Template Maker

## Prerequisites
- Python 3.8 or higher
- Internet connection for API access
- OpenRouter API account and key
- Notion account with workspace access

## Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd notion-template-maker
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the project root:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
NOTION_CLIENT_ID=your_notion_client_id_here
NOTION_CLIENT_SECRET=your_notion_client_secret_here
```

## Running the Application

### Development Mode
```bash
streamlit run app.py --server.headless true --server.port 8501
```

### Production Mode
```bash
streamlit run app.py --server.headless true --server.port 8501 --server.address 0.0.0.0
```

## Usage Guide

### 1. Setup API Keys
1. Open the application in your browser
2. Enter your OpenRouter API key in the configuration panel
3. Click "Connect to Notion" and authorize the application

### 2. Generate Template
1. Select your preferred AI model from the dropdown
2. Enter detailed requirements in the text area:
   ```
   Create a project management template with:
   - Task database with status, priority, assignee
   - Timeline view for deadlines
   - Project overview page with progress tracking
   ```
3. Click "Generate Template"
4. Wait for the AI to process your requirements (may take 30-60 seconds)

### 3. Review and Import
1. Review the generated template structure in the preview panel
2. Make any necessary adjustments to the preview
3. Click "Import to Notion" to deploy the template
4. The application will create all pages, databases, and relations in your workspace

### 4. Template Management
- **Save Locally**: Download the template as JSON for backup
- **Export JSON**: Get the raw template structure
- **Generate New**: Create variations of your template

## Example Templates

### Project Management Template
```
Requirements:
Create a comprehensive project management system with:
- Main projects database with status, priority, deadline
- Tasks database linked to projects
- Team member database with roles and assignments
- Calendar view for deadlines
- Kanban board for task status
- Progress tracking with formulas
- Resource allocation page
```

### Personal Knowledge Base
```
Requirements:
Build a personal knowledge management system with:
- Notes database with tags and categories
- Daily journal template
- Book tracking database
- Idea capture system
- Project documentation pages
- Search and filter capabilities
- Archive system for old content
```

### Business CRM
```
Requirements:
Design a customer relationship management template with:
- Contacts database with company info
- Deal pipeline with stages
- Meeting notes linked to contacts
- Follow-up task automation
- Revenue tracking dashboard
- Email integration notes
- Deal history timeline
```

## Troubleshooting

### Common Issues

**Template Generation Fails**
- Check your OpenRouter API key is valid and has credits
- Ensure the selected model is available
- Try a simpler requirements description

**Notion Import Fails**
- Verify OAuth permissions are granted
- Check workspace has available space
- Ensure no duplicate page names

**Application Won't Start**
- Confirm Python 3.8+ is installed
- Check all dependencies are installed
- Verify port 8501 is not in use

**Slow Performance**
- Complex requirements take longer to process
- Large templates may take time to import
- Check your internet connection

### API Limits
- OpenRouter: 50 requests/minute, 1000/hour
- Notion: 3 requests/second
- Application implements automatic retry with backoff

## Development

### Project Structure
```
notion-template-maker/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not committed)
├── src/
│   ├── api/              # API integration modules
│   │   ├── openrouter.py
│   │   └── notion.py
│   ├── models/           # Data models
│   │   ├── template.py
│   │   └── user.py
│   ├── services/         # Business logic
│   │   ├── generator.py
│   │   └── validator.py
│   └── ui/               # UI components
│       ├── components.py
│       └── pages.py
└── tests/                # Test files
    ├── test_api.py
    ├── test_generator.py
    └── test_ui.py
```

### Running Tests
```bash
pytest tests/
```

### Adding New Features
1. Create feature branch from main
2. Implement following TDD principles
3. Add tests for new functionality
4. Update documentation
5. Submit pull request

## Support
- Check the troubleshooting section above
- Review the PRD for detailed requirements
- Examine the spec.md for implementation details
- Test with simple requirements first
