"""
Template model for the Notion Template Maker application.
Handles template definitions, configurations, and metadata.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator
import uuid
import json


class TemplateProperty(BaseModel):
    """Represents a property in a Notion database."""

    name: str
    type: str  # 'title', 'rich_text', 'number', 'select', 'multi_select', 'date', 'people', 'files', 'checkbox', 'url', 'email', 'phone_number'
    config: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("type")
    @classmethod
    def validate_property_type(cls, v):
        """Validate property type is supported."""
        valid_types = {
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
        if v not in valid_types:
            raise ValueError(f"Invalid property type: {v}")
        return v

    def to_notion_format(self) -> Dict[str, Any]:
        """Convert to Notion API format."""
        notion_config = {self.type: self.config}
        return notion_config


class TemplateDatabase(BaseModel):
    """Represents a Notion database in a template."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: Optional[str] = None
    properties: List[TemplateProperty] = Field(default_factory=list)
    parent_page_id: Optional[str] = None
    is_inline: bool = False

    def add_property(
        self, name: str, prop_type: str, config: Optional[Dict[str, Any]] = None
    ):
        """Add a property to the database."""
        if config is None:
            config = {}
        property_obj = TemplateProperty(name=name, type=prop_type, config=config)
        self.properties.append(property_obj)

    def get_property(self, name: str) -> Optional[TemplateProperty]:
        """Get a property by name."""
        for prop in self.properties:
            if prop.name == name:
                return prop
        return None

    def to_notion_format(self) -> Dict[str, Any]:
        """Convert to Notion API format for database creation."""
        properties = {}
        for prop in self.properties:
            properties[prop.name] = prop.to_notion_format()

        notion_db = {
            "title": [{"text": {"content": self.title}}],
            "properties": properties,
        }

        if self.parent_page_id:
            notion_db["parent"] = {"type": "page_id", "page_id": self.parent_page_id}
        else:
            notion_db["parent"] = {"type": "workspace", "workspace": True}

        return notion_db


class TemplatePage(BaseModel):
    """Represents a Notion page in a template."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: List[Dict[str, Any]] = Field(default_factory=list)
    icon: Optional[str] = None
    cover: Optional[str] = None
    parent_page_id: Optional[str] = None

    def add_content_block(self, block_type: str, content: Dict[str, Any]):
        """Add a content block to the page."""
        block = {"object": "block", "type": block_type, block_type: content}
        self.content.append(block)

    def to_notion_format(self) -> Dict[str, Any]:
        """Convert to Notion API format for page creation."""
        notion_page = {
            "properties": {"title": {"title": [{"text": {"content": self.title}}]}},
            "children": self.content,
        }

        if self.icon:
            notion_page["icon"] = {"type": "emoji", "emoji": self.icon}

        if self.cover:
            notion_page["cover"] = {"type": "external", "external": {"url": self.cover}}

        if self.parent_page_id:
            notion_page["parent"] = {"type": "page_id", "page_id": self.parent_page_id}
        else:
            notion_page["parent"] = {"type": "workspace", "workspace": True}

        return notion_page


class Template(BaseModel):
    """Main template model containing pages and databases."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = None
    title: Optional[str] = None  # Alias for name for backward compatibility
    description: Optional[str] = None
    category: str = "general"  # 'general', 'project_management', 'knowledge_base', 'personal', 'business'
    version: str = "1.0.0"
    author: Optional[str] = None

    # Template content
    pages: List[TemplatePage] = Field(default_factory=list)
    databases: List[TemplateDatabase] = Field(default_factory=list)
    sections: List[Dict[str, Any]] = Field(
        default_factory=list
    )  # For backward compatibility
    properties: List[Dict[str, Any]] = Field(
        default_factory=list
    )  # For backward compatibility

    # Metadata
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_public: bool = False
    usage_count: int = 0

    # Template configuration
    config: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("category")
    @classmethod
    def validate_category(cls, v):
        """Validate template category."""
        valid_categories = {
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
        }
        if v not in valid_categories:
            raise ValueError(f"Invalid category: {v}")
        return v

    @field_validator("updated_at", mode="before")
    @classmethod
    def set_updated_at(cls, v):
        """Automatically set updated_at on model changes."""
        return datetime.now(timezone.utc)

    @field_validator("name", mode="before")
    @classmethod
    def set_name_from_title(cls, v, info):
        """Set name from title if name is not provided."""
        if v is None:
            title = info.data.get("title")
            if title:
                return title
        return v

    def add_page(self, title: str, **kwargs) -> TemplatePage:
        """Add a page to the template."""
        page = TemplatePage(title=title, **kwargs)
        self.pages.append(page)
        return page

    def add_database(self, title: str, **kwargs) -> TemplateDatabase:
        """Add a database to the template."""
        database = TemplateDatabase(title=title, **kwargs)
        self.databases.append(database)
        return database

    def get_page(self, page_id: str) -> Optional[TemplatePage]:
        """Get a page by ID."""
        for page in self.pages:
            if page.id == page_id:
                return page
        return None

    def get_database(self, database_id: str) -> Optional[TemplateDatabase]:
        """Get a database by ID."""
        for database in self.databases:
            if database.id == database_id:
                return database
        return None

    def increment_usage(self):
        """Increment usage count."""
        self.usage_count += 1
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Template":
        """Create template from dictionary."""
        return cls.model_validate(data)

    def to_json(self) -> str:
        """Convert template to JSON string."""
        return self.model_dump_json(indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "Template":
        """Create template from JSON string."""
        return cls.model_validate_json(json_str)

    def validate_template(self) -> List[str]:
        """Validate template structure and return list of errors."""
        errors = []

        if not self.name.strip():
            errors.append("Template name cannot be empty")

        if not self.pages and not self.databases:
            errors.append("Template must contain at least one page or database")

        # Validate pages
        for i, page in enumerate(self.pages):
            if not page.title.strip():
                errors.append(f"Page {i+1} has empty title")

        # Validate databases
        for i, database in enumerate(self.databases):
            if not database.title.strip():
                errors.append(f"Database {i+1} has empty title")

            # Check for required Name/Title property
            has_title_prop = any(prop.type == "title" for prop in database.properties)
            if not has_title_prop:
                errors.append(
                    f"Database '{database.title}' missing required title property"
                )

        return errors

    def __str__(self) -> str:
        """String representation of the template."""
        return f"Template(name={self.name!r}, category={self.category}, pages={len(self.pages)}, databases={len(self.databases)})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return (
            f"Template(id={self.id!r}, name={self.name!r}, category={self.category!r}, "
            f"version={self.version!r}, pages={len(self.pages)}, databases={len(self.databases)})"
        )


class TemplateCollection(BaseModel):
    """Collection of templates with search and filtering capabilities."""

    templates: List[Template] = Field(default_factory=list)

    def add_template(self, template: Template):
        """Add a template to the collection."""
        self.templates.append(template)

    def get_template(self, template_id: str) -> Optional[Template]:
        """Get a template by ID."""
        for template in self.templates:
            if template.id == template_id:
                return template
        return None

    def search_templates(
        self, query: str, category: Optional[str] = None
    ) -> List[Template]:
        """Search templates by name, description, or tags."""
        results = []
        query_lower = query.lower()

        for template in self.templates:
            if category and template.category != category:
                continue

            # Search in name, description, and tags
            searchable_text = f"{template.name} {template.description or ''} {' '.join(template.tags)}".lower()

            if query_lower in searchable_text:
                results.append(template)

        return results

    def get_templates_by_category(self, category: str) -> List[Template]:
        """Get all templates in a specific category."""
        return [t for t in self.templates if t.category == category]

    def get_popular_templates(self, limit: int = 10) -> List[Template]:
        """Get most popular templates by usage count."""
        return sorted(self.templates, key=lambda t: t.usage_count, reverse=True)[:limit]
