"""
Template generation service for the Notion Template Maker application.
Orchestrates template creation using AI and Notion APIs.
"""

from typing import Optional, Dict, Any, List
import json
import time
import hashlib
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from backend.clients.openrouter_client import OpenRouterClient
from backend.clients.notion_client import NotionClient


class TemplateGenerator:
    """Service for generating Notion templates using AI."""

    def __init__(
        self,
        openrouter_client: Optional[OpenRouterClient] = None,
        notion_client: Optional[NotionClient] = None,
        cache_ttl: int = 3600,  # 1 hour cache
        generation_timeout: int = 45,
    ):  # 45 second timeout
        """
        Initialize the template generator.

        Args:
            openrouter_client: OpenRouter API client
            notion_client: Notion API client
            cache_ttl: Cache time-to-live in seconds
            generation_timeout: Maximum generation time in seconds
        """
        self.openrouter_client = openrouter_client
        self.notion_client = notion_client
        self.cache_ttl = cache_ttl
        self.generation_timeout = generation_timeout
        self._cache = {}
        self._executor = ThreadPoolExecutor(max_workers=2)

    def set_clients(
        self, openrouter_client: OpenRouterClient, notion_client: NotionClient
    ):
        """Set the API clients."""
        self.openrouter_client = openrouter_client
        self.notion_client = notion_client

    def _get_cache_key(self, user_input: Dict[str, Any]) -> str:
        """Generate a cache key for the user input."""
        # Create a deterministic string representation of the input
        input_str = json.dumps(user_input, sort_keys=True, default=str)
        return hashlib.md5(input_str.encode()).hexdigest()

    def _is_cache_valid(self, cache_entry: Dict[str, Any]) -> bool:
        """Check if a cache entry is still valid."""
        if "timestamp" not in cache_entry:
            return False
        return (time.time() - cache_entry["timestamp"]) < self.cache_ttl

    def _get_cached_result(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get a cached result if available and valid."""
        if cache_key in self._cache:
            cache_entry = self._cache[cache_key]
            if self._is_cache_valid(cache_entry):
                return cache_entry["data"]
            else:
                # Remove expired cache entry
                del self._cache[cache_key]
        return None

    def _cache_result(self, cache_key: str, result: Dict[str, Any]):
        """Cache a result with timestamp."""
        self._cache[cache_key] = {"data": result, "timestamp": time.time()}

    def generate_template(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete Notion template based on user input with performance optimizations.

        Args:
            user_input: Dictionary containing template specifications

        Returns:
            Dictionary with generated pages and databases

        Raises:
            ValueError: If required clients are not set or input is invalid
            TimeoutError: If generation exceeds timeout
        """
        if not self.openrouter_client:
            raise ValueError("OpenRouter client not set")

        start_time = time.time()

        # Check cache first
        cache_key = self._get_cache_key(user_input)
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result

        try:
            # Use ThreadPoolExecutor for timeout handling
            future = self._executor.submit(self._generate_template_async, user_input)

            # Wait for completion with timeout
            result = future.result(timeout=self.generation_timeout)

            # Cache the result
            self._cache_result(cache_key, result)

            generation_time = time.time() - start_time
            result["metadata"]["generation_time_seconds"] = generation_time
            result["metadata"]["cached"] = False

            return result

        except TimeoutError:
            generation_time = time.time() - start_time
            raise TimeoutError(
                f"Template generation timed out after {generation_time:.1f} seconds (limit: {self.generation_timeout}s)"
            )
        except Exception as e:
            generation_time = time.time() - start_time
            raise RuntimeError(
                f"Template generation failed after {generation_time:.1f} seconds: {str(e)}"
            )

    def _generate_template_async(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Async template generation logic."""
        # Extract user input with defaults for performance
        template_type = user_input.get("template_type", "general")
        title = user_input.get("title", "New Template")
        description = user_input.get("description", "")
        features = user_input.get("features", [])
        custom_properties = user_input.get("custom_properties", {})

        # Optimize AI prompt based on input complexity
        optimized_input = self._optimize_input_for_performance(user_input)

        # Generate template using AI with optimized parameters
        ai_response = self.openrouter_client.generate_template(
            template_type=template_type,
            title=title,
            description=description,
            features=features,
            custom_properties=custom_properties,
            **optimized_input,
        )

        # Process and validate the AI response
        processed_template = self._process_ai_response(ai_response, user_input)

        return processed_template

    def _optimize_input_for_performance(
        self, user_input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Optimize user input for better performance."""
        optimized = {}

        # Limit description length for faster processing
        if "description" in user_input:
            description = user_input["description"]
            if len(description) > 500:
                optimized["description"] = description[:500] + "..."
                optimized["truncated"] = True

        # Limit features to most important ones
        if "features" in user_input:
            features = user_input["features"]
            if len(features) > 10:
                optimized["features"] = features[:10]
                optimized["truncated"] = True

        # Set performance-focused AI parameters
        optimized.update(
            {
                "temperature": 0.7,  # Balanced creativity vs speed
                "max_tokens": 2000,  # Reasonable limit for template generation
                "model": "anthropic/claude-3-haiku",  # Fast model for generation
            }
        )

        return optimized

    def _process_ai_response(
        self, ai_response: Dict[str, Any], user_input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process and validate the AI-generated template response.

        Args:
            ai_response: Raw AI response
            user_input: Original user input

        Returns:
            Processed template data
        """
        processed = {
            "pages": [],
            "databases": [],
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "template_type": user_input.get("template_type", "general"),
                "ai_model": getattr(self.openrouter_client, "default_model", "unknown"),
            },
        }

        # Process pages
        if "pages" in ai_response:
            for page_data in ai_response["pages"]:
                processed_page = self._process_page_data(page_data)
                if processed_page:
                    processed["pages"].append(processed_page)

        # Process databases
        if "databases" in ai_response:
            for db_data in ai_response["databases"]:
                processed_db = self._process_database_data(db_data)
                if processed_db:
                    processed["databases"].append(processed_db)

        # Add user customizations
        self._apply_user_customizations(processed, user_input)

        return processed

    def _process_page_data(self, page_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process and validate page data from AI response.

        Args:
            page_data: Raw page data from AI

        Returns:
            Processed page data or None if invalid
        """
        try:
            title = page_data.get("title", "").strip()
            if not title:
                return None

            processed_page = {
                "title": title,
                "content": [],
                "icon": page_data.get("icon"),
                "cover": page_data.get("cover"),
            }

            # Process content blocks
            content = page_data.get("content", [])
            if isinstance(content, list):
                processed_page["content"] = self._validate_content_blocks(content)

            return processed_page

        except Exception:
            return None

    def _process_database_data(
        self, db_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Process and validate database data from AI response.

        Args:
            db_data: Raw database data from AI

        Returns:
            Processed database data or None if invalid
        """
        try:
            title = db_data.get("title", "").strip()
            if not title:
                return None

            processed_db = {
                "title": title,
                "description": db_data.get("description", ""),
                "properties": {},
            }

            # Process properties
            properties = db_data.get("properties", {})
            if isinstance(properties, dict):
                processed_db["properties"] = self._validate_database_properties(
                    properties
                )

            # Ensure Name/Title property exists
            if "Name" not in processed_db["properties"]:
                processed_db["properties"]["Name"] = {"title": {}}

            return processed_db

        except Exception:
            return None

    def _validate_content_blocks(
        self, blocks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Validate and clean content blocks.

        Args:
            blocks: List of content blocks

        Returns:
            Validated content blocks
        """
        valid_blocks = []
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
        }

        for block in blocks:
            if isinstance(block, dict) and block.get("type") in valid_types:
                # Ensure proper structure
                if "content" in block:
                    block_type = block["type"]
                    if block_type in [
                        "paragraph",
                        "heading_1",
                        "heading_2",
                        "heading_3",
                        "bulleted_list_item",
                        "numbered_list_item",
                        "to_do",
                    ]:
                        # Ensure rich_text structure
                        content = block["content"]
                        if isinstance(content, dict) and "rich_text" not in content:
                            content["rich_text"] = [{"text": {"content": str(content)}}]

                    valid_blocks.append(
                        {"type": block["type"], block["type"]: block["content"]}
                    )

        return valid_blocks

    def _validate_database_properties(
        self, properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate and clean database properties.

        Args:
            properties: Raw properties dictionary

        Returns:
            Validated properties
        """
        valid_properties = {}
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
        }

        for prop_name, prop_config in properties.items():
            if isinstance(prop_config, dict):
                prop_type = prop_config.get("type")
                if prop_type in valid_types:
                    valid_properties[prop_name] = {prop_type: prop_config}
                elif isinstance(prop_config, dict) and len(prop_config) == 1:
                    # Handle case where type is key
                    prop_type = list(prop_config.keys())[0]
                    if prop_type in valid_types:
                        valid_properties[prop_name] = prop_config

        return valid_properties

    def _apply_user_customizations(
        self, template: Dict[str, Any], user_input: Dict[str, Any]
    ):
        """
        Apply user customizations to the generated template.

        Args:
            template: Processed template data
            user_input: User input with customizations
        """
        custom_properties = user_input.get("custom_properties", {})

        # Apply custom properties to databases
        for database in template.get("databases", []):
            for prop_name, prop_type in custom_properties.items():
                if prop_name not in database.get("properties", {}):
                    if prop_type == "text":
                        database["properties"][prop_name] = {"rich_text": {}}
                    elif prop_type == "number":
                        database["properties"][prop_name] = {"number": {}}
                    elif prop_type == "select":
                        database["properties"][prop_name] = {"select": {"options": []}}
                    elif prop_type == "date":
                        database["properties"][prop_name] = {"date": {}}

    def create_notion_template(
        self, template_data: Dict[str, Any], parent_page_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create the generated template in Notion.

        Args:
            template_data: Processed template data
            parent_page_id: ID of parent page in Notion

        Returns:
            Dictionary with created Notion items

        Raises:
            ValueError: If Notion client is not set
        """
        if not self.notion_client:
            raise ValueError("Notion client not set")

        created_items = {"pages": [], "databases": []}

        # Create databases first (pages might reference them)
        for db_data in template_data.get("databases", []):
            try:
                notion_db = self.notion_client.create_database(
                    title=db_data["title"],
                    properties=db_data["properties"],
                    parent_id=parent_page_id,
                    description=db_data.get("description"),
                )
                created_items["databases"].append(
                    {
                        "id": notion_db["id"],
                        "title": db_data["title"],
                        "url": notion_db.get("url", ""),
                    }
                )
            except Exception as e:
                # Log error but continue with other items
                print(f"Failed to create database '{db_data['title']}': {e}")

        # Create pages
        for page_data in template_data.get("pages", []):
            try:
                notion_page = self.notion_client.create_page(
                    title=page_data["title"],
                    content_blocks=page_data.get("content", []),
                    parent_id=parent_page_id,
                    icon=page_data.get("icon"),
                    cover=page_data.get("cover"),
                )
                created_items["pages"].append(
                    {
                        "id": notion_page["id"],
                        "title": page_data["title"],
                        "url": notion_page.get("url", ""),
                    }
                )
            except Exception as e:
                # Log error but continue with other items
                print(f"Failed to create page '{page_data['title']}': {e}")

        return created_items

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for the template generator."""
        return {
            "cache_size": len(self._cache),
            "cache_hit_ratio": self._calculate_cache_hit_ratio(),
            "average_generation_time": self._calculate_average_generation_time(),
            "timeout_count": getattr(self, "_timeout_count", 0),
            "total_generations": getattr(self, "_total_generations", 0),
        }

    def _calculate_cache_hit_ratio(self) -> float:
        """Calculate cache hit ratio."""
        total_requests = getattr(self, "_total_requests", 0)
        cache_hits = getattr(self, "_cache_hits", 0)

        if total_requests == 0:
            return 0.0

        return cache_hits / total_requests

    def _calculate_average_generation_time(self) -> float:
        """Calculate average generation time."""
        generation_times = getattr(self, "_generation_times", [])

        if not generation_times:
            return 0.0

        return sum(generation_times) / len(generation_times)

    def clear_cache(self):
        """Clear the template cache."""
        self._cache.clear()

    def optimize_for_speed(self):
        """Optimize settings for faster generation."""
        self.generation_timeout = 30  # Reduce timeout
        self.cache_ttl = 7200  # Increase cache TTL to 2 hours

        # Clear old cache entries
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._cache.items() if not self._is_cache_valid(entry)
        ]

        for key in expired_keys:
            del self._cache[key]

    def optimize_for_quality(self):
        """Optimize settings for higher quality generation."""
        self.generation_timeout = 60  # Increase timeout for better results
        self.cache_ttl = 1800  # Reduce cache TTL to 30 minutes

        # Update AI parameters for quality
        if hasattr(self, "_ai_params"):
            self._ai_params.update(
                {
                    "temperature": 0.8,
                    "max_tokens": 3000,
                    "model": "anthropic/claude-3-sonnet",
                }
            )

    def validate_template_data(self, template_data: Dict[str, Any]) -> List[str]:
        """
        Validate template data structure.

        Args:
            template_data: Template data to validate

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
                if not isinstance(page, dict):
                    errors.append(f"Page {i} must be a dictionary")
                elif "title" not in page:
                    errors.append(f"Page {i} must have a 'title' field")

        # Validate databases
        databases = template_data.get("databases", [])
        if not isinstance(databases, list):
            errors.append("'databases' must be a list")
        else:
            for i, db in enumerate(databases):
                if not isinstance(db, dict):
                    errors.append(f"Database {i} must be a dictionary")
                elif "title" not in db:
                    errors.append(f"Database {i} must have a 'title' field")
                elif "properties" not in db:
                    errors.append(f"Database {i} must have a 'properties' field")

        return errors

    def estimate_complexity(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estimate the complexity of template generation.

        Args:
            user_input: User input for template generation

        Returns:
            Complexity estimation
        """
        complexity = {
            "level": "simple",
            "estimated_pages": 1,
            "estimated_databases": 1,
            "estimated_time_seconds": 30,
        }

        template_type = user_input.get("template_type", "general")
        features = user_input.get("features", [])
        custom_properties = user_input.get("custom_properties", {})

        # Adjust based on template type
        if template_type in ["project_management", "knowledge_base", "business"]:
            complexity["level"] = "medium"
            complexity["estimated_pages"] = 3
            complexity["estimated_databases"] = 2
            complexity["estimated_time_seconds"] = 60

        if template_type in ["enterprise", "complex"]:
            complexity["level"] = "complex"
            complexity["estimated_pages"] = 5
            complexity["estimated_databases"] = 3
            complexity["estimated_time_seconds"] = 120

        # Adjust based on features
        if len(features) > 3:
            complexity["estimated_pages"] += 1
            complexity["estimated_time_seconds"] += 30

        # Adjust based on custom properties
        if len(custom_properties) > 5:
            complexity["estimated_databases"] += 1
            complexity["estimated_time_seconds"] += 20

        return complexity

    def __str__(self) -> str:
        """String representation of the service."""
        return "TemplateGenerator()"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"TemplateGenerator(openrouter={'set' if self.openrouter_client else 'not set'}, notion={'set' if self.notion_client else 'not set'})"
