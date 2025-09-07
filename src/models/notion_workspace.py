"""
NotionWorkspace model for the Notion Template Maker application.
Handles Notion workspace data, pages, databases, and user permissions.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field, validator
import uuid


class NotionUser(BaseModel):
    """Represents a Notion user."""

    id: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    type: str = "person"  # 'person' or 'bot'
    person: Optional[Dict[str, Any]] = None
    bot: Optional[Dict[str, Any]] = None

    def is_bot(self) -> bool:
        """Check if user is a bot."""
        return self.type == "bot"

    def get_display_name(self) -> str:
        """Get display name for the user."""
        if self.name:
            return self.name
        if self.person and "email" in self.person:
            return self.person["email"]
        return f"User {self.id[:8]}"


class NotionPage(BaseModel):
    """Represents a Notion page."""

    id: str
    title: str
    url: str
    created_time: datetime
    last_edited_time: datetime
    created_by: NotionUser
    last_edited_by: NotionUser
    parent_type: str  # 'workspace', 'page_id', 'database_id'
    parent_id: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    archived: bool = False

    @validator("created_time", "last_edited_time", pre=True)
    def parse_datetime(cls, v):
        """Parse datetime strings to datetime objects."""
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v

    def get_property_value(self, property_name: str) -> Any:
        """Get a property value by name."""
        return self.properties.get(property_name)

    def has_property(self, property_name: str) -> bool:
        """Check if page has a specific property."""
        return property_name in self.properties

    def is_child_of(self, parent_id: str) -> bool:
        """Check if page is a child of the given parent."""
        return self.parent_id == parent_id


class NotionDatabase(BaseModel):
    """Represents a Notion database."""

    id: str
    title: str
    url: str
    created_time: datetime
    last_edited_time: datetime
    created_by: NotionUser
    last_edited_by: NotionUser
    parent_type: str
    parent_id: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    archived: bool = False

    @validator("created_time", "last_edited_time", pre=True)
    def parse_datetime(cls, v):
        """Parse datetime strings to datetime objects."""
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v

    def get_property(self, property_name: str) -> Optional[Dict[str, Any]]:
        """Get a property definition by name."""
        return self.properties.get(property_name)

    def has_property(self, property_name: str) -> bool:
        """Check if database has a specific property."""
        return property_name in self.properties

    def get_property_names(self) -> List[str]:
        """Get list of all property names."""
        return list(self.properties.keys())

    def get_property_types(self) -> Dict[str, str]:
        """Get mapping of property names to their types."""
        return {
            name: prop.get("type", "unknown") for name, prop in self.properties.items()
        }


class NotionWorkspace(BaseModel):
    """Represents a Notion workspace."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = None
    icon: Optional[str] = None
    cover: Optional[str] = None

    # Content
    pages: List[NotionPage] = Field(default_factory=list)
    databases: List[NotionDatabase] = Field(default_factory=list)

    # Users and permissions
    users: List[NotionUser] = Field(default_factory=list)
    owner: Optional[NotionUser] = None

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_synced: Optional[datetime] = None

    # Access token (for API operations)
    access_token: Optional[str] = None

    def add_page(self, page: NotionPage):
        """Add a page to the workspace."""
        # Remove existing page with same ID if present
        self.pages = [p for p in self.pages if p.id != page.id]
        self.pages.append(page)
        self.updated_at = datetime.utcnow()

    def add_database(self, database: NotionDatabase):
        """Add a database to the workspace."""
        # Remove existing database with same ID if present
        self.databases = [d for d in self.databases if d.id != database.id]
        self.databases.append(database)
        self.updated_at = datetime.utcnow()

    def add_user(self, user: NotionUser):
        """Add a user to the workspace."""
        # Remove existing user with same ID if present
        self.users = [u for u in self.users if u.id != user.id]
        self.users.append(user)
        self.updated_at = datetime.utcnow()

    def get_page(self, page_id: str) -> Optional[NotionPage]:
        """Get a page by ID."""
        for page in self.pages:
            if page.id == page_id:
                return page
        return None

    def get_database(self, database_id: str) -> Optional[NotionDatabase]:
        """Get a database by ID."""
        for database in self.databases:
            if database.id == database_id:
                return database
        return None

    def get_user(self, user_id: str) -> Optional[NotionUser]:
        """Get a user by ID."""
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def get_pages_by_parent(self, parent_id: str) -> List[NotionPage]:
        """Get all pages that are children of the given parent."""
        return [page for page in self.pages if page.parent_id == parent_id]

    def get_databases_by_parent(self, parent_id: str) -> List[NotionDatabase]:
        """Get all databases that are children of the given parent."""
        return [
            database for database in self.databases if database.parent_id == parent_id
        ]

    def get_root_pages(self) -> List[NotionPage]:
        """Get all pages at the workspace root level."""
        return [page for page in self.pages if page.parent_type == "workspace"]

    def get_root_databases(self) -> List[NotionDatabase]:
        """Get all databases at the workspace root level."""
        return [
            database
            for database in self.databases
            if database.parent_type == "workspace"
        ]

    def search_pages(self, query: str) -> List[NotionPage]:
        """Search pages by title."""
        query_lower = query.lower()
        return [page for page in self.pages if query_lower in page.title.lower()]

    def search_databases(self, query: str) -> List[NotionDatabase]:
        """Search databases by title."""
        query_lower = query.lower()
        return [
            database
            for database in self.databases
            if query_lower in database.title.lower()
        ]

    def get_workspace_stats(self) -> Dict[str, int]:
        """Get workspace statistics."""
        return {
            "total_pages": len(self.pages),
            "total_databases": len(self.databases),
            "total_users": len(self.users),
            "archived_pages": len([p for p in self.pages if p.archived]),
            "archived_databases": len([d for d in self.databases if d.archived]),
        }

    def mark_synced(self):
        """Mark workspace as recently synced."""
        self.last_synced = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def is_synced_recently(self, max_age_minutes: int = 30) -> bool:
        """Check if workspace was synced recently."""
        if not self.last_synced:
            return False
        age_minutes = (datetime.utcnow() - self.last_synced).total_seconds() / 60
        return age_minutes <= max_age_minutes

    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert workspace to dictionary."""
        data = self.dict()

        if not include_sensitive:
            # Remove sensitive information
            if "access_token" in data:
                data["access_token"] = "***" if data["access_token"] else None

        return data

    def __str__(self) -> str:
        """String representation of the workspace."""
        stats = self.get_workspace_stats()
        return (
            f"NotionWorkspace(name={self.name!r}, "
            f"pages={stats['total_pages']}, databases={stats['total_databases']}, "
            f"users={stats['total_users']})"
        )

    def __repr__(self) -> str:
        """Detailed string representation."""
        return (
            f"NotionWorkspace(id={self.id!r}, name={self.name!r}, "
            f"pages={len(self.pages)}, databases={len(self.databases)}, "
            f"users={len(self.users)}, last_synced={self.last_synced})"
        )


class WorkspaceSyncResult(BaseModel):
    """Result of a workspace synchronization operation."""

    workspace_id: str
    success: bool
    synced_at: datetime = Field(default_factory=datetime.utcnow)
    pages_synced: int = 0
    databases_synced: int = 0
    users_synced: int = 0
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    def add_error(self, error: str):
        """Add an error message."""
        self.errors.append(error)
        self.success = False

    def add_warning(self, warning: str):
        """Add a warning message."""
        self.warnings.append(warning)

    def increment_pages(self, count: int = 1):
        """Increment pages synced count."""
        self.pages_synced += count

    def increment_databases(self, count: int = 1):
        """Increment databases synced count."""
        self.databases_synced += count

    def increment_users(self, count: int = 1):
        """Increment users synced count."""
        self.users_synced += count

    def get_summary(self) -> Dict[str, Any]:
        """Get synchronization summary."""
        return {
            "success": self.success,
            "synced_at": self.synced_at.isoformat(),
            "pages_synced": self.pages_synced,
            "databases_synced": self.databases_synced,
            "users_synced": self.users_synced,
            "total_items": self.pages_synced
            + self.databases_synced
            + self.users_synced,
            "errors_count": len(self.errors),
            "warnings_count": len(self.warnings),
        }
