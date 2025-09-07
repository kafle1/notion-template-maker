"""
User model for the Notion Template Maker application.
Handles user data, authentication, and session management.
"""

from typing import Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator, ConfigDict
import uuid


class User(BaseModel):
    """User model representing an application user."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: Optional[str] = None
    name: Optional[str] = None

    # API Keys (encrypted in production)
    openrouter_api_key: Optional[str] = None
    notion_access_token: Optional[str] = None
    notion_refresh_token: Optional[str] = None

    # OAuth state
    notion_oauth_state: Optional[str] = None
    notion_workspace_id: Optional[str] = None

    # Session data
    session_id: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # User preferences
    preferences: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        """Validate email format."""
        if v is not None:
            import re

            # More comprehensive email validation
            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_pattern, v) or ".." in v:
                raise ValueError("Invalid email format")
        return v

    @field_validator("updated_at", mode="before")
    @classmethod
    def set_updated_at(cls, v):
        """Automatically set updated_at on model changes."""
        return datetime.now(timezone.utc)

    def has_valid_openrouter_key(self) -> bool:
        """Check if user has a valid OpenRouter API key."""
        return (
            self.openrouter_api_key is not None
            and len(self.openrouter_api_key.strip()) > 0
        )

    def has_valid_notion_token(self) -> bool:
        """Check if user has a valid Notion access token."""
        return (
            self.notion_access_token is not None
            and len(self.notion_access_token.strip()) > 0
        )

    def is_authenticated(self) -> bool:
        """Check if user is fully authenticated with both APIs."""
        return self.has_valid_openrouter_key() and self.has_valid_notion_token()

    def update_api_keys(
        self, openrouter_key: Optional[str] = None, notion_token: Optional[str] = None
    ):
        """Update API keys and mark as updated."""
        if openrouter_key is not None:
            self.openrouter_api_key = openrouter_key
        if notion_token is not None:
            self.notion_access_token = notion_token
        self.updated_at = datetime.utcnow()

    def set_notion_oauth_data(
        self,
        access_token: str,
        refresh_token: Optional[str] = None,
        workspace_id: Optional[str] = None,
    ):
        """Set Notion OAuth data after successful authentication."""
        self.notion_access_token = access_token
        if refresh_token:
            self.notion_refresh_token = refresh_token
        if workspace_id:
            self.notion_workspace_id = workspace_id
        self.updated_at = datetime.utcnow()

    def clear_notion_auth(self):
        """Clear Notion authentication data."""
        self.notion_access_token = None
        self.notion_refresh_token = None
        self.notion_workspace_id = None
        self.notion_oauth_state = None
        self.updated_at = datetime.utcnow()

    def start_session(self, session_id: str):
        """Start a new user session."""
        self.session_id = session_id
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def end_session(self):
        """End the current user session."""
        self.session_id = None
        self.updated_at = datetime.now(timezone.utc)

    def update_preferences(self, preferences: Dict[str, Any]):
        """Update user preferences."""
        self.preferences.update(preferences)
        self.updated_at = datetime.now(timezone.utc)

    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a user preference value."""
        return self.preferences.get(key, default)

    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert user to dictionary, optionally including sensitive data."""
        data = self.model_dump()

        if not include_sensitive:
            # Remove sensitive information
            sensitive_fields = [
                "openrouter_api_key",
                "notion_access_token",
                "notion_refresh_token",
            ]
            for field in sensitive_fields:
                if field in data:
                    data[field] = "***" if data[field] else None

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Create user from dictionary."""
        return cls.model_validate(data)

    def __str__(self) -> str:
        """String representation of the user."""
        return f"User(id={self.id}, email={self.email}, authenticated={self.is_authenticated()})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return (
            f"User(id={self.id!r}, email={self.email!r}, "
            f"name={self.name!r}, authenticated={self.is_authenticated()})"
        )


class UserSession:
    """Helper class for managing user sessions."""

    def __init__(self, user: User):
        self.user = user
        self.created_at = datetime.utcnow()
        self.last_activity = datetime.utcnow()

    def update_activity(self):
        """Update last activity timestamp."""
        self.last_activity = datetime.utcnow()

    def is_expired(self, max_age_seconds: int = 3600) -> bool:
        """Check if session has expired."""
        return (
            datetime.utcnow() - self.last_activity
        ).total_seconds() > max_age_seconds

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary."""
        return {
            "user_id": self.user.id,
            "session_id": self.user.session_id,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "is_expired": self.is_expired(),
        }
