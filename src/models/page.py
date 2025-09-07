"""
Page model for the Notion Template Maker application.
Handles Notion page configurations, content blocks, and operations.
"""

from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from pydantic import BaseModel, Field, validator
import uuid


class PageProperty(BaseModel):
    """Represents a property value in a Notion page."""

    id: str
    name: str
    type: str
    value: Any

    def to_notion_format(self) -> Dict[str, Any]:
        """Convert to Notion API format."""
        if self.type == "title":
            return {"title": [{"text": {"content": str(self.value)}}]}
        elif self.type == "rich_text":
            return {"rich_text": [{"text": {"content": str(self.value)}}]}
        elif self.type in ["select", "multi_select"]:
            return {self.type: {"name": str(self.value)}}
        elif self.type == "number":
            return {"number": self.value}
        elif self.type == "checkbox":
            return {"checkbox": bool(self.value)}
        elif self.type == "date":
            return {
                "date": {
                    "start": self.value.isoformat()
                    if isinstance(self.value, datetime)
                    else str(self.value)
                }
            }
        elif self.type == "url":
            return {"url": str(self.value)}
        elif self.type == "email":
            return {"email": str(self.value)}
        elif self.type == "phone_number":
            return {"phone_number": str(self.value)}
        else:
            # For other types, return as-is
            return {self.type: self.value}


class ContentBlock(BaseModel):
    """Represents a content block in a Notion page."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str
    content: Dict[str, Any]

    @validator("type")
    def validate_block_type(cls, v):
        """Validate block type is supported by Notion."""
        valid_types = {
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
        if v not in valid_types:
            raise ValueError(f"Unsupported block type: {v}")
        return v

    def to_notion_format(self) -> Dict[str, Any]:
        """Convert to Notion API format."""
        return {"object": "block", "type": self.type, self.type: self.content}


class Page(BaseModel):
    """Represents a Notion page with full configuration."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    notion_id: Optional[str] = None  # Notion's internal ID
    title: str
    icon: Optional[str] = None
    cover: Optional[str] = None

    # Properties
    properties: List[PageProperty] = Field(default_factory=list)

    # Content blocks
    content_blocks: List[ContentBlock] = Field(default_factory=list)

    # Parent information
    parent_type: str = "workspace"  # 'workspace', 'page_id', 'database_id'
    parent_id: Optional[str] = None

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by_user_id: Optional[str] = None
    url: Optional[str] = None
    archived: bool = False

    # Template-specific fields
    is_template: bool = False
    template_category: Optional[str] = None

    def add_property(self, name: str, prop_type: str, value: Any) -> PageProperty:
        """Add a property to the page."""
        prop_id = str(uuid.uuid4())
        property_obj = PageProperty(id=prop_id, name=name, type=prop_type, value=value)
        self.properties.append(property_obj)
        self.updated_at = datetime.utcnow()
        return property_obj

    def get_property(self, property_id: str) -> Optional[PageProperty]:
        """Get a property by ID."""
        for prop in self.properties:
            if prop.id == property_id:
                return prop
        return None

    def get_property_by_name(self, name: str) -> Optional[PageProperty]:
        """Get a property by name."""
        for prop in self.properties:
            if prop.name == name:
                return prop
        return None

    def update_property_value(self, property_id: str, new_value: Any) -> bool:
        """Update a property value."""
        prop = self.get_property(property_id)
        if prop:
            prop.value = new_value
            self.updated_at = datetime.utcnow()
            return True
        return False

    def remove_property(self, property_id: str) -> bool:
        """Remove a property by ID."""
        original_length = len(self.properties)
        self.properties = [p for p in self.properties if p.id != property_id]

        if len(self.properties) < original_length:
            self.updated_at = datetime.utcnow()
            return True
        return False

    def add_content_block(
        self, block_type: str, content: Dict[str, Any]
    ) -> ContentBlock:
        """Add a content block to the page."""
        block = ContentBlock(type=block_type, content=content)
        self.content_blocks.append(block)
        self.updated_at = datetime.utcnow()
        return block

    def add_paragraph(
        self, text: str, annotations: Optional[Dict[str, Any]] = None
    ) -> ContentBlock:
        """Add a paragraph block."""
        content = {
            "rich_text": [{"text": {"content": text}, "annotations": annotations or {}}]
        }
        return self.add_content_block("paragraph", content)

    def add_heading(self, text: str, level: int = 1) -> ContentBlock:
        """Add a heading block."""
        if level not in [1, 2, 3]:
            raise ValueError("Heading level must be 1, 2, or 3")

        block_type = f"heading_{level}"
        content = {"rich_text": [{"text": {"content": text}}]}
        return self.add_content_block(block_type, content)

    def add_list_item(self, text: str, list_type: str = "bulleted") -> ContentBlock:
        """Add a list item block."""
        if list_type not in ["bulleted", "numbered"]:
            raise ValueError("List type must be 'bulleted' or 'numbered'")

        block_type = f"{list_type}_list_item"
        content = {"rich_text": [{"text": {"content": text}}]}
        return self.add_content_block(block_type, content)

    def add_to_do(self, text: str, checked: bool = False) -> ContentBlock:
        """Add a to-do block."""
        content = {"rich_text": [{"text": {"content": text}}], "checked": checked}
        return self.add_content_block("to_do", content)

    def add_code_block(self, code: str, language: str = "python") -> ContentBlock:
        """Add a code block."""
        content = {"rich_text": [{"text": {"content": code}}], "language": language}
        return self.add_content_block("code", content)

    def add_image(self, url: str, caption: Optional[str] = None) -> ContentBlock:
        """Add an image block."""
        content = {"type": "external", "external": {"url": url}}
        if caption:
            content["caption"] = [{"text": {"content": caption}}]
        return self.add_content_block("image", content)

    def add_divider(self) -> ContentBlock:
        """Add a divider block."""
        return self.add_content_block("divider", {})

    def get_content_block(self, block_id: str) -> Optional[ContentBlock]:
        """Get a content block by ID."""
        for block in self.content_blocks:
            if block.id == block_id:
                return block
        return None

    def remove_content_block(self, block_id: str) -> bool:
        """Remove a content block by ID."""
        original_length = len(self.content_blocks)
        self.content_blocks = [b for b in self.content_blocks if b.id != block_id]

        if len(self.content_blocks) < original_length:
            self.updated_at = datetime.utcnow()
            return True
        return False

    def insert_content_block(
        self, index: int, block_type: str, content: Dict[str, Any]
    ) -> ContentBlock:
        """Insert a content block at a specific index."""
        block = ContentBlock(type=block_type, content=content)
        self.content_blocks.insert(index, block)
        self.updated_at = datetime.utcnow()
        return block

    def to_notion_format(self) -> Dict[str, Any]:
        """Convert to Notion API format for page creation."""
        notion_page = {
            "properties": {},
            "children": [block.to_notion_format() for block in self.content_blocks],
        }

        # Add title property
        notion_page["properties"]["title"] = {
            "title": [{"text": {"content": self.title}}]
        }

        # Add other properties
        for prop in self.properties:
            notion_page["properties"][prop.name] = prop.to_notion_format()

        # Add icon if present
        if self.icon:
            notion_page["icon"] = {"type": "emoji", "emoji": self.icon}

        # Add cover if present
        if self.cover:
            notion_page["cover"] = {"type": "external", "external": {"url": self.cover}}

        # Set parent
        if self.parent_id:
            if self.parent_type == "page_id":
                notion_page["parent"] = {"type": "page_id", "page_id": self.parent_id}
            elif self.parent_type == "database_id":
                notion_page["parent"] = {
                    "type": "database_id",
                    "database_id": self.parent_id,
                }
        else:
            notion_page["parent"] = {"type": "workspace", "workspace": True}

        return notion_page

    def validate_page(self) -> List[str]:
        """Validate page configuration and return list of errors."""
        errors = []

        if not self.title.strip():
            errors.append("Page title cannot be empty")

        # Validate content blocks
        for i, block in enumerate(self.content_blocks):
            if block.type in [
                "heading_1",
                "heading_2",
                "heading_3",
                "paragraph",
                "bulleted_list_item",
                "numbered_list_item",
                "to_do",
            ]:
                rich_text = block.content.get("rich_text", [])
                if not rich_text:
                    errors.append(
                        f"Block {i+1} ({block.type}) has no rich text content"
                    )

        return errors

    def clone(self) -> "Page":
        """Create a deep copy of the page."""
        # Create new page with same configuration
        cloned = Page(
            title=f"{self.title} (Copy)",
            icon=self.icon,
            cover=self.cover,
            parent_type=self.parent_type,
            parent_id=self.parent_id,
            is_template=self.is_template,
            template_category=self.template_category,
        )

        # Clone properties
        for prop in self.properties:
            cloned.add_property(prop.name, prop.type, prop.value)

        # Clone content blocks
        for block in self.content_blocks:
            cloned.add_content_block(block.type, block.content.copy())

        return cloned

    def get_plain_text_content(self) -> str:
        """Extract plain text content from all blocks."""
        text_parts = []

        for block in self.content_blocks:
            if "rich_text" in block.content:
                for rich_text_item in block.content["rich_text"]:
                    if "text" in rich_text_item and "content" in rich_text_item["text"]:
                        text_parts.append(rich_text_item["text"]["content"])

        return "\n".join(text_parts)

    def __str__(self) -> str:
        """String representation of the page."""
        return f"Page(title={self.title!r}, properties={len(self.properties)}, blocks={len(self.content_blocks)})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return (
            f"Page(id={self.id!r}, title={self.title!r}, "
            f"properties={len(self.properties)}, blocks={len(self.content_blocks)}, "
            f"notion_id={self.notion_id!r})"
        )
