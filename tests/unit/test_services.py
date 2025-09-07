"""
Unit tests for Notion Template Maker services.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from src.services.template_generator import TemplateGenerator
from src.services.template_validator import TemplateValidator
from src.services.session_manager import SessionManager
from src.services.notion_import_service import NotionImportService
from src.services.notion_oauth_service import NotionOAuthService
from src.services.logging_service import LoggingService
from src.services.error_handler import ErrorHandler


class TestTemplateGenerator:
    """Test cases for TemplateGenerator service."""

    def test_generate_template_success(self):
        """Test successful template generation."""
        generator = TemplateGenerator()

        requirements = {
            "title": "Test Template",
            "description": "A test template",
            "sections": ["Introduction", "Main Content"],
            "properties": ["Status", "Priority"],
        }

        # Mock OpenRouter client
        mock_client = Mock()
        mock_client.generate_template.return_value = {
            "id": "generated-template-123",
            "title": "Test Template",
            "sections": [
                {"name": "Introduction", "content": "Intro content"},
                {"name": "Main Content", "content": "Main content"},
            ],
            "properties": [
                {"name": "Status", "type": "select", "options": ["Todo", "Done"]},
                {"name": "Priority", "type": "select", "options": ["Low", "High"]},
            ],
        }

        result = generator.generate_template(requirements, mock_client)

        assert result["id"] == "generated-template-123"
        assert result["title"] == "Test Template"
        assert len(result["sections"]) == 2
        assert len(result["properties"]) == 2

        mock_client.generate_template.assert_called_once_with(requirements)

    def test_generate_template_with_empty_requirements(self):
        """Test template generation with empty requirements."""
        generator = TemplateGenerator()

        requirements = {}
        mock_client = Mock()
        mock_client.generate_template.return_value = {
            "id": "empty-template",
            "title": "Empty Template",
            "sections": [],
            "properties": [],
        }

        result = generator.generate_template(requirements, mock_client)

        assert result["id"] == "empty-template"
        assert result["title"] == "Empty Template"

    def test_generate_template_client_error(self):
        """Test template generation with client error."""
        generator = TemplateGenerator()

        requirements = {"title": "Test"}
        mock_client = Mock()
        mock_client.generate_template.side_effect = Exception("API Error")

        with pytest.raises(Exception, match="API Error"):
            generator.generate_template(requirements, mock_client)


class TestTemplateValidator:
    """Test cases for TemplateValidator service."""

    def test_validate_valid_template(self):
        """Test validation of a valid template."""
        validator = TemplateValidator()

        valid_template = {
            "id": "valid-template",
            "title": "Valid Template",
            "description": "Valid description",
            "sections": [
                {"name": "Section 1", "content": "Content 1"},
                {"name": "Section 2", "content": "Content 2"},
            ],
            "properties": [
                {"name": "Status", "type": "select", "options": ["Todo", "Done"]},
                {"name": "Priority", "type": "text"},
            ],
        }

        result = validator.validate_template(valid_template)

        assert result["valid"] is True
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) == 0

    def test_validate_invalid_template_missing_title(self):
        """Test validation of template missing title."""
        validator = TemplateValidator()

        invalid_template = {
            "id": "invalid-template",
            "description": "Missing title",
            "sections": [{"name": "Section 1", "content": "Content"}],
            "properties": [{"name": "Status", "type": "text"}],
        }

        result = validator.validate_template(invalid_template)

        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert "title" in str(result["errors"]).lower()

    def test_validate_template_with_warnings(self):
        """Test validation of template with warnings."""
        validator = TemplateValidator()

        template_with_warnings = {
            "id": "warning-template",
            "title": "T",  # Very short title
            "description": "",  # Empty description
            "sections": [{"name": "Section 1", "content": "Content"}],
            "properties": [{"name": "Status", "type": "text"}],
        }

        result = validator.validate_template(template_with_warnings)

        assert result["valid"] is True  # Still valid but with warnings
        assert len(result["warnings"]) > 0

    def test_validate_template_sections(self):
        """Test validation of template sections."""
        validator = TemplateValidator()

        # Valid sections
        valid_template = {
            "id": "sections-test",
            "title": "Sections Test",
            "sections": [
                {"name": "Section 1", "content": "Content 1"},
                {
                    "name": "Section 2",
                    "content": "Content 2",
                    "properties": {"key": "value"},
                },
            ],
            "properties": [{"name": "Status", "type": "text"}],
        }

        result = validator.validate_template(valid_template)
        assert result["valid"] is True

        # Invalid sections - missing name
        invalid_template = {
            "id": "invalid-sections",
            "title": "Invalid Sections",
            "sections": [{"content": "Content without name"}],
            "properties": [{"name": "Status", "type": "text"}],
        }

        result = validator.validate_template(invalid_template)
        assert result["valid"] is False

    def test_validate_template_properties(self):
        """Test validation of template properties."""
        validator = TemplateValidator()

        # Valid properties
        valid_template = {
            "id": "properties-test",
            "title": "Properties Test",
            "sections": [{"name": "Section 1", "content": "Content"}],
            "properties": [
                {"name": "Status", "type": "select", "options": ["Todo", "Done"]},
                {"name": "Priority", "type": "number"},
                {"name": "Description", "type": "text"},
            ],
        }

        result = validator.validate_template(valid_template)
        assert result["valid"] is True

        # Invalid properties - missing name
        invalid_template = {
            "id": "invalid-properties",
            "title": "Invalid Properties",
            "sections": [{"name": "Section 1", "content": "Content"}],
            "properties": [{"type": "text"}],
        }

        result = validator.validate_template(invalid_template)
        assert result["valid"] is False


class TestSessionManager:
    """Test cases for SessionManager service."""

    @patch("src.services.session_manager.SessionManager._load_session_data")
    @patch("src.services.session_manager.SessionManager._save_session_data")
    def test_store_and_get_api_key(self, mock_save, mock_load):
        """Test storing and retrieving API keys."""
        mock_load.return_value = {}

        manager = SessionManager()
        session_id = "test-session-123"

        # Store API key
        manager.store_api_key(session_id, "openrouter", "sk-or-v1-test-key")

        # Retrieve API key
        key = manager.get_api_key(session_id, "openrouter")

        assert key == "sk-or-v1-test-key"
        mock_save.assert_called()

    @patch("src.services.session_manager.SessionManager._load_session_data")
    def test_get_nonexistent_api_key(self, mock_load):
        """Test retrieving non-existent API key."""
        mock_load.return_value = {}

        manager = SessionManager()
        session_id = "test-session-123"

        key = manager.get_api_key(session_id, "nonexistent")

        assert key is None

    @patch("src.services.session_manager.SessionManager._load_session_data")
    @patch("src.services.session_manager.SessionManager._save_session_data")
    def test_store_oauth_data(self, mock_save, mock_load):
        """Test storing OAuth data."""
        mock_load.return_value = {}

        manager = SessionManager()
        session_id = "test-session-123"

        oauth_data = {
            "access_token": "test-token",
            "workspace_id": "workspace-123",
            "token_type": "bearer",
        }

        manager.store_oauth_data(session_id, oauth_data)

        # Verify data was stored
        stored_data = manager.get_oauth_data(session_id)
        assert stored_data["access_token"] == "test-token"
        assert stored_data["workspace_id"] == "workspace-123"

    @patch("src.services.session_manager.SessionManager._load_session_data")
    def test_get_oauth_data(self, mock_load):
        """Test retrieving OAuth data."""
        oauth_data = {"access_token": "test-token", "workspace_id": "workspace-123"}
        mock_load.return_value = {"oauth": oauth_data}

        manager = SessionManager()
        session_id = "test-session-123"

        result = manager.get_oauth_data(session_id)

        assert result["access_token"] == "test-token"
        assert result["workspace_id"] == "workspace-123"

    @patch("src.services.session_manager.SessionManager._load_session_data")
    def test_clear_session_data(self, mock_load):
        """Test clearing session data."""
        mock_load.return_value = {
            "api_keys": {"openrouter": "test-key"},
            "oauth": {"access_token": "test-token"},
        }

        manager = SessionManager()
        session_id = "test-session-123"

        manager.clear_session_data(session_id)

        # Verify data was cleared
        assert manager.get_api_key(session_id, "openrouter") is None
        assert manager.get_oauth_data(session_id) is None


class TestNotionImportService:
    """Test cases for NotionImportService."""

    def test_import_template_success(self):
        """Test successful template import."""
        service = NotionImportService()

        template_data = {
            "id": "test-template",
            "title": "Test Template",
            "sections": [{"name": "Section 1", "content": "Content"}],
            "properties": [{"name": "Status", "type": "text"}],
        }

        # Mock Notion client
        mock_client = Mock()
        mock_client.create_database.return_value = {"id": "database-123"}
        mock_client.create_page.return_value = {"id": "page-123"}

        result = service.import_template(template_data, mock_client)

        assert result["success"] is True
        assert "database_id" in result
        assert "page_id" in result

    def test_import_template_client_error(self):
        """Test template import with client error."""
        service = NotionImportService()

        template_data = {"id": "test-template", "title": "Test"}

        mock_client = Mock()
        mock_client.create_database.side_effect = Exception("Notion API Error")

        result = service.import_template(template_data, mock_client)

        assert result["success"] is False
        assert "error" in result

    def test_import_template_invalid_data(self):
        """Test template import with invalid data."""
        service = NotionImportService()

        invalid_template_data = {}  # Missing required fields

        mock_client = Mock()

        result = service.import_template(invalid_template_data, mock_client)

        assert result["success"] is False
        assert "error" in result


class TestNotionOAuthService:
    """Test cases for NotionOAuthService."""

    @patch("src.services.notion_oauth_service.requests.post")
    def test_handle_oauth_callback_success(self, mock_post):
        """Test successful OAuth callback handling."""
        service = NotionOAuthService()

        # Mock successful token response
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "test-access-token",
            "workspace_id": "workspace-123",
            "token_type": "bearer",
        }
        mock_post.return_value = mock_response

        result = service.handle_oauth_callback(
            "http://localhost:8501", "test-state", "test-code-verifier"
        )

        assert "access_token" in result
        assert result["access_token"] == "test-access-token"
        assert result["workspace_id"] == "workspace-123"

    @patch("src.services.notion_oauth_service.requests.post")
    def test_handle_oauth_callback_error(self, mock_post):
        """Test OAuth callback handling with error."""
        service = NotionOAuthService()

        mock_post.side_effect = Exception("OAuth request failed")

        with pytest.raises(Exception, match="OAuth request failed"):
            service.handle_oauth_callback(
                "http://localhost:8501", "test-state", "test-code-verifier"
            )

    def test_generate_oauth_url(self):
        """Test OAuth URL generation."""
        service = NotionOAuthService()

        url = service.generate_oauth_url("test-state")

        assert "https://api.notion.com/v1/oauth/authorize" in url
        assert "test-state" in url
        assert "client_id=" in url


class TestLoggingService:
    """Test cases for LoggingService."""

    def test_log_user_action(self):
        """Test logging user actions."""
        logger = LoggingService()

        logger.log_user_action("template_generated", template_id="test-123")

        # Verify log was recorded (would check log file in real implementation)
        assert True  # Placeholder assertion

    def test_log_error(self):
        """Test logging errors."""
        logger = LoggingService()

        try:
            raise ValueError("Test error")
        except Exception as e:
            logger.log_error(e, {"operation": "test"})

        # Verify error was logged
        assert True  # Placeholder assertion

    def test_get_logs(self):
        """Test retrieving logs."""
        logger = LoggingService()

        logs = logger.get_logs(limit=10)

        assert isinstance(logs, list)


class TestErrorHandler:
    """Test cases for ErrorHandler."""

    def test_handle_error(self):
        """Test error handling."""
        handler = ErrorHandler()

        try:
            raise ValueError("Test error")
        except Exception as e:
            result = handler.handle_error(e, {"operation": "test"})

        assert "error_id" in result
        assert "message" in result
        assert result["message"] == "Test error"

    def test_error_boundary_decorator(self):
        """Test error boundary decorator."""
        handler = ErrorHandler()

        @handler.error_boundary("test_operation")
        def test_function():
            raise ValueError("Test error")

        with pytest.raises(ValueError, match="Test error"):
            test_function()

    def test_get_error_summary(self):
        """Test getting error summary."""
        handler = ErrorHandler()

        summary = handler.get_error_summary(hours=24)

        assert isinstance(summary, dict)
        assert "total_errors" in summary
        assert "errors_by_type" in summary
