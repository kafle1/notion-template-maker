"""
Input validation and sanitization utilities for Notion Template Maker.
"""

import re
import html
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse


class InputValidator:
    """Handles input validation and sanitization for the application."""

    @staticmethod
    def sanitize_text(text: str) -> str:
        """Sanitize text input by removing potentially harmful content."""
        if not text:
            return ""

        # Remove HTML tags
        text = re.sub(r"<[^>]+>", "", text)

        # Escape HTML entities
        text = html.escape(text)

        # Remove null bytes
        text = text.replace("\x00", "")

        # Remove control characters except newlines and tabs
        text = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

        return text.strip()

    @staticmethod
    def validate_template_requirements(requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Validate template requirements input."""
        errors = []
        warnings = []

        # Validate title
        if "title" in requirements:
            title = requirements["title"]
            if not title or len(title.strip()) == 0:
                errors.append("Template title is required")
            elif len(title) > 100:
                errors.append("Template title must be less than 100 characters")
            elif not re.match(r"^[a-zA-Z0-9\s\-_]+$", title):
                warnings.append(
                    "Template title contains special characters that may cause issues"
                )

        # Validate description
        if "description" in requirements:
            description = requirements["description"]
            if len(description) > 1000:
                errors.append("Description must be less than 1000 characters")
            elif len(description.strip()) == 0:
                warnings.append("Description is empty")

        # Validate sections
        if "sections" in requirements:
            sections = requirements["sections"]
            if not isinstance(sections, list):
                errors.append("Sections must be a list")
            elif len(sections) == 0:
                errors.append("At least one section is required")
            elif len(sections) > 20:
                errors.append("Maximum 20 sections allowed")
            else:
                for i, section in enumerate(sections):
                    if not isinstance(section, dict):
                        errors.append(f"Section {i+1} must be an object")
                    elif "name" not in section:
                        errors.append(f"Section {i+1} must have a name")
                    elif len(section.get("name", "")) > 50:
                        errors.append(
                            f"Section {i+1} name must be less than 50 characters"
                        )

        # Validate properties
        if "properties" in requirements:
            properties = requirements["properties"]
            if not isinstance(properties, list):
                errors.append("Properties must be a list")
            elif len(properties) > 50:
                errors.append("Maximum 50 properties allowed")
            else:
                for i, prop in enumerate(properties):
                    if not isinstance(prop, dict):
                        errors.append(f"Property {i+1} must be an object")
                    elif "name" not in prop:
                        errors.append(f"Property {i+1} must have a name")
                    elif len(prop.get("name", "")) > 50:
                        errors.append(
                            f"Property {i+1} name must be less than 50 characters"
                        )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "sanitized_requirements": InputValidator._sanitize_requirements(
                requirements
            ),
        }

    @staticmethod
    def _sanitize_requirements(requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize all text fields in requirements."""
        sanitized = {}

        for key, value in requirements.items():
            if isinstance(value, str):
                sanitized[key] = InputValidator.sanitize_text(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    InputValidator._sanitize_requirements(item)
                    if isinstance(item, dict)
                    else InputValidator.sanitize_text(str(item))
                    if isinstance(item, str)
                    else item
                    for item in value
                ]
            elif isinstance(value, dict):
                sanitized[key] = InputValidator._sanitize_requirements(value)
            else:
                sanitized[key] = value

        return sanitized

    @staticmethod
    def validate_api_key(api_key: str, provider: str) -> Dict[str, Any]:
        """Validate API key format and basic structure."""
        errors = []

        if not api_key or len(api_key.strip()) == 0:
            errors.append(f"{provider} API key is required")
            return {"valid": False, "errors": errors}

        api_key = api_key.strip()

        # Provider-specific validation
        if provider.lower() == "openrouter":
            if not api_key.startswith("sk-or-v1-"):
                errors.append("OpenRouter API key should start with 'sk-or-v1-'")
            elif len(api_key) < 50:
                errors.append("OpenRouter API key appears to be too short")
        elif provider.lower() == "notion":
            if not re.match(r"^secret_[a-zA-Z0-9]{43}$", api_key):
                errors.append(
                    "Notion API key should be in format 'secret_[43-character-string]'"
                )
        else:
            # Generic validation
            if len(api_key) < 10:
                errors.append(f"{provider} API key appears to be too short")
            if not re.match(r"^[a-zA-Z0-9\-_\.]+$", api_key):
                errors.append(f"{provider} API key contains invalid characters")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "masked_key": InputValidator._mask_api_key(api_key),
        }

    @staticmethod
    def _mask_api_key(api_key: str) -> str:
        """Mask API key for display purposes."""
        if len(api_key) <= 8:
            return api_key
        return api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_json(json_str: str) -> Dict[str, Any]:
        """Validate and parse JSON string."""
        try:
            import json

            parsed = json.loads(json_str)
            return {"valid": True, "data": parsed}
        except json.JSONDecodeError as e:
            return {"valid": False, "error": str(e)}
        except Exception as e:
            return {"valid": False, "error": f"Invalid JSON: {str(e)}"}
