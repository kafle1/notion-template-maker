"""
Template validation service for the Notion Template Maker application.
Validates template data, user input, and API responses.
"""

from typing import Optional, Dict, Any, List
import re
from datetime import datetime


class TemplateValidator:
    """Service for validating templates and user input."""

    # Maximum limits
    MAX_TITLE_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 500
    MAX_CONTENT_BLOCKS = 100
    MAX_DATABASE_PROPERTIES = 50
    MAX_PROPERTY_NAME_LENGTH = 50
    MAX_SELECT_OPTIONS = 50

    # Valid template types
    VALID_TEMPLATE_TYPES = {
        "general",
        "project_management",
        "knowledge_base",
        "personal",
        "business",
        "education",
        "health",
        "finance",
        "marketing",
        "development",
        "design",
        "writing",
        "research",
        "meeting_notes",
        "task_management",
        "goal_tracking",
        "habit_tracking",
        "budget_tracking",
    }

    # Valid Notion property types
    VALID_PROPERTY_TYPES = {
        "title",
        "rich_text",
        "number",
        "select",
        "multi_select",
        "date",
        "people",
        "files",
        "checkbox",
        "url",
        "email",
        "phone_number",
        "formula",
        "relation",
        "rollup",
        "created_time",
        "created_by",
        "last_edited_time",
        "last_edited_by",
    }

    # Valid Notion block types
    VALID_BLOCK_TYPES = {
        "paragraph",
        "heading_1",
        "heading_2",
        "heading_3",
        "bulleted_list_item",
        "numbered_list_item",
        "to_do",
        "code",
        "quote",
        "callout",
        "divider",
        "image",
        "video",
        "file",
        "embed",
        "bookmark",
        "link_preview",
        "table",
        "table_row",
        "column_list",
        "column",
    }

    def validate_user_input(self, user_input: Dict[str, Any]) -> List[str]:
        """
        Validate user input for template generation.

        Args:
            user_input: User input dictionary

        Returns:
            List of validation errors
        """
        errors = []

        if not isinstance(user_input, dict):
            errors.append("User input must be a dictionary")
            return errors

        # Validate template type
        template_type = user_input.get("template_type", "").strip()
        if not template_type:
            errors.append("Template type is required")
        elif template_type not in self.VALID_TEMPLATE_TYPES:
            errors.append(f"Invalid template type: {template_type}")

        # Validate title
        title = user_input.get("title", "").strip()
        if not title:
            errors.append("Title is required")
        elif len(title) > self.MAX_TITLE_LENGTH:
            errors.append(f"Title too long (max {self.MAX_TITLE_LENGTH} characters)")

        # Validate description
        description = user_input.get("description", "")
        if (
            isinstance(description, str)
            and len(description) > self.MAX_DESCRIPTION_LENGTH
        ):
            errors.append(
                f"Description too long (max {self.MAX_DESCRIPTION_LENGTH} characters)"
            )

        # Validate features
        features = user_input.get("features", [])
        if features:
            if not isinstance(features, list):
                errors.append("Features must be a list")
            else:
                for feature in features:
                    if not isinstance(feature, str) or not feature.strip():
                        errors.append("All features must be non-empty strings")

        # Validate custom properties
        custom_properties = user_input.get("custom_properties", {})
        if custom_properties:
            prop_errors = self._validate_custom_properties(custom_properties)
            errors.extend(prop_errors)

        return errors

    def _validate_custom_properties(self, properties: Dict[str, Any]) -> List[str]:
        """
        Validate custom properties configuration.

        Args:
            properties: Custom properties dictionary

        Returns:
            List of validation errors
        """
        errors = []

        if not isinstance(properties, dict):
            errors.append("Custom properties must be a dictionary")
            return errors

        for prop_name, prop_type in properties.items():
            # Validate property name
            if not isinstance(prop_name, str) or not prop_name.strip():
                errors.append("Property names must be non-empty strings")
                continue

            if len(prop_name) > self.MAX_PROPERTY_NAME_LENGTH:
                errors.append(
                    f"Property name '{prop_name}' too long (max {self.MAX_PROPERTY_NAME_LENGTH} characters)"
                )

            # Validate property type
            if not isinstance(prop_type, str):
                errors.append(f"Property '{prop_name}' type must be a string")
                continue

            # Allow common aliases
            type_mapping = {
                "text": "rich_text",
                "string": "rich_text",
                "boolean": "checkbox",
                "bool": "checkbox",
            }

            normalized_type = type_mapping.get(prop_type.lower(), prop_type.lower())

            if normalized_type not in self.VALID_PROPERTY_TYPES:
                errors.append(f"Invalid property type '{prop_type}' for '{prop_name}'")

        return errors

    def validate_template_data(self, template_data: Dict[str, Any]) -> List[str]:
        """
        Validate generated template data structure.

        Args:
            template_data: Template data dictionary

        Returns:
            List of validation errors
        """
        errors = []

        if not isinstance(template_data, dict):
            errors.append("Template data must be a dictionary")
            return errors

        # Validate pages
        pages = template_data.get("pages", [])
        if not isinstance(pages, list):
            errors.append("'pages' must be a list")
        else:
            for i, page in enumerate(pages):
                page_errors = self._validate_page_data(page, i)
                errors.extend(page_errors)

        # Validate databases
        databases = template_data.get("databases", [])
        if not isinstance(databases, list):
            errors.append("'databases' must be a list")
        else:
            for i, db in enumerate(databases):
                db_errors = self._validate_database_data(db, i)
                errors.extend(db_errors)

        # Validate metadata
        metadata = template_data.get("metadata", {})
        if metadata:
            meta_errors = self._validate_metadata(metadata)
            errors.extend(meta_errors)

        return errors

    def _validate_page_data(self, page_data: Dict[str, Any], index: int) -> List[str]:
        """
        Validate individual page data.

        Args:
            page_data: Page data dictionary
            index: Page index for error messages

        Returns:
            List of validation errors
        """
        errors = []
        prefix = f"Page {index}"

        if not isinstance(page_data, dict):
            errors.append(f"{prefix}: must be a dictionary")
            return errors

        # Validate title
        title = page_data.get("title", "").strip()
        if not title:
            errors.append(f"{prefix}: title is required")
        elif len(title) > self.MAX_TITLE_LENGTH:
            errors.append(
                f"{prefix}: title too long (max {self.MAX_TITLE_LENGTH} characters)"
            )

        # Validate content blocks
        content = page_data.get("content", [])
        if not isinstance(content, list):
            errors.append(f"{prefix}: content must be a list")
        elif len(content) > self.MAX_CONTENT_BLOCKS:
            errors.append(
                f"{prefix}: too many content blocks (max {self.MAX_CONTENT_BLOCKS})"
            )
        else:
            for j, block in enumerate(content):
                block_errors = self._validate_content_block(
                    block, f"{prefix} block {j}"
                )
                errors.extend(block_errors)

        # Validate icon
        icon = page_data.get("icon")
        if icon and not isinstance(icon, str):
            errors.append(f"{prefix}: icon must be a string")

        # Validate cover
        cover = page_data.get("cover")
        if cover and not isinstance(cover, str):
            errors.append(f"{prefix}: cover must be a string")

        return errors

    def _validate_database_data(self, db_data: Dict[str, Any], index: int) -> List[str]:
        """
        Validate individual database data.

        Args:
            db_data: Database data dictionary
            index: Database index for error messages

        Returns:
            List of validation errors
        """
        errors = []
        prefix = f"Database {index}"

        if not isinstance(db_data, dict):
            errors.append(f"{prefix}: must be a dictionary")
            return errors

        # Validate title
        title = db_data.get("title", "").strip()
        if not title:
            errors.append(f"{prefix}: title is required")
        elif len(title) > self.MAX_TITLE_LENGTH:
            errors.append(
                f"{prefix}: title too long (max {self.MAX_TITLE_LENGTH} characters)"
            )

        # Validate description
        description = db_data.get("description", "")
        if (
            isinstance(description, str)
            and len(description) > self.MAX_DESCRIPTION_LENGTH
        ):
            errors.append(
                f"{prefix}: description too long (max {self.MAX_DESCRIPTION_LENGTH} characters)"
            )

        # Validate properties
        properties = db_data.get("properties", {})
        if not isinstance(properties, dict):
            errors.append(f"{prefix}: properties must be a dictionary")
        elif len(properties) > self.MAX_DATABASE_PROPERTIES:
            errors.append(
                f"{prefix}: too many properties (max {self.MAX_DATABASE_PROPERTIES})"
            )
        else:
            prop_errors = self._validate_database_properties(properties, prefix)
            errors.extend(prop_errors)

        return errors

    def _validate_database_properties(
        self, properties: Dict[str, Any], prefix: str
    ) -> List[str]:
        """
        Validate database properties.

        Args:
            properties: Properties dictionary
            prefix: Error message prefix

        Returns:
            List of validation errors
        """
        errors = []

        # Check for required title property
        has_title = False
        for prop_name, prop_config in properties.items():
            if not isinstance(prop_name, str) or not prop_name.strip():
                errors.append(f"{prefix}: property names must be non-empty strings")
                continue

            if len(prop_name) > self.MAX_PROPERTY_NAME_LENGTH:
                errors.append(f"{prefix}: property name '{prop_name}' too long")

            if not isinstance(prop_config, dict):
                errors.append(
                    f"{prefix}: property '{prop_name}' config must be a dictionary"
                )
                continue

            # Check property type
            if "title" in prop_config:
                has_title = True
            elif len(prop_config) == 1:
                prop_type = list(prop_config.keys())[0]
                if prop_type not in self.VALID_PROPERTY_TYPES:
                    errors.append(
                        f"{prefix}: invalid property type '{prop_type}' for '{prop_name}'"
                    )

                # Validate select options
                if prop_type in ["select", "multi_select"]:
                    options = prop_config[prop_type].get("options", [])
                    if len(options) > self.MAX_SELECT_OPTIONS:
                        errors.append(
                            f"{prefix}: too many options for '{prop_name}' (max {self.MAX_SELECT_OPTIONS})"
                        )

        if not has_title:
            errors.append(f"{prefix}: must have at least one title property")

        return errors

    def _validate_content_block(self, block: Dict[str, Any], prefix: str) -> List[str]:
        """
        Validate individual content block.

        Args:
            block: Content block dictionary
            prefix: Error message prefix

        Returns:
            List of validation errors
        """
        errors = []

        if not isinstance(block, dict):
            errors.append(f"{prefix}: must be a dictionary")
            return errors

        # Validate block type
        block_type = block.get("type")
        if not block_type:
            errors.append(f"{prefix}: type is required")
        elif block_type not in self.VALID_BLOCK_TYPES:
            errors.append(f"{prefix}: invalid block type '{block_type}'")

        # Validate block content structure
        if block_type and block_type in block:
            content = block[block_type]
            if not isinstance(content, dict):
                errors.append(f"{prefix}: content must be a dictionary")

            # Validate rich text for text blocks
            if block_type in [
                "paragraph",
                "heading_1",
                "heading_2",
                "heading_3",
                "bulleted_list_item",
                "numbered_list_item",
                "to_do",
            ]:
                if "rich_text" in content:
                    rich_text = content["rich_text"]
                    if not isinstance(rich_text, list):
                        errors.append(f"{prefix}: rich_text must be a list")

        return errors

    def _validate_metadata(self, metadata: Dict[str, Any]) -> List[str]:
        """
        Validate template metadata.

        Args:
            metadata: Metadata dictionary

        Returns:
            List of validation errors
        """
        errors = []

        # Validate generated_at
        generated_at = metadata.get("generated_at")
        if generated_at:
            try:
                datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
            except ValueError:
                errors.append("Invalid generated_at timestamp format")

        # Validate template_type
        template_type = metadata.get("template_type")
        if template_type and template_type not in self.VALID_TEMPLATE_TYPES:
            errors.append(f"Invalid template_type in metadata: {template_type}")

        return errors

    def sanitize_string(self, text: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize a string for safe use.

        Args:
            text: Input string
            max_length: Maximum allowed length

        Returns:
            Sanitized string
        """
        if not isinstance(text, str):
            text = str(text)

        # Remove potentially harmful characters
        text = re.sub(r"[<>]", "", text)

        # Trim whitespace
        text = text.strip()

        # Apply length limit
        if max_length and len(text) > max_length:
            text = text[:max_length].rstrip()

        return text

    def validate_api_response(
        self, response: Dict[str, Any], expected_fields: List[str]
    ) -> List[str]:
        """
        Validate API response structure.

        Args:
            response: API response dictionary
            expected_fields: List of expected fields

        Returns:
            List of validation errors
        """
        errors = []

        if not isinstance(response, dict):
            errors.append("API response must be a dictionary")
            return errors

        for field in expected_fields:
            if field not in response:
                errors.append(f"Missing required field: {field}")

        return errors

    def estimate_risk_level(self, user_input: Dict[str, Any]) -> str:
        """
        Estimate risk level of template generation based on input.

        Args:
            user_input: User input dictionary

        Returns:
            Risk level: 'low', 'medium', 'high'
        """
        risk_score = 0

        # Complex template types increase risk
        template_type = user_input.get("template_type", "")
        if template_type in ["enterprise", "complex"]:
            risk_score += 2

        # Many features increase risk
        features = user_input.get("features", [])
        risk_score += min(len(features), 3)

        # Many custom properties increase risk
        custom_props = user_input.get("custom_properties", {})
        risk_score += min(len(custom_props), 2)

        # Long descriptions might indicate complex requirements
        description = user_input.get("description", "")
        if len(description) > 200:
            risk_score += 1

        if risk_score <= 2:
            return "low"
        elif risk_score <= 4:
            return "medium"
        else:
            return "high"

    def __str__(self) -> str:
        """String representation of the validator."""
        return "TemplateValidator()"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return "TemplateValidator()"
