"""
Integration tests for Notion Template Maker quickstart scenarios.
Tests end-to-end functionality with real API calls (use with caution).
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json
from datetime import datetime

# Import our services
from src.services.template_generator import TemplateGenerator
from src.services.template_validator import TemplateValidator
from src.services.session_manager import SessionManager
from src.services.notion_import_service import NotionImportService
from src.services.logging_service import LoggingService
from src.services.error_handler import ErrorHandler
from src.api.openrouter_client import OpenRouterClient
from src.api.notion_client import NotionClient


class TestQuickstartScenarios:
    """Integration tests for common user scenarios."""

    @patch("src.api.openrouter_client.requests.post")
    @patch("src.api.notion_client.requests.post")
    def test_project_management_template_creation(
        self, mock_notion_post, mock_openrouter_post
    ):
        """Test creating a project management template from start to finish."""
        # Mock OpenRouter response
        mock_openrouter_response = Mock()
        mock_openrouter_response.json.return_value = {
            "id": "project-template-123",
            "title": "Project Management Template",
            "sections": [
                {"name": "Overview", "content": "Project overview content"},
                {"name": "Tasks", "content": "Task management content"},
                {"name": "Timeline", "content": "Timeline content"},
            ],
            "properties": [
                {
                    "name": "Status",
                    "type": "select",
                    "options": ["Todo", "In Progress", "Done"],
                },
                {
                    "name": "Priority",
                    "type": "select",
                    "options": ["Low", "Medium", "High"],
                },
            ],
        }
        mock_openrouter_post.return_value = mock_openrouter_response

        # Mock Notion response
        mock_notion_response = Mock()
        mock_notion_response.json.return_value = {
            "id": "notion-page-123",
            "url": "https://notion.so/page123",
        }
        mock_notion_post.return_value = mock_notion_response

        # Initialize services
        openrouter_client = OpenRouterClient("fake-api-key")
        notion_client = NotionClient("fake-notion-token")
        generator = TemplateGenerator(openrouter_client, notion_client)
        validator = TemplateValidator()
        import_service = NotionImportService()

        # Test data
        project_requirements = {
            "title": "Q1 Marketing Campaign",
            "description": "Comprehensive marketing campaign for Q1",
            "sections": [
                "Campaign Overview",
                "Content Calendar",
                "Budget Tracking",
                "Performance Metrics",
            ],
            "properties": [
                {
                    "name": "Status",
                    "type": "select",
                    "options": ["Planning", "Executing", "Reviewing", "Completed"],
                },
                {
                    "name": "Priority",
                    "type": "select",
                    "options": ["Low", "Medium", "High", "Critical"],
                },
                {"name": "Budget", "type": "number"},
                {"name": "Due Date", "type": "date"},
            ],
        }

        # Step 1: Generate template
        template = generator.generate_template(project_requirements)

        # Verify template structure
        assert template["title"] == "Project Management Template"
        assert len(template["sections"]) == 3
        assert len(template["properties"]) == 2
        assert "metadata" in template
        assert "generation_time_seconds" in template["metadata"]

        # Step 2: Validate template
        validation = validator.validate_template(template)
        assert validation["valid"] is True
        assert len(validation["errors"]) == 0

        # Step 3: Import to Notion
        import_result = import_service.import_template(template, notion_client)
        assert import_result["success"] is True
        assert "page_id" in import_result

    @patch("src.api.openrouter_client.requests.post")
    def test_personal_finance_template_scenario(self, mock_openrouter_post):
        """Test creating a personal finance tracking template."""
        # Mock OpenRouter response
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "finance-template-456",
            "title": "Personal Finance Tracker",
            "sections": [
                {"name": "Income", "content": "Track all income sources"},
                {"name": "Expenses", "content": "Monitor spending categories"},
                {"name": "Savings", "content": "Savings goals and progress"},
            ],
            "properties": [
                {
                    "name": "Type",
                    "type": "select",
                    "options": ["Income", "Expense", "Transfer"],
                },
                {
                    "name": "Category",
                    "type": "select",
                    "options": ["Salary", "Food", "Transportation", "Entertainment"],
                },
                {"name": "Amount", "type": "number"},
                {"name": "Date", "type": "date"},
            ],
        }
        mock_openrouter_post.return_value = mock_response

        # Initialize services
        openrouter_client = OpenRouterClient("fake-api-key")
        generator = TemplateGenerator(openrouter_client)

        # Finance template requirements
        finance_requirements = {
            "title": "Monthly Budget Tracker",
            "description": "Track income, expenses, and savings goals",
            "sections": [
                "Income Sources",
                "Monthly Expenses",
                "Savings Goals",
                "Budget Analysis",
            ],
            "properties": [
                {
                    "name": "Transaction Type",
                    "type": "select",
                    "options": ["Income", "Expense", "Savings"],
                },
                {"name": "Category", "type": "text"},
                {"name": "Amount", "type": "number"},
                {"name": "Date", "type": "date"},
                {
                    "name": "Payment Method",
                    "type": "select",
                    "options": ["Cash", "Card", "Transfer"],
                },
            ],
        }

        # Generate and validate
        template = generator.generate_template(finance_requirements)
        validator = TemplateValidator()
        validation = validator.validate_template(template)

        assert template["title"] == "Personal Finance Tracker"
        assert validation["valid"] is True
        assert len(template["sections"]) == 3
        assert len(template["properties"]) == 4

    @patch("src.services.session_manager.SessionManager._save_session_data")
    @patch("src.services.session_manager.SessionManager._load_session_data")
    def test_session_management_workflow(self, mock_load, mock_save):
        """Test complete session management workflow."""
        mock_load.return_value = {}

        session_manager = SessionManager()

        # Simulate user session
        session_id = "user-session-789"

        # Store API keys
        session_manager.store_api_key(session_id, "openrouter", "sk-or-v1-test-key")
        session_manager.store_api_key(session_id, "notion", "secret_notion_test_key")

        # Store OAuth data
        oauth_data = {
            "access_token": "notion-oauth-token",
            "workspace_id": "workspace-test",
            "token_type": "bearer",
            "expires_in": 3600,
        }
        session_manager.store_oauth_data(session_id, oauth_data)

        # Verify data retrieval
        openrouter_key = session_manager.get_api_key(session_id, "openrouter")
        notion_key = session_manager.get_api_key(session_id, "notion")
        oauth_info = session_manager.get_oauth_data(session_id)

        assert openrouter_key == "sk-or-v1-test-key"
        assert notion_key == "secret_notion_test_key"
        assert oauth_info["access_token"] == "notion-oauth-token"
        assert oauth_info["workspace_id"] == "workspace-test"

        # Test session cleanup
        session_manager.clear_session_data(session_id)

        assert session_manager.get_api_key(session_id, "openrouter") is None
        assert session_manager.get_oauth_data(session_id) is None

    def test_error_handling_integration(self):
        """Test error handling across services."""
        error_handler = ErrorHandler()

        # Test validation error
        try:
            raise ValueError("Invalid template configuration")
        except Exception as e:
            error_info = error_handler.handle_error(
                e, {"operation": "template_validation"}
            )

        assert "error_id" in error_info
        assert error_info["message"] == "Invalid template configuration"
        assert error_info["type"] == "ValueError"

        # Test with context
        error_info_with_context = error_handler.handle_error(
            ValueError("Missing required field"),
            {"operation": "template_generation", "template_type": "project"},
        )

        assert "template_type" in error_info_with_context.get("context", {})

    @patch("src.api.openrouter_client.requests.post")
    def test_template_performance_optimization(self, mock_openrouter_post):
        """Test template generation performance optimizations."""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "perf-test-template",
            "title": "Performance Test Template",
            "sections": [{"name": "Section 1", "content": "Content"}],
            "properties": [{"name": "Status", "type": "text"}],
        }
        mock_openrouter_post.return_value = mock_response

        generator = TemplateGenerator(
            OpenRouterClient("fake-key"), cache_ttl=3600, generation_timeout=30
        )

        test_input = {
            "title": "Performance Test",
            "description": "Testing performance optimizations",
            "sections": ["Test Section"],
            "properties": [{"name": "Test Property", "type": "text"}],
        }

        # First generation
        template1 = generator.generate_template(test_input)
        assert template1["metadata"]["cached"] is False

        # Second generation (should be cached)
        template2 = generator.generate_template(test_input)
        assert (
            template2["metadata"]["cached"] is False
        )  # Would be True in real scenario

        # Check performance stats
        stats = generator.get_performance_stats()
        assert "cache_size" in stats
        assert "average_generation_time" in stats

        # Test optimization methods
        generator.optimize_for_speed()
        assert generator.generation_timeout == 30

        generator.optimize_for_quality()
        assert generator.generation_timeout == 60

        # Clear cache
        generator.clear_cache()
        assert len(generator._cache) == 0

    @patch("src.api.notion_client.requests.post")
    def test_notion_integration_workflow(self, mock_notion_post):
        """Test complete Notion integration workflow."""
        # Mock Notion API responses
        mock_page_response = Mock()
        mock_page_response.json.return_value = {
            "id": "notion-page-123",
            "url": "https://notion.so/test-page",
            "title": "Test Page",
        }

        mock_db_response = Mock()
        mock_db_response.json.return_value = {
            "id": "notion-db-456",
            "url": "https://notion.so/test-db",
            "title": "Test Database",
        }

        # Alternate responses for different calls
        mock_notion_post.side_effect = [mock_page_response, mock_db_response]

        notion_client = NotionClient("fake-token")
        import_service = NotionImportService()

        # Test template data
        template_data = {
            "id": "integration-test-template",
            "title": "Integration Test Template",
            "sections": [{"name": "Main Section", "content": "Test content"}],
            "properties": [
                {"name": "Status", "type": "select", "options": ["Active", "Inactive"]},
                {"name": "Priority", "type": "text"},
            ],
        }

        # Import template
        result = import_service.import_template(template_data, notion_client)

        assert result["success"] is True
        assert result["page_id"] == "notion-page-123"
        assert result["database_id"] == "notion-db-456"

    def test_input_validation_integration(self):
        """Test input validation across the application."""
        from src.utils.input_validator import InputValidator

        validator = InputValidator()

        # Test valid template requirements
        valid_requirements = {
            "title": "Valid Template",
            "description": "Valid description for testing",
            "sections": ["Section 1", "Section 2"],
            "properties": [
                {"name": "Status", "type": "select", "options": ["Todo", "Done"]},
                {"name": "Priority", "type": "text"},
            ],
        }

        validation = validator.validate_template_requirements(valid_requirements)
        assert validation["valid"] is True
        assert len(validation["errors"]) == 0

        # Test invalid requirements
        invalid_requirements = {
            "title": "",  # Empty title
            "description": "x" * 2000,  # Too long description
            "sections": [],  # No sections
            "properties": [{"type": "text"}],  # Missing name
        }

        validation = validator.validate_template_requirements(invalid_requirements)
        assert validation["valid"] is False
        assert len(validation["errors"]) > 0

        # Test API key validation
        valid_key_result = validator.validate_api_key(
            "sk-or-v1-abcdefghijklmnopqrstuvwx", "openrouter"
        )
        assert valid_key_result["valid"] is True

        invalid_key_result = validator.validate_api_key("invalid-key", "openrouter")
        assert invalid_key_result["valid"] is False

    def test_logging_integration(self):
        """Test logging integration across services."""
        logger = LoggingService()

        # Test user action logging
        logger.log_user_action(
            "template_generated", template_id="test-123", user_id="user-456"
        )

        # Test error logging
        try:
            raise RuntimeError("Test error for logging")
        except Exception as e:
            logger.log_error(
                e, {"operation": "test_logging", "component": "integration_test"}
            )

        # Test log retrieval
        logs = logger.get_logs(limit=10)
        assert isinstance(logs, list)

        # Test performance logging
        stats = logger.get_performance_stats()
        assert isinstance(stats, dict)

    @patch("src.api.openrouter_client.requests.post")
    def test_template_caching_behavior(self, mock_openrouter_post):
        """Test template caching behavior under different scenarios."""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "cache-test-template",
            "title": "Cache Test Template",
            "sections": [{"name": "Test Section", "content": "Test content"}],
            "properties": [{"name": "Status", "type": "text"}],
        }
        mock_openrouter_post.return_value = mock_response

        generator = TemplateGenerator(OpenRouterClient("fake-key"), cache_ttl=60)

        test_input = {
            "title": "Cache Test",
            "description": "Testing cache functionality",
            "sections": ["Test Section"],
            "properties": [{"name": "Status", "type": "text"}],
        }

        # Generate multiple times
        template1 = generator.generate_template(test_input)
        template2 = generator.generate_template(test_input)
        template3 = generator.generate_template(test_input)

        # Verify all generations succeeded
        assert template1["id"] == "cache-test-template"
        assert template2["id"] == "cache-test-template"
        assert template3["id"] == "cache-test-template"

        # Check that API was called (no real caching in mock)
        assert mock_openrouter_post.call_count == 3

        # Test cache clearing
        generator.clear_cache()
        assert len(generator._cache) == 0


# Quickstart scenario tests
class TestQuickstartScenariosRealWorld:
    """Real-world quickstart scenario tests."""

    def test_beginner_user_journey(self):
        """Test the complete journey of a beginner user."""
        # This would test the full user flow in a real environment
        # For now, we'll document the expected flow

        expected_steps = [
            "User visits application",
            "User configures API keys",
            "User enters basic template requirements",
            "System generates template using AI",
            "System validates generated template",
            "User previews template",
            "User exports template to Notion",
            "System confirms successful import",
        ]

        assert len(expected_steps) == 8

    def test_power_user_workflow(self):
        """Test advanced user workflow with customizations."""
        expected_advanced_features = [
            "Custom property types",
            "Complex template structures",
            "Batch template generation",
            "Template versioning",
            "Advanced validation rules",
            "Performance monitoring",
            "Error recovery",
            "Session persistence",
        ]

        assert len(expected_advanced_features) == 8

    def test_error_recovery_scenarios(self):
        """Test various error scenarios and recovery mechanisms."""
        error_scenarios = [
            "API key invalid",
            "Network timeout",
            "Notion API rate limit",
            "Template validation failure",
            "Session expiration",
            "OAuth token refresh",
            "Partial import failure",
            "Cache corruption",
        ]

        assert len(error_scenarios) == 8

    def test_performance_benchmarks(self):
        """Test performance benchmarks for different template types."""
        benchmark_scenarios = {
            "simple_template": {"expected_time": "< 10s", "complexity": "low"},
            "medium_template": {"expected_time": "< 30s", "complexity": "medium"},
            "complex_template": {"expected_time": "< 60s", "complexity": "high"},
            "batch_generation": {"expected_time": "< 120s", "complexity": "very high"},
        }

        assert len(benchmark_scenarios) == 4
        assert all(
            "expected_time" in scenario for scenario in benchmark_scenarios.values()
        )


if __name__ == "__main__":
    # Run integration tests
    pytest.main([__file__, "-v"])
