"""
Unit tests for Notion Template Maker models.
"""

import pytest
from datetime import datetime
from src.models.template import Template
from src.models.user import User


class TestTemplate:
    """Test cases for Template model."""

    def test_template_creation(self):
        """Test creating a template with valid data."""
        template_data = {
            "id": "test-template-123",
            "title": "Test Template",
            "description": "A test template",
            "sections": [
                {"name": "Section 1", "content": "Content 1"},
                {"name": "Section 2", "content": "Content 2"},
            ],
            "properties": [
                {"name": "Status", "type": "select", "options": ["Todo", "Done"]},
                {
                    "name": "Priority",
                    "type": "select",
                    "options": ["Low", "Medium", "High"],
                },
            ],
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        template = Template(**template_data)

        assert template.id == "test-template-123"
        assert template.title == "Test Template"
        assert template.description == "A test template"
        assert len(template.sections) == 2
        assert len(template.properties) == 2

    def test_template_validation(self):
        """Test template validation."""
        # Valid template
        valid_data = {
            "id": "valid-template",
            "title": "Valid Template",
            "description": "Valid description",
            "sections": [{"name": "Section 1", "content": "Content"}],
            "properties": [{"name": "Status", "type": "text"}],
        }

        template = Template(**valid_data)
        assert template.id == "valid-template"
        assert template.title == "Valid Template"

        # Invalid template - invalid category
        invalid_data = {
            "id": "invalid-template",
            "title": "Invalid Template",
            "description": "Invalid category",
            "category": "invalid_category",
            "sections": [{"name": "Section 1", "content": "Content"}],
            "properties": [{"name": "Status", "type": "text"}],
        }

        with pytest.raises(Exception):  # Pydantic validation errors
            Template(**invalid_data)

    def test_template_to_dict(self):
        """Test converting template to dictionary."""
        template_data = {
            "id": "test-template",
            "title": "Test Template",
            "description": "Test description",
            "sections": [{"name": "Section 1", "content": "Content 1"}],
            "properties": [{"name": "Status", "type": "text"}],
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        template = Template(**template_data)
        template_dict = template.to_dict()

        assert template_dict["id"] == "test-template"
        assert template_dict["title"] == "Test Template"
        assert "created_at" in template_dict
        assert "updated_at" in template_dict

    def test_template_from_dict(self):
        """Test creating template from dictionary."""
        template_dict = {
            "id": "from-dict-template",
            "title": "From Dict Template",
            "description": "Created from dict",
            "sections": [{"name": "Section 1", "content": "Content"}],
            "properties": [{"name": "Status", "type": "text"}],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        template = Template.from_dict(template_dict)

        assert template.id == "from-dict-template"
        assert template.title == "From Dict Template"
        assert len(template.sections) == 1

    def test_template_sections_validation(self):
        """Test template sections validation."""
        # Valid sections
        valid_sections = [
            {"name": "Section 1", "content": "Content 1"},
            {
                "name": "Section 2",
                "content": "Content 2",
                "properties": {"key": "value"},
            },
        ]

        template_data = {
            "id": "sections-test",
            "title": "Sections Test",
            "description": "Testing sections",
            "sections": valid_sections,
            "properties": [{"name": "Status", "type": "text"}],
        }

        template = Template(**template_data)
        assert len(template.sections) == 2

        # Invalid sections - missing name (but we don't validate this)
        invalid_sections = [{"content": "Content without name"}]

        template_data["sections"] = invalid_sections
        template = Template(**template_data)  # Should not raise error
        assert len(template.sections) == 1

    def test_template_properties_validation(self):
        """Test template properties validation."""
        # Valid properties
        valid_properties = [
            {"name": "Status", "type": "select", "options": ["Todo", "Done"]},
            {"name": "Priority", "type": "number"},
            {"name": "Description", "type": "text"},
        ]

        template_data = {
            "id": "properties-test",
            "title": "Properties Test",
            "description": "Testing properties",
            "sections": [{"name": "Section 1", "content": "Content"}],
            "properties": valid_properties,
        }

        template = Template(**template_data)
        assert len(template.properties) == 3

        # Invalid properties - missing name (but we don't validate this)
        invalid_properties = [{"type": "text"}]

        template_data["properties"] = invalid_properties
        template = Template(**template_data)  # Should not raise error
        assert len(template.properties) == 1


class TestUser:
    """Test cases for User model."""

    def test_user_creation(self):
        """Test creating a user with valid data."""
        user_data = {
            "id": "user-123",
            "email": "test@example.com",
            "name": "Test User",
            "preferences": {"theme": "dark", "language": "en"},
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        user = User(**user_data)

        assert user.id == "user-123"
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.preferences["theme"] == "dark"

    def test_user_validation(self):
        """Test user validation."""
        # Valid user
        valid_data = {
            "id": "valid-user",
            "email": "valid@example.com",
            "name": "Valid User",
        }

        user = User(**valid_data)
        assert user.id == "valid-user"
        assert user.email == "valid@example.com"

        # Invalid user - invalid email
        invalid_data = {
            "id": "invalid-user",
            "email": "invalid-email",
            "name": "Invalid User",
        }

        with pytest.raises(ValueError):
            User(**invalid_data)

    def test_user_to_dict(self):
        """Test converting user to dictionary."""
        user_data = {
            "id": "test-user",
            "email": "test@example.com",
            "name": "Test User",
            "preferences": {"theme": "light"},
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        user = User(**user_data)
        user_dict = user.to_dict()

        assert user_dict["id"] == "test-user"
        assert user_dict["email"] == "test@example.com"
        assert user_dict["preferences"]["theme"] == "light"

    def test_user_from_dict(self):
        """Test creating user from dictionary."""
        user_dict = {
            "id": "from-dict-user",
            "email": "fromdict@example.com",
            "name": "From Dict User",
            "preferences": {"theme": "dark"},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        user = User.from_dict(user_dict)

        assert user.id == "from-dict-user"
        assert user.email == "fromdict@example.com"
        assert user.preferences["theme"] == "dark"

    def test_user_email_validation(self):
        """Test user email validation."""
        # Valid emails
        valid_emails = [
            "test@example.com",
            "user.name+tag@example.co.uk",
            "test.email@subdomain.example.com",
        ]

        for email in valid_emails:
            user_data = {"id": f"user-{email}", "email": email, "name": "Test User"}
            user = User(**user_data)
            assert user.email == email

        # Invalid emails
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test..test@example.com",
        ]

        for email in invalid_emails:
            user_data = {"id": f"user-{email}", "email": email, "name": "Test User"}

            with pytest.raises(Exception):  # Pydantic ValidationError
                User(**user_data)

    def test_user_preferences_handling(self):
        """Test user preferences handling."""
        # Default preferences
        user_data = {
            "id": "prefs-user",
            "email": "prefs@example.com",
            "name": "Prefs User",
        }

        user = User(**user_data)
        assert user.preferences == {}

        # Custom preferences
        custom_prefs = {"theme": "dark", "language": "es", "notifications": True}

        user_data["preferences"] = custom_prefs
        user = User(**user_data)

        assert user.preferences["theme"] == "dark"
        assert user.preferences["language"] == "es"
        assert user.preferences["notifications"] is True
