"""
Integration tests for template generation flow.
Tests the complete template generation workflow from input to output.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json


class TestTemplateGenerationIntegration:
    """Test complete template generation integration."""

    def test_template_generation_full_flow(self):
        """Test complete template generation from user input to Notion creation."""
        user_input = {
            "template_type": "project_management",
            "title": "My Project Tracker",
            "description": "A comprehensive project management template",
            "features": ["task_tracking", "team_collaboration", "progress_monitoring"],
        }

        expected_openrouter_request = {
            "model": "anthropic/claude-3-haiku",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a Notion template generator. Generate detailed Notion page and database structures.",
                },
                {
                    "role": "user",
                    "content": "Generate a project management template with: task_tracking, team_collaboration, progress_monitoring",
                },
            ],
            "temperature": 0.7,
            "max_tokens": 2000,
        }

        expected_openrouter_response = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "pages": [
                                    {
                                        "title": "Project Overview",
                                        "content": [
                                            {
                                                "type": "heading_1",
                                                "heading_1": {
                                                    "rich_text": [
                                                        {
                                                            "type": "text",
                                                            "text": {
                                                                "content": "Project Overview"
                                                            },
                                                        }
                                                    ]
                                                },
                                            }
                                        ],
                                    }
                                ],
                                "databases": [
                                    {
                                        "title": "Tasks",
                                        "properties": {
                                            "Name": {"title": {}},
                                            "Status": {
                                                "select": {
                                                    "options": [
                                                        {"name": "To Do"},
                                                        {"name": "In Progress"},
                                                        {"name": "Done"},
                                                    ]
                                                }
                                            },
                                            "Assignee": {"people": {}},
                                        },
                                    }
                                ],
                            }
                        )
                    }
                }
            ]
        }

        # This test will fail until implementation
        try:
            from src.services.template_generator import TemplateGenerator
            from src.api.openrouter_client import OpenRouterClient
            from src.api.notion_client import NotionClient

            generator = TemplateGenerator()

            with patch("requests.post") as mock_post:
                # Mock OpenRouter response
                mock_post.return_value.json.return_value = expected_openrouter_response

                # Mock Notion responses
                notion_responses = [
                    {
                        "id": "page_123",
                        "url": "https://notion.so/page_123",
                    },  # Page creation
                    {
                        "id": "database_456",
                        "url": "https://notion.so/database_456",
                    },  # Database creation
                ]
                mock_post.side_effect = [
                    Mock(json=lambda: expected_openrouter_response),  # OpenRouter call
                    Mock(json=lambda: notion_responses[0]),  # Page creation
                    Mock(json=lambda: notion_responses[1]),  # Database creation
                ]

                result = generator.generate_template(user_input)

                # Verify OpenRouter was called correctly
                openrouter_call = mock_post.call_args_list[0]
                openrouter_data = json.loads(openrouter_call[1]["data"])
                assert openrouter_data["model"] == "anthropic/claude-3-haiku"
                assert (
                    "project management"
                    in openrouter_data["messages"][1]["content"].lower()
                )

                # Verify Notion API calls were made
                assert (
                    len(mock_post.call_args_list) >= 2
                )  # At least OpenRouter + Notion calls

                # Verify result structure
                assert "pages" in result
                assert "databases" in result
                assert len(result["pages"]) > 0
                assert len(result["databases"]) > 0

        except ImportError:
            pytest.fail("TemplateGenerator or API clients not implemented yet")

    def test_template_generation_with_custom_properties(self):
        """Test template generation with custom user-defined properties."""
        custom_properties = {
            "custom_field_1": "text",
            "custom_field_2": "number",
            "custom_field_3": "select",
        }

        user_input = {
            "template_type": "custom",
            "title": "Custom Template",
            "custom_properties": custom_properties,
        }

        # This test will fail until implementation
        try:
            from src.services.template_generator import TemplateGenerator

            generator = TemplateGenerator()

            with patch("requests.post") as mock_post:
                mock_response = {
                    "choices": [
                        {
                            "message": {
                                "content": json.dumps(
                                    {
                                        "databases": [
                                            {
                                                "title": "Custom Database",
                                                "properties": {
                                                    "Name": {"title": {}},
                                                    "custom_field_1": {"rich_text": {}},
                                                    "custom_field_2": {"number": {}},
                                                    "custom_field_3": {
                                                        "select": {"options": []}
                                                    },
                                                },
                                            }
                                        ]
                                    }
                                )
                            }
                        }
                    ]
                }
                mock_post.return_value.json.return_value = mock_response

                result = generator.generate_template(user_input)

                # Verify custom properties were included in the request
                call_args = mock_post.call_args
                request_data = json.loads(call_args[1]["data"])
                request_content = request_data["messages"][1]["content"]

                assert "custom_field_1" in request_content
                assert "custom_field_2" in request_content
                assert "custom_field_3" in request_content

        except ImportError:
            pytest.fail("TemplateGenerator not implemented yet")

    def test_template_generation_error_handling(self):
        """Test error handling in template generation flow."""
        user_input = {"template_type": "project_management", "title": "Test Template"}

        error_scenarios = [
            # OpenRouter API error
            {
                "service": "openrouter",
                "status_code": 429,
                "error": {"error": {"message": "Rate limit exceeded"}},
            },
            # Notion API error
            {
                "service": "notion",
                "status_code": 401,
                "error": {"error": {"code": "unauthorized"}},
            },
            # Invalid response format
            {
                "service": "openrouter",
                "status_code": 200,
                "error": {"choices": []},  # Empty choices
            },
        ]

        for scenario in error_scenarios:
            with patch("requests.post") as mock_post:
                if scenario["service"] == "openrouter":
                    mock_post.return_value.status_code = scenario["status_code"]
                    mock_post.return_value.json.return_value = scenario["error"]
                else:
                    # First call succeeds (OpenRouter), second fails (Notion)
                    mock_post.side_effect = [
                        Mock(
                            json=lambda: {"choices": [{"message": {"content": "{}"}}]}
                        ),
                        Mock(
                            status_code=scenario["status_code"],
                            json=lambda: scenario["error"],
                        ),
                    ]

                try:
                    from src.services.template_generator import TemplateGenerator

                    generator = TemplateGenerator()

                    with pytest.raises(Exception) as exc_info:
                        generator.generate_template(user_input)

                    # Verify appropriate error was raised
                    error_message = str(exc_info.value).lower()
                    if scenario["service"] == "openrouter":
                        assert (
                            "openrouter" in error_message
                            or "rate limit" in error_message
                        )
                    else:
                        assert (
                            "notion" in error_message or "unauthorized" in error_message
                        )

                except ImportError:
                    pytest.fail("TemplateGenerator not implemented yet")

    def test_template_generation_with_session_management(self):
        """Test template generation with session state management."""
        user_input = {"template_type": "meeting_notes", "title": "Meeting Template"}

        # This test will fail until implementation
        try:
            from src.services.template_generator import TemplateGenerator
            from src.services.session_manager import SessionManager

            generator = TemplateGenerator()
            session_manager = SessionManager()

            # Mock session state
            session_data = {
                "api_keys": {
                    "openrouter": "test_openrouter_key",
                    "notion": "test_notion_token",
                },
                "user_preferences": {
                    "model": "anthropic/claude-3-haiku",
                    "temperature": 0.7,
                },
            }

            with patch("streamlit.session_state", session_data), patch(
                "requests.post"
            ) as mock_post:
                mock_post.return_value.json.return_value = {
                    "choices": [
                        {
                            "message": {
                                "content": json.dumps(
                                    {
                                        "pages": [
                                            {"title": "Meeting Notes", "content": []}
                                        ]
                                    }
                                )
                            }
                        }
                    ]
                }

                result = generator.generate_template(user_input)

                # Verify session data was used
                call_args = mock_post.call_args
                request_data = json.loads(call_args[1]["data"])

                # Check that API keys were used (in headers)
                headers = call_args[1]["headers"]
                assert "Authorization" in headers
                assert "Bearer test_openrouter_key" in headers["Authorization"]

                # Check that user preferences were applied
                assert request_data["model"] == "anthropic/claude-3-haiku"
                assert request_data["temperature"] == 0.7

        except ImportError:
            pytest.fail("TemplateGenerator or SessionManager not implemented yet")

    def test_template_validation_integration(self):
        """Test template validation as part of generation flow."""
        user_input = {"template_type": "invalid_template", "title": ""}

        # This test will fail until implementation
        try:
            from src.services.template_generator import TemplateGenerator
            from src.services.template_validator import TemplateValidator

            generator = TemplateGenerator()
            validator = TemplateValidator()

            # Test validation before generation
            with pytest.raises(ValueError) as exc_info:
                generator.generate_template(user_input)

            assert (
                "title" in str(exc_info.value).lower()
                or "required" in str(exc_info.value).lower()
            )

        except ImportError:
            pytest.fail("TemplateGenerator or TemplateValidator not implemented yet")
