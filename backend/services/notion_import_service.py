"""
Notion import service for the Notion Template Maker application.
Handles importing generated templates into Notion workspaces.
"""

from typing import Optional, Dict, Any, List, Tuple
import json
from datetime import datetime
from backend.clients.notion_client import NotionClient


class NotionImportService:
    """Service for importing templates into Notion."""

    def __init__(self, notion_client: Optional[NotionClient] = None):
        """
        Initialize the Notion import service.

        Args:
            notion_client: Notion API client
        """
        self.notion_client = notion_client

    def set_client(self, notion_client: NotionClient):
        """Set the Notion API client."""
        self.notion_client = notion_client

    def import_template(
        self,
        template_data: Dict[str, Any],
        workspace_id: Optional[str] = None,
        parent_page_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Import a complete template into Notion.

        Args:
            template_data: Generated template data with pages and databases
            workspace_id: Target workspace ID (optional)
            parent_page_id: Parent page ID for the template (optional)

        Returns:
            Import results with created page/database IDs

        Raises:
            ValueError: If Notion client is not set or template data is invalid
        """
        if not self.notion_client:
            raise ValueError("Notion client not set")

        if not isinstance(template_data, dict):
            raise ValueError("Template data must be a dictionary")

        results = {
            "success": True,
            "created_pages": [],
            "created_databases": [],
            "errors": [],
            "metadata": {
                "imported_at": datetime.now().isoformat(),
                "template_type": template_data.get("metadata", {}).get(
                    "template_type", "unknown"
                ),
            },
        }

        try:
            # Import databases first (pages may reference them)
            if "databases" in template_data:
                for db_data in template_data["databases"]:
                    try:
                        db_result = self._import_database(
                            db_data, workspace_id, parent_page_id
                        )
                        results["created_databases"].append(db_result)
                    except Exception as e:
                        results["errors"].append(
                            f"Failed to import database '{db_data.get('title', 'Unknown')}': {str(e)}"
                        )

            # Import pages
            if "pages" in template_data:
                for page_data in template_data["pages"]:
                    try:
                        page_result = self._import_page(
                            page_data, workspace_id, parent_page_id
                        )
                        results["created_pages"].append(page_result)
                    except Exception as e:
                        results["errors"].append(
                            f"Failed to import page '{page_data.get('title', 'Unknown')}': {str(e)}"
                        )

            # Check if any imports failed
            if results["errors"]:
                results["success"] = False

        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Import failed: {str(e)}")

        return results

    def _import_database(
        self,
        db_data: Dict[str, Any],
        workspace_id: Optional[str] = None,
        parent_page_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Import a single database into Notion.

        Args:
            db_data: Database data to import
            workspace_id: Target workspace ID
            parent_page_id: Parent page ID

        Returns:
            Database creation result
        """
        # Prepare database properties
        properties = self._convert_template_properties(db_data.get("properties", {}))

        # Prepare database data
        database_data = {
            "title": db_data.get("title", "Untitled Database"),
            "properties": properties,
        }

        # Add description if available
        if db_data.get("description"):
            database_data["description"] = db_data["description"]

        # Add icon if available
        if db_data.get("icon"):
            database_data["icon"] = {"emoji": db_data["icon"]}

        # Add cover if available
        if db_data.get("cover"):
            database_data["cover"] = {"external": {"url": db_data["cover"]}}

        # Determine parent
        if parent_page_id:
            database_data["parent"] = {"page_id": parent_page_id}
        elif workspace_id:
            database_data["parent"] = {"workspace_id": workspace_id}

        # Create the database
        created_db = self.notion_client.create_database(database_data)

        # Import sample entries if available
        imported_entries = []
        if db_data.get("entries"):
            for entry in db_data["entries"][:10]:  # Limit to 10 sample entries
                try:
                    entry_data = self._convert_template_entry(entry, created_db["id"])
                    created_entry = self.notion_client.create_page(entry_data)
                    imported_entries.append(created_entry["id"])
                except Exception as e:
                    print(f"Warning: Failed to import entry: {e}")

        return {
            "id": created_db["id"],
            "title": created_db["title"][0]["plain_text"]
            if created_db.get("title")
            else db_data.get("title"),
            "url": created_db.get("url", ""),
            "imported_entries": imported_entries,
        }

    def _import_page(
        self,
        page_data: Dict[str, Any],
        workspace_id: Optional[str] = None,
        parent_page_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Import a single page into Notion.

        Args:
            page_data: Page data to import
            workspace_id: Target workspace ID
            parent_page_id: Parent page ID

        Returns:
            Page creation result
        """
        # Prepare page content
        content_blocks = self._convert_template_content(page_data.get("content", []))

        # Prepare page data
        page_create_data = {
            "title": page_data.get("title", "Untitled Page"),
            "content": content_blocks,
        }

        # Add icon if available
        if page_data.get("icon"):
            page_create_data["icon"] = {"emoji": page_data["icon"]}

        # Add cover if available
        if page_data.get("cover"):
            page_create_data["cover"] = {"external": {"url": page_data["cover"]}}

        # Determine parent
        if parent_page_id:
            page_create_data["parent"] = {"page_id": parent_page_id}
        elif workspace_id:
            page_create_data["parent"] = {"workspace_id": workspace_id}

        # Create the page
        created_page = self.notion_client.create_page(page_create_data)

        return {
            "id": created_page["id"],
            "title": created_page["title"][0]["plain_text"]
            if created_page.get("title")
            else page_data.get("title"),
            "url": created_page.get("url", ""),
        }

    def _convert_template_properties(
        self, template_properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Convert template properties to Notion API format.

        Args:
            template_properties: Template properties dictionary

        Returns:
            Notion API properties dictionary
        """
        notion_properties = {}

        for prop_name, prop_config in template_properties.items():
            if isinstance(prop_config, dict):
                # Handle different property types
                if "title" in prop_config:
                    notion_properties[prop_name] = {"title": {}}
                elif "rich_text" in prop_config:
                    notion_properties[prop_name] = {"rich_text": {}}
                elif "number" in prop_config:
                    number_config = prop_config["number"]
                    notion_properties[prop_name] = {
                        "number": {"format": number_config.get("format", "number")}
                    }
                elif "select" in prop_config:
                    select_config = prop_config["select"]
                    options = []
                    if "options" in select_config:
                        for option in select_config["options"]:
                            if isinstance(option, str):
                                options.append({"name": option})
                            elif isinstance(option, dict):
                                options.append(
                                    {
                                        "name": option.get("name", ""),
                                        "color": option.get("color", "default"),
                                    }
                                )

                    notion_properties[prop_name] = {"select": {"options": options}}
                elif "multi_select" in prop_config:
                    multi_config = prop_config["multi_select"]
                    options = []
                    if "options" in multi_config:
                        for option in multi_config["options"]:
                            if isinstance(option, str):
                                options.append({"name": option})
                            elif isinstance(option, dict):
                                options.append(
                                    {
                                        "name": option.get("name", ""),
                                        "color": option.get("color", "default"),
                                    }
                                )

                    notion_properties[prop_name] = {
                        "multi_select": {"options": options}
                    }
                elif "date" in prop_config:
                    notion_properties[prop_name] = {"date": {}}
                elif "checkbox" in prop_config:
                    notion_properties[prop_name] = {"checkbox": {}}
                elif "url" in prop_config:
                    notion_properties[prop_name] = {"url": {}}
                elif "email" in prop_config:
                    notion_properties[prop_name] = {"email": {}}
                elif "phone_number" in prop_config:
                    notion_properties[prop_name] = {"phone_number": {}}
                else:
                    # Default to rich text for unknown types
                    notion_properties[prop_name] = {"rich_text": {}}
            else:
                # Simple property type string
                prop_type = prop_config
                if prop_type == "title":
                    notion_properties[prop_name] = {"title": {}}
                elif prop_type == "text":
                    notion_properties[prop_name] = {"rich_text": {}}
                elif prop_type == "number":
                    notion_properties[prop_name] = {"number": {}}
                elif prop_type == "select":
                    notion_properties[prop_name] = {"select": {}}
                elif prop_type == "checkbox":
                    notion_properties[prop_name] = {"checkbox": {}}
                elif prop_type == "date":
                    notion_properties[prop_name] = {"date": {}}
                else:
                    notion_properties[prop_name] = {"rich_text": {}}

        return notion_properties

    def _convert_template_content(
        self, template_content: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Convert template content blocks to Notion API format.

        Args:
            template_content: List of template content blocks

        Returns:
            List of Notion API content blocks
        """
        notion_blocks = []

        for block in template_content:
            if not isinstance(block, dict):
                continue

            block_type = block.get("type")
            if not block_type:
                continue

            # Convert based on block type
            if block_type == "paragraph":
                notion_blocks.append(self._convert_paragraph_block(block))
            elif block_type == "heading_1":
                notion_blocks.append(self._convert_heading_block(block, 1))
            elif block_type == "heading_2":
                notion_blocks.append(self._convert_heading_block(block, 2))
            elif block_type == "heading_3":
                notion_blocks.append(self._convert_heading_block(block, 3))
            elif block_type == "bulleted_list_item":
                notion_blocks.append(
                    self._convert_list_block(block, "bulleted_list_item")
                )
            elif block_type == "numbered_list_item":
                notion_blocks.append(
                    self._convert_list_block(block, "numbered_list_item")
                )
            elif block_type == "to_do":
                notion_blocks.append(self._convert_todo_block(block))
            elif block_type == "code":
                notion_blocks.append(self._convert_code_block(block))
            elif block_type == "quote":
                notion_blocks.append(self._convert_quote_block(block))
            elif block_type == "divider":
                notion_blocks.append({"divider": {}})
            elif block_type == "image":
                notion_blocks.append(self._convert_image_block(block))
            else:
                # Convert to paragraph for unknown types
                notion_blocks.append(self._convert_paragraph_block(block))

        return notion_blocks

    def _convert_paragraph_block(self, block: Dict[str, Any]) -> Dict[str, Any]:
        """Convert paragraph block."""
        rich_text = self._extract_rich_text(
            block.get("paragraph", {}).get("rich_text", [])
        )
        return {"paragraph": {"rich_text": rich_text}}

    def _convert_heading_block(
        self, block: Dict[str, Any], level: int
    ) -> Dict[str, Any]:
        """Convert heading block."""
        block_key = f"heading_{level}"
        rich_text = self._extract_rich_text(
            block.get(block_key, {}).get("rich_text", [])
        )
        return {block_key: {"rich_text": rich_text}}

    def _convert_list_block(
        self, block: Dict[str, Any], list_type: str
    ) -> Dict[str, Any]:
        """Convert list block."""
        rich_text = self._extract_rich_text(
            block.get(list_type, {}).get("rich_text", [])
        )
        return {list_type: {"rich_text": rich_text}}

    def _convert_todo_block(self, block: Dict[str, Any]) -> Dict[str, Any]:
        """Convert todo block."""
        rich_text = self._extract_rich_text(block.get("to_do", {}).get("rich_text", []))
        checked = block.get("to_do", {}).get("checked", False)
        return {"to_do": {"rich_text": rich_text, "checked": checked}}

    def _convert_code_block(self, block: Dict[str, Any]) -> Dict[str, Any]:
        """Convert code block."""
        code_data = block.get("code", {})
        rich_text = self._extract_rich_text(code_data.get("rich_text", []))
        language = code_data.get("language", "plain text")
        return {"code": {"rich_text": rich_text, "language": language}}

    def _convert_quote_block(self, block: Dict[str, Any]) -> Dict[str, Any]:
        """Convert quote block."""
        rich_text = self._extract_rich_text(block.get("quote", {}).get("rich_text", []))
        return {"quote": {"rich_text": rich_text}}

    def _convert_image_block(self, block: Dict[str, Any]) -> Dict[str, Any]:
        """Convert image block."""
        image_data = block.get("image", {})
        if "external" in image_data:
            return {"image": {"external": image_data["external"]}}
        elif "file" in image_data:
            return {"image": {"file": image_data["file"]}}
        else:
            return {
                "image": {
                    "external": {
                        "url": "https://via.placeholder.com/400x200?text=Image"
                    }
                }
            }

    def _extract_rich_text(self, rich_text_array: List[Any]) -> List[Dict[str, Any]]:
        """
        Extract rich text from template format to Notion API format.

        Args:
            rich_text_array: Array of rich text objects

        Returns:
            Notion API rich text array
        """
        if not rich_text_array:
            return [{"text": {"content": ""}}]

        notion_rich_text = []

        for item in rich_text_array:
            if isinstance(item, str):
                notion_rich_text.append({"text": {"content": item}})
            elif isinstance(item, dict):
                text_content = item.get("text", {}).get("content", "")
                if not text_content and "plain_text" in item:
                    text_content = item["plain_text"]

                rich_text_item = {"text": {"content": text_content}}

                # Add annotations
                if "annotations" in item:
                    annotations = item["annotations"]
                    rich_text_item["annotations"] = {}

                    if annotations.get("bold"):
                        rich_text_item["annotations"]["bold"] = True
                    if annotations.get("italic"):
                        rich_text_item["annotations"]["italic"] = True
                    if annotations.get("strikethrough"):
                        rich_text_item["annotations"]["strikethrough"] = True
                    if annotations.get("underline"):
                        rich_text_item["annotations"]["underline"] = True
                    if annotations.get("code"):
                        rich_text_item["annotations"]["code"] = True

                    color = annotations.get("color")
                    if color and color != "default":
                        rich_text_item["annotations"]["color"] = color

                notion_rich_text.append(rich_text_item)

        return notion_rich_text

    def _convert_template_entry(
        self, entry: Dict[str, Any], database_id: str
    ) -> Dict[str, Any]:
        """
        Convert template entry to Notion page format.

        Args:
            entry: Template entry data
            database_id: Target database ID

        Returns:
            Notion page creation data
        """
        page_data = {"parent": {"database_id": database_id}, "properties": {}}

        # Convert properties
        if "properties" in entry:
            for prop_name, prop_value in entry["properties"].items():
                if prop_name.lower() == "title" or prop_name.lower() == "name":
                    page_data["properties"][prop_name] = {
                        "title": [{"text": {"content": str(prop_value)}}]
                    }
                elif isinstance(prop_value, bool):
                    page_data["properties"][prop_name] = {"checkbox": prop_value}
                elif isinstance(prop_value, (int, float)):
                    page_data["properties"][prop_name] = {"number": prop_value}
                else:
                    page_data["properties"][prop_name] = {
                        "rich_text": [{"text": {"content": str(prop_value)}}]
                    }

        # Add content if available
        if "content" in entry:
            page_data["content"] = self._convert_template_content(entry["content"])

        return page_data

    def validate_import_data(self, template_data: Dict[str, Any]) -> List[str]:
        """
        Validate template data before import.

        Args:
            template_data: Template data to validate

        Returns:
            List of validation errors
        """
        errors = []

        if not isinstance(template_data, dict):
            errors.append("Template data must be a dictionary")
            return errors

        # Check for required structure
        if "pages" not in template_data and "databases" not in template_data:
            errors.append("Template must contain pages or databases")

        # Validate pages
        if "pages" in template_data:
            pages = template_data["pages"]
            if not isinstance(pages, list):
                errors.append("Pages must be a list")
            else:
                for i, page in enumerate(pages):
                    if not isinstance(page, dict):
                        errors.append(f"Page {i} must be a dictionary")
                    elif "title" not in page:
                        errors.append(f"Page {i} must have a title")

        # Validate databases
        if "databases" in template_data:
            databases = template_data["databases"]
            if not isinstance(databases, list):
                errors.append("Databases must be a list")
            else:
                for i, db in enumerate(databases):
                    if not isinstance(db, dict):
                        errors.append(f"Database {i} must be a dictionary")
                    elif "title" not in db:
                        errors.append(f"Database {i} must have a title")

        return errors

    def get_import_status(self, import_result: Dict[str, Any]) -> str:
        """
        Get a human-readable status message for import results.

        Args:
            import_result: Import result dictionary

        Returns:
            Status message
        """
        if import_result.get("success"):
            pages_count = len(import_result.get("created_pages", []))
            dbs_count = len(import_result.get("created_databases", []))
            return (
                f"✅ Successfully imported {pages_count} pages and {dbs_count} databases"
            )
        else:
            errors_count = len(import_result.get("errors", []))
            return f"❌ Import failed with {errors_count} errors"

    def __str__(self) -> str:
        """String representation of the import service."""
        client_status = "connected" if self.notion_client else "disconnected"
        return f"NotionImportService(client={client_status})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"NotionImportService(notion_client={self.notion_client is not None})"
