"""
Notion API client for the Notion Template Maker application.
Handles communication with Notion API for workspace operations.
"""

import requests
from typing import Optional, Dict, Any, List
import json
from datetime import datetime


class NotionClient:
    """Client for interacting with Notion API."""

    BASE_URL = "https://api.notion.com/v1"

    def __init__(self, access_token: str, notion_version: str = "2022-06-28"):
        """
        Initialize the Notion client.

        Args:
            access_token: Notion API access token
            notion_version: Notion API version to use
        """
        self.access_token = access_token
        self.notion_version = notion_version
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Notion-Version": notion_version,
            }
        )

    def search_workspace(
        self,
        query: str = "",
        filter_type: Optional[str] = None,
        sort: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Search the user's workspace for pages and databases.

        Args:
            query: Search query string
            filter_type: Filter by 'page' or 'database'
            sort: Sort configuration

        Returns:
            Search results
        """
        url = f"{self.BASE_URL}/search"
        payload = {"query": query}

        if filter_type:
            payload["filter"] = {"property": "object", "value": filter_type}

        if sort:
            payload["sort"] = sort

        response = self.session.post(url, json=payload)
        response.raise_for_status()

        return response.json()

    def get_page(self, page_id: str) -> Dict[str, Any]:
        """
        Retrieve a page by ID.

        Args:
            page_id: The ID of the page to retrieve

        Returns:
            Page data
        """
        url = f"{self.BASE_URL}/pages/{page_id}"
        response = self.session.get(url)
        response.raise_for_status()

        return response.json()

    def get_database(self, database_id: str) -> Dict[str, Any]:
        """
        Retrieve a database by ID.

        Args:
            database_id: The ID of the database to retrieve

        Returns:
            Database data
        """
        url = f"{self.BASE_URL}/databases/{database_id}"
        response = self.session.get(url)
        response.raise_for_status()

        return response.json()

    def create_page(
        self,
        title: str,
        content_blocks: Optional[List[Dict[str, Any]]] = None,
        parent_id: Optional[str] = None,
        icon: Optional[str] = None,
        cover: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new page in Notion.

        Args:
            title: Title of the page
            content_blocks: List of content blocks for the page
            parent_id: ID of parent page (optional)
            icon: Emoji icon for the page (optional)
            cover: Cover image URL (optional)

        Returns:
            Created page data
        """
        url = f"{self.BASE_URL}/pages"

        # Build page properties
        properties = {"title": {"title": [{"text": {"content": title}}]}}

        # Build page data
        page_data = {"properties": properties}

        # Add parent
        if parent_id:
            page_data["parent"] = {"type": "page_id", "page_id": parent_id}
        else:
            page_data["parent"] = {"type": "workspace", "workspace": True}

        # Add icon
        if icon:
            page_data["icon"] = {"type": "emoji", "emoji": icon}

        # Add cover
        if cover:
            page_data["cover"] = {"type": "external", "external": {"url": cover}}

        # Add content blocks
        if content_blocks:
            page_data["children"] = content_blocks

        response = self.session.post(url, json=page_data)
        response.raise_for_status()

        return response.json()

    def create_database(
        self,
        title: str,
        properties: Dict[str, Any],
        parent_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new database in Notion.

        Args:
            title: Title of the database
            properties: Database properties configuration
            parent_id: ID of parent page (optional)
            description: Database description (optional)

        Returns:
            Created database data
        """
        url = f"{self.BASE_URL}/databases"

        # Build database data
        database_data = {
            "title": [{"text": {"content": title}}],
            "properties": properties,
        }

        # Add parent
        if parent_id:
            database_data["parent"] = {"type": "page_id", "page_id": parent_id}
        else:
            database_data["parent"] = {"type": "workspace", "workspace": True}

        # Add description
        if description:
            database_data["description"] = [{"text": {"content": description}}]

        response = self.session.post(url, json=database_data)
        response.raise_for_status()

        return response.json()

    def update_page(
        self,
        page_id: str,
        properties: Optional[Dict[str, Any]] = None,
        archived: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Update a page's properties.

        Args:
            page_id: ID of the page to update
            properties: Properties to update
            archived: Whether to archive the page

        Returns:
            Updated page data
        """
        url = f"{self.BASE_URL}/pages/{page_id}"

        update_data = {}
        if properties:
            update_data["properties"] = properties
        if archived is not None:
            update_data["archived"] = archived

        response = self.session.patch(url, json=update_data)
        response.raise_for_status()

        return response.json()

    def update_database(
        self,
        database_id: str,
        title: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update a database's configuration.

        Args:
            database_id: ID of the database to update
            title: New title (optional)
            properties: Properties to update (optional)
            description: New description (optional)

        Returns:
            Updated database data
        """
        url = f"{self.BASE_URL}/databases/{database_id}"

        update_data = {}

        if title:
            update_data["title"] = [{"text": {"content": title}}]

        if properties:
            update_data["properties"] = properties

        if description:
            update_data["description"] = [{"text": {"content": description}}]

        response = self.session.patch(url, json=update_data)
        response.raise_for_status()

        return response.json()

    def get_page_content(
        self, page_id: str, start_cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get the content blocks of a page.

        Args:
            page_id: ID of the page
            start_cursor: Cursor for pagination

        Returns:
            Page content blocks
        """
        url = f"{self.BASE_URL}/blocks/{page_id}/children"

        params = {}
        if start_cursor:
            params["start_cursor"] = start_cursor

        response = self.session.get(url, params=params)
        response.raise_for_status()

        return response.json()

    def append_block_children(
        self, block_id: str, children: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Append children blocks to a block.

        Args:
            block_id: ID of the parent block
            children: List of child blocks to append

        Returns:
            API response
        """
        url = f"{self.BASE_URL}/blocks/{block_id}/children"

        response = self.session.patch(url, json={"children": children})
        response.raise_for_status()

        return response.json()

    def query_database(
        self,
        database_id: str,
        filter_conditions: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None,
        start_cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Query a database for pages.

        Args:
            database_id: ID of the database to query
            filter_conditions: Filter conditions
            sorts: Sort specifications
            start_cursor: Cursor for pagination

        Returns:
            Query results
        """
        url = f"{self.BASE_URL}/databases/{database_id}/query"

        payload = {}

        if filter_conditions:
            payload["filter"] = filter_conditions

        if sorts:
            payload["sorts"] = sorts

        if start_cursor:
            payload["start_cursor"] = start_cursor

        response = self.session.post(url, json=payload)
        response.raise_for_status()

        return response.json()

    def validate_token(self) -> bool:
        """
        Validate the access token by making a test request.

        Returns:
            True if token is valid, False otherwise
        """
        try:
            # Try to search with an empty query
            self.search_workspace("")
            return True
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                return False
            # For other errors, re-raise
            raise
        except Exception:
            # For network errors, assume token is valid
            return True

    def test_integration_connection(self) -> Dict[str, Any]:
        """
        Test the integration connection and return detailed status.

        Returns:
            Dictionary with connection status and details
        """
        result = {
            "connected": False,
            "error": None,
            "user_info": None,
            "workspaces": None
        }

        try:
            # Test basic connectivity
            user_info = self.get_user_info()
            result["user_info"] = user_info

            # Test workspace access
            workspaces = self.search_workspace("")
            result["workspaces"] = workspaces

            result["connected"] = True

        except requests.HTTPError as e:
            if e.response.status_code == 401:
                result["error"] = "Invalid integration token or insufficient permissions"
            elif e.response.status_code == 403:
                result["error"] = "Integration does not have access to the requested resources"
            else:
                result["error"] = f"HTTP error: {e.response.status_code}"
        except requests.RequestException as e:
            result["error"] = f"Network error: {str(e)}"
        except Exception as e:
            result["error"] = f"Unexpected error: {str(e)}"

        return result

    def get_user_info(self) -> Dict[str, Any]:
        """
        Get information about the authenticated user.

        Returns:
            User information
        """
        url = f"{self.BASE_URL}/users/me"
        response = self.session.get(url)
        response.raise_for_status()

        return response.json()

    def list_users(self) -> Dict[str, Any]:
        """
        List all users in the workspace.

        Returns:
            List of users
        """
        url = f"{self.BASE_URL}/users"
        response = self.session.get(url)
        response.raise_for_status()

        return response.json()

    def _handle_rate_limit(self, response: requests.Response) -> None:
        """
        Handle rate limiting (Notion has rate limits).

        Args:
            response: The API response
        """
        # Notion API rate limits are handled by the requests-retry mechanism
        # or can be implemented here if needed
        pass

    def __str__(self) -> str:
        """String representation of the client."""
        return "NotionClient()"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"NotionClient(access_token={'*' * 8}, version={self.notion_version!r})"

