"""
Database model for the Notion Template Maker application.
Handles database configurations, properties, and operations.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field, validator
import uuid


class DatabaseProperty(BaseModel):
    """Represents a property in a Notion database."""

    id: str
    name: str
    type: str
    configuration: Dict[str, Any] = Field(default_factory=dict)

    @validator("type")
    def validate_property_type(cls, v):
        """Validate property type is supported by Notion."""
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
            raise ValueError(f"Unsupported property type: {v}")
        return v

    def to_notion_format(self) -> Dict[str, Any]:
        """Convert to Notion API format."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            self.type: self.configuration,
        }

    def get_select_options(self) -> List[Dict[str, Any]]:
        """Get select/multi_select options if applicable."""
        if self.type in ["select", "multi_select"]:
            return self.configuration.get("options", [])
        return []

    def add_select_option(self, name: str, color: str = "default"):
        """Add an option to select/multi_select property."""
        if self.type not in ["select", "multi_select"]:
            raise ValueError(f"Cannot add option to {self.type} property")

        options = self.configuration.setdefault("options", [])
        new_option = {"id": str(uuid.uuid4()), "name": name, "color": color}
        options.append(new_option)

    def remove_select_option(self, option_name: str):
        """Remove an option from select/multi_select property."""
        if self.type not in ["select", "multi_select"]:
            raise ValueError(f"Cannot remove option from {self.type} property")

        options = self.configuration.get("options", [])
        self.configuration["options"] = [
            opt for opt in options if opt["name"] != option_name
        ]


class DatabaseView(BaseModel):
    """Represents a view (filter/sort configuration) for a database."""

    id: str
    name: str
    type: str = "table"  # 'table', 'board', 'list', 'calendar', 'gallery', 'timeline'
    query2: Dict[str, Any] = Field(default_factory=dict)  # Notion's view query format

    @validator("type")
    def validate_view_type(cls, v):
        """Validate view type is supported."""
        valid_types = {"table", "board", "list", "calendar", "gallery", "timeline"}
        if v not in valid_types:
            raise ValueError(f"Unsupported view type: {v}")
        return v

    def set_sort(self, property_name: str, direction: str = "ascending"):
        """Set sorting for the view."""
        if "sort" not in self.query2:
            self.query2["sort"] = []

        # Remove existing sort for this property
        self.query2["sort"] = [
            s for s in self.query2["sort"] if s.get("property") != property_name
        ]

        # Add new sort
        self.query2["sort"].append({"property": property_name, "direction": direction})

    def add_filter(self, property_name: str, filter_type: str, value: Any):
        """Add a filter to the view."""
        if "filter" not in self.query2:
            self.query2["filter"] = {"and": []}

        filter_condition = {"property": property_name, filter_type: value}

        if isinstance(self.query2["filter"], dict) and "and" in self.query2["filter"]:
            self.query2["filter"]["and"].append(filter_condition)
        else:
            # Simple filter case
            self.query2["filter"] = filter_condition


class Database(BaseModel):
    """Represents a Notion database with full configuration."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    notion_id: Optional[str] = None  # Notion's internal ID
    title: str
    description: Optional[str] = None

    # Properties
    properties: List[DatabaseProperty] = Field(default_factory=list)

    # Views
    views: List[DatabaseView] = Field(default_factory=list)

    # Parent information
    parent_type: str = "workspace"  # 'workspace', 'page_id', 'database_id'
    parent_id: Optional[str] = None

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by_user_id: Optional[str] = None
    url: Optional[str] = None

    # Template-specific fields
    is_template: bool = False
    template_category: Optional[str] = None

    def add_property(
        self, name: str, prop_type: str, configuration: Optional[Dict[str, Any]] = None
    ) -> DatabaseProperty:
        """Add a property to the database."""
        if configuration is None:
            configuration = {}

        # Generate ID for the property
        prop_id = str(uuid.uuid4())

        property_obj = DatabaseProperty(
            id=prop_id, name=name, type=prop_type, configuration=configuration
        )

        self.properties.append(property_obj)
        self.updated_at = datetime.utcnow()
        return property_obj

    def get_property(self, property_id: str) -> Optional[DatabaseProperty]:
        """Get a property by ID."""
        for prop in self.properties:
            if prop.id == property_id:
                return prop
        return None

    def get_property_by_name(self, name: str) -> Optional[DatabaseProperty]:
        """Get a property by name."""
        for prop in self.properties:
            if prop.name == name:
                return prop
        return None

    def remove_property(self, property_id: str) -> bool:
        """Remove a property by ID."""
        original_length = len(self.properties)
        self.properties = [p for p in self.properties if p.id != property_id]

        if len(self.properties) < original_length:
            self.updated_at = datetime.utcnow()
            return True
        return False

    def add_view(self, name: str, view_type: str = "table") -> DatabaseView:
        """Add a view to the database."""
        view_id = str(uuid.uuid4())
        view = DatabaseView(id=view_id, name=name, type=view_type)
        self.views.append(view)
        self.updated_at = datetime.utcnow()
        return view

    def get_view(self, view_id: str) -> Optional[DatabaseView]:
        """Get a view by ID."""
        for view in self.views:
            if view.id == view_id:
                return view
        return None

    def has_title_property(self) -> bool:
        """Check if database has a title property (required for Notion databases)."""
        return any(prop.type == "title" for prop in self.properties)

    def ensure_title_property(self):
        """Ensure database has at least one title property."""
        if not self.has_title_property():
            self.add_property("Name", "title")

    def get_property_names(self) -> List[str]:
        """Get list of all property names."""
        return [prop.name for prop in self.properties]

    def get_properties_by_type(self, prop_type: str) -> List[DatabaseProperty]:
        """Get all properties of a specific type."""
        return [prop for prop in self.properties if prop.type == prop_type]

    def to_notion_format(self) -> Dict[str, Any]:
        """Convert to Notion API format for database creation."""
        # Ensure we have a title property
        self.ensure_title_property()

        properties = {}
        for prop in self.properties:
            properties[prop.name] = {"type": prop.type, prop.type: prop.configuration}

        notion_db = {
            "title": [{"text": {"content": self.title}}],
            "properties": properties,
        }

        if self.description:
            notion_db["description"] = [{"text": {"content": self.description}}]

        # Set parent
        if self.parent_id:
            if self.parent_type == "page_id":
                notion_db["parent"] = {"type": "page_id", "page_id": self.parent_id}
            elif self.parent_type == "database_id":
                notion_db["parent"] = {
                    "type": "database_id",
                    "database_id": self.parent_id,
                }
        else:
            notion_db["parent"] = {"type": "workspace", "workspace": True}

        return notion_db

    def validate_database(self) -> List[str]:
        """Validate database configuration and return list of errors."""
        errors = []

        if not self.title.strip():
            errors.append("Database title cannot be empty")

        if not self.has_title_property():
            errors.append("Database must have at least one title property")

        # Validate property configurations
        for prop in self.properties:
            if not prop.name.strip():
                errors.append(f"Property has empty name")

            # Validate select/multi_select options
            if prop.type in ["select", "multi_select"]:
                options = prop.configuration.get("options", [])
                if not options:
                    errors.append(
                        f"Property '{prop.name}' of type {prop.type} must have at least one option"
                    )

                # Check for duplicate option names
                option_names = [opt.get("name", "").strip() for opt in options]
                if len(option_names) != len(set(option_names)):
                    errors.append(f"Property '{prop.name}' has duplicate option names")

        return errors

    def clone(self) -> "Database":
        """Create a deep copy of the database."""
        # Create new database with same configuration
        cloned = Database(
            title=f"{self.title} (Copy)",
            description=self.description,
            parent_type=self.parent_type,
            parent_id=self.parent_id,
            is_template=self.is_template,
            template_category=self.template_category,
        )

        # Clone properties
        for prop in self.properties:
            cloned.add_property(prop.name, prop.type, prop.configuration.copy())

        # Clone views
        for view in self.views:
            cloned_view = cloned.add_view(view.name, view.type)
            cloned_view.query2 = view.query2.copy()

        return cloned

    def __str__(self) -> str:
        """String representation of the database."""
        return f"Database(title={self.title!r}, properties={len(self.properties)}, views={len(self.views)})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return (
            f"Database(id={self.id!r}, title={self.title!r}, "
            f"properties={len(self.properties)}, views={len(self.views)}, "
            f"notion_id={self.notion_id!r})"
        )
