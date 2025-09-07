"""
Unit tests for Notion Template Maker UI components.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.ui.api_config import render_api_config
from src.ui.template_input import render_template_input
from src.ui.template_preview import render_template_preview
from src.ui.progress_indicator import render_progress
from src.ui.error_handler import handle_error


class TestApiConfig:
    """Test cases for API configuration UI component."""

    @patch("src.ui.api_config.st")
    def test_render_api_config_openrouter(self, mock_st):
        """Test rendering OpenRouter API configuration."""
        # Mock streamlit components
        mock_st.sidebar = Mock()
        mock_st.subheader = Mock()
        mock_st.text_input = Mock(return_value="sk-or-v1-test-key")
        mock_st.success = Mock()
        mock_st.error = Mock()
        mock_st.expander = Mock()
        mock_st.markdown = Mock()

        # Mock session state
        mock_st.session_state = Mock()
        mock_st.session_state.get.return_value = None

        result = render_api_config()

        assert "openrouter_configured" in result
        assert "notion_configured" in result
        assert "all_configured" in result

    @patch("src.ui.api_config.st")
    def test_render_api_config_notion_oauth(self, mock_st):
        """Test rendering Notion OAuth configuration."""
        # Mock streamlit components
        mock_st.sidebar = Mock()
        mock_st.subheader = Mock()
        mock_st.markdown = Mock()
        mock_st.button = Mock(return_value=True)
        mock_st.text_input = Mock(return_value="")
        mock_st.success = Mock()
        mock_st.error = Mock()
        mock_st.expander = Mock()

        # Mock session state
        mock_st.session_state = Mock()
        mock_st.session_state.get.return_value = None

        result = render_api_config()

        assert "openrouter_configured" in result
        assert "notion_configured" in result

    @patch("src.ui.api_config.st")
    def test_render_api_config_with_session_manager(self, mock_st):
        """Test rendering API config with session manager."""
        # Mock session manager
        mock_session_manager = Mock()
        mock_session_manager.get_api_key.return_value = "sk-or-v1-stored-key"

        # Mock streamlit components
        mock_st.sidebar = Mock()
        mock_st.subheader = Mock()
        mock_st.text_input = Mock(return_value="sk-or-v1-stored-key")
        mock_st.success = Mock()
        mock_st.error = Mock()
        mock_st.expander = Mock()
        mock_st.markdown = Mock()
        mock_st.button = Mock(return_value=False)

        # Mock session state
        mock_st.session_state = Mock()
        mock_st.session_state.get.return_value = "test-session-id"

        result = render_api_config(session_manager=mock_session_manager)

        assert result["openrouter_configured"] is True
        mock_session_manager.get_api_key.assert_called_with(
            "test-session-id", "openrouter"
        )


class TestTemplateInput:
    """Test cases for template input UI component."""

    @patch("src.ui.template_input.st")
    def test_render_template_input_basic(self, mock_st):
        """Test rendering basic template input form."""
        # Mock streamlit components
        mock_st.header = Mock()
        mock_st.text_input = Mock(return_value="Test Template")
        mock_st.text_area = Mock(return_value="Test description")
        mock_st.multiselect = Mock(return_value=["Section 1", "Section 2"])
        mock_st.selectbox = Mock(side_effect=["select", "text"])
        mock_st.slider = Mock(return_value=5)
        mock_st.button = Mock(return_value=False)
        mock_st.expander = Mock()
        mock_st.markdown = Mock()

        result = render_template_input()

        assert isinstance(result, dict)
        assert "title" in result
        assert result["title"] == "Test Template"

    @patch("src.ui.template_input.st")
    def test_render_template_input_with_properties(self, mock_st):
        """Test rendering template input with custom properties."""
        # Mock streamlit components
        mock_st.header = Mock()
        mock_st.text_input = Mock(
            side_effect=["Test Template", "Property 1", "Property 2"]
        )
        mock_st.text_area = Mock(return_value="Test description")
        mock_st.multiselect = Mock(return_value=["Section 1"])
        mock_st.selectbox = Mock(side_effect=["select", "text", "select"])
        mock_st.slider = Mock(return_value=2)
        mock_st.button = Mock(side_effect=[True, False])  # Add property, then submit
        mock_st.expander = Mock()
        mock_st.markdown = Mock()
        mock_st.empty = Mock()

        result = render_template_input()

        assert isinstance(result, dict)
        assert "properties" in result

    @patch("src.ui.template_input.st")
    def test_render_template_input_validation(self, mock_st):
        """Test template input validation."""
        # Mock streamlit components
        mock_st.header = Mock()
        mock_st.text_input = Mock(return_value="")  # Empty title
        mock_st.text_area = Mock(return_value="")
        mock_st.multiselect = Mock(return_value=[])
        mock_st.selectbox = Mock(return_value="text")
        mock_st.slider = Mock(return_value=0)
        mock_st.button = Mock(return_value=True)
        mock_st.expander = Mock()
        mock_st.markdown = Mock()
        mock_st.warning = Mock()

        result = render_template_input()

        # Should return None for invalid input
        assert result is None


class TestTemplatePreview:
    """Test cases for template preview UI component."""

    @patch("src.ui.template_preview.st")
    def test_render_template_preview_with_data(self, mock_st):
        """Test rendering template preview with data."""
        # Mock template data
        template_data = {
            "id": "test-template",
            "title": "Test Template",
            "description": "Test description",
            "sections": [
                {"name": "Section 1", "content": "Content 1"},
                {"name": "Section 2", "content": "Content 2"},
            ],
            "properties": [
                {"name": "Status", "type": "select", "options": ["Todo", "Done"]},
                {"name": "Priority", "type": "text"},
            ],
        }

        # Mock streamlit components
        mock_st.header = Mock()
        mock_st.subheader = Mock()
        mock_st.markdown = Mock()
        mock_st.json = Mock()
        mock_st.expander = Mock()
        mock_st.button = Mock(return_value=False)

        # Mock session state
        mock_st.session_state = Mock()
        mock_st.session_state.get.return_value = template_data

        render_template_preview()

        # Verify components were called
        mock_st.header.assert_called_with("👀 Template Preview")
        mock_st.subheader.assert_called()

    @patch("src.ui.template_preview.st")
    def test_render_template_preview_no_data(self, mock_st):
        """Test rendering template preview with no data."""
        # Mock streamlit components
        mock_st.header = Mock()
        mock_st.info = Mock()

        # Mock session state
        mock_st.session_state = Mock()
        mock_st.session_state.get.return_value = None

        render_template_preview()

        mock_st.info.assert_called_with(
            "No template to preview. Generate a template first."
        )

    @patch("src.ui.template_preview.st")
    def test_render_template_preview_export(self, mock_st):
        """Test template preview export functionality."""
        template_data = {
            "id": "test-template",
            "title": "Test Template",
            "sections": [{"name": "Section 1", "content": "Content"}],
            "properties": [{"name": "Status", "type": "text"}],
        }

        # Mock streamlit components
        mock_st.header = Mock()
        mock_st.subheader = Mock()
        mock_st.markdown = Mock()
        mock_st.json = Mock()
        mock_st.expander = Mock()
        mock_st.button = Mock(return_value=True)  # Export button clicked
        mock_st.download_button = Mock()

        # Mock session state
        mock_st.session_state = Mock()
        mock_st.session_state.get.return_value = template_data

        render_template_preview()

        mock_st.download_button.assert_called()


class TestProgressIndicator:
    """Test cases for progress indicator UI component."""

    @patch("src.ui.progress_indicator.st")
    def test_render_progress_basic(self, mock_st):
        """Test rendering basic progress indicator."""
        # Mock streamlit components
        mock_st.spinner = Mock()
        mock_st.progress = Mock()
        mock_st.text = Mock()
        mock_st.empty = Mock()

        render_progress()

        mock_st.spinner.assert_called_once()
        mock_st.progress.assert_called()

    @patch("src.ui.progress_indicator.st")
    @patch("time.sleep")
    def test_render_progress_with_steps(self, mock_st, mock_sleep):
        """Test rendering progress with multiple steps."""
        # Mock streamlit components
        mock_st.spinner = Mock()
        mock_st.progress = Mock()
        mock_st.text = Mock()
        mock_st.empty = Mock()

        render_progress()

        # Verify progress updates were called
        assert mock_st.progress.call_count > 1
        assert mock_st.text.call_count > 1


class TestErrorHandlerUI:
    """Test cases for error handler UI component."""

    @patch("src.ui.error_handler.st")
    def test_handle_error_basic(self, mock_st):
        """Test basic error handling."""
        # Mock streamlit components
        mock_st.error = Mock()
        mock_st.expander = Mock()
        mock_st.code = Mock()
        mock_st.button = Mock(return_value=False)

        test_error = ValueError("Test error message")

        handle_error(test_error)

        mock_st.error.assert_called_with("❌ An error occurred: Test error message")

    @patch("src.ui.error_handler.st")
    def test_handle_error_with_details(self, mock_st):
        """Test error handling with additional details."""
        # Mock streamlit components
        mock_st.error = Mock()
        mock_st.expander = Mock()
        mock_st.code = Mock()
        mock_st.button = Mock(return_value=True)  # Show details clicked

        test_error = Exception("Detailed error")
        context = {"operation": "test_operation", "user_id": "user123"}

        handle_error(test_error, context)

        mock_st.error.assert_called()
        mock_st.expander.assert_called()

    @patch("src.ui.error_handler.st")
    def test_handle_error_network_issue(self, mock_st):
        """Test error handling for network issues."""
        # Mock streamlit components
        mock_st.error = Mock()
        mock_st.expander = Mock()
        mock_st.code = Mock()
        mock_st.button = Mock(return_value=False)

        # Simulate network error
        test_error = ConnectionError("Network connection failed")

        handle_error(test_error)

        mock_st.error.assert_called_with("❌ Network error: Network connection failed")

    @patch("src.ui.error_handler.st")
    def test_handle_error_validation_issue(self, mock_st):
        """Test error handling for validation issues."""
        # Mock streamlit components
        mock_st.error = Mock()
        mock_st.expander = Mock()
        mock_st.code = Mock()
        mock_st.button = Mock(return_value=False)

        # Simulate validation error
        test_error = ValueError("Invalid input: title is required")

        handle_error(test_error)

        mock_st.error.assert_called_with(
            "❌ Validation error: Invalid input: title is required"
        )
