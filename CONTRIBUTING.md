# Contributing to Notion Template Maker

First off, thank you for considering contributing to Notion Template Maker! It's people like you that make this tool great.

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## 🚀 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if applicable**
- **Include your environment details** (OS, Python version, Node version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any similar features in other applications**

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** if you've added code that should be tested
4. **Ensure the test suite passes** (`make test`)
5. **Format your code** (`make format`)
6. **Run linters** (`make lint`)
7. **Write a good commit message**

## 📝 Development Process

### Setup Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/notion-template-maker.git
cd notion-template-maker

# Install dependencies
make install

# Run development server
make dev
```

### Project Structure

```
notion-template-maker/
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── src/             # Shared Python modules
├── tests/           # Test suite
└── docs/            # Documentation
```

### Coding Standards

#### Python (Backend)
- Follow PEP 8 style guide
- Use type hints
- Maximum line length: 88 characters (Black default)
- Docstrings for all public functions/classes

```python
def generate_template(title: str, description: str) -> Template:
    """Generate a Notion template based on input.
    
    Args:
        title: The template title
        description: Detailed description of template needs
        
    Returns:
        Template: The generated template object
        
    Raises:
        ValidationError: If input is invalid
    """
    pass
```

#### JavaScript/React (Frontend)
- Use functional components with hooks
- Follow ESLint configuration
- Use meaningful variable names
- Add PropTypes or TypeScript types

```jsx
const TemplateCard = ({ template, onImport }) => {
  // Component logic
  return (
    <div className="template-card">
      {/* JSX */}
    </div>
  );
};
```

#### General Guidelines
- Keep functions small and focused
- Write self-documenting code
- Add comments for complex logic
- Avoid premature optimization
- Use meaningful commit messages

### Testing

```bash
# Run all tests
make test

# Run specific test types
pytest tests/unit -v
pytest tests/integration -v
pytest tests/contract -v

# Run with coverage
pytest --cov=src --cov-report=html
```

#### Writing Tests
- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

```python
def test_template_generation_with_valid_input():
    # Arrange
    generator = TemplateGenerator()
    title = "Project Management"
    
    # Act
    result = generator.generate(title)
    
    # Assert
    assert result.title == title
    assert len(result.pages) > 0
```

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
feat: add template type selector
fix: resolve OAuth callback issue
docs: update API documentation
style: format code with black
refactor: simplify template validator
test: add integration tests for import
chore: update dependencies
```

### Branch Naming

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation only
- `refactor/` - Code refactoring
- `test/` - Adding or updating tests

Example: `feature/add-template-sharing`

## 🏗️ Architecture Guidelines

### Backend (FastAPI)
- Keep routes thin, logic in services
- Use dependency injection
- Validate input with Pydantic models
- Handle errors gracefully
- Use async/await for I/O operations

### Frontend (React)
- One component per file
- Keep components small and reusable
- Use custom hooks for shared logic
- Manage state with Zustand
- Follow atomic design principles

### Database/Models
- Use Pydantic for data validation
- Keep models simple and focused
- Add helpful error messages
- Document model fields

## 📚 Documentation

- Update README.md for user-facing changes
- Add docstrings to all public APIs
- Update API documentation for endpoint changes
- Include examples in documentation
- Keep CHANGELOG.md up to date

## 🐛 Debugging Tips

### Backend Debugging
```bash
# Run with debug logging
LOG_LEVEL=DEBUG make dev-backend

# Use pdb for debugging
import pdb; pdb.set_trace()
```

### Frontend Debugging
```bash
# Run with debug output
make dev-frontend

# Use browser DevTools
# Add debugger statements in code
```

## 📦 Release Process

1. Update version in `pyproject.toml` and `package.json`
2. Update CHANGELOG.md
3. Create a pull request to `main`
4. After merge, create a GitHub release
5. Tag follows semantic versioning: `v2.1.0`

## ❓ Questions?

- Open a [GitHub Discussion](https://github.com/yourusername/notion-template-maker/discussions)
- Check existing [Issues](https://github.com/yourusername/notion-template-maker/issues)
- Read the [Documentation](https://github.com/yourusername/notion-template-maker/wiki)

## 🎉 Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Credited in the README (for significant contributions)

Thank you for contributing! 🙌
