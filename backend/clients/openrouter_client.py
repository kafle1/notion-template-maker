"""
OpenRouter API client for the Notion Template Maker application.
Handles communication with OpenRouter API for AI-powered template generation.
"""

import requests
from typing import Optional, Dict, Any, List
import json


class OpenRouterClient:
    """Client for interacting with OpenRouter API."""

    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self, api_key: str, model: str = "deepseek/deepseek-chat-v3.1:free"):
        """
        Initialize the OpenRouter client.

        Args:
            api_key: OpenRouter API key
            model: Default model to use for requests
        """
        self.api_key = api_key
        self.default_model = model
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://notion-template-maker.com",
                "X-Title": "Notion Template Maker",
            }
        )

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to OpenRouter.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (defaults to instance default)
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters

        Returns:
            API response as dictionary

        Raises:
            requests.HTTPError: If the API request fails
        """
        url = f"{self.BASE_URL}/chat/completions"
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
            **kwargs,
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

        response = self.session.post(url, json=payload)
        response.raise_for_status()

        return response.json()

    def generate_template_prompt(
        self,
        template_type: str,
        user_description: str,
        features: Optional[List[str]] = None,
        custom_properties: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a prompt for template creation.

        Args:
            template_type: Type of template (e.g., 'project_management', 'knowledge_base')
            user_description: User's description of what they want
            features: List of features to include
            custom_properties: Custom properties to add

        Returns:
            Formatted prompt string
        """
        prompt_parts = [
            f"Create a Notion template for: {template_type}",
            f"Description: {user_description}",
        ]

        if features:
            prompt_parts.append(f"Features to include: {', '.join(features)}")

        if custom_properties:
            props_str = ", ".join([f"{k} ({v})" for k, v in custom_properties.items()])
            prompt_parts.append(f"Custom properties: {props_str}")

        prompt_parts.extend(
            [
                "",
                "Please generate a JSON response with the following structure:",
                "{",
                '  "pages": [',
                "    {",
                '      "title": "Page Title",',
                '      "content": [',
                '        {"type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "Heading"}}]}}',
                "      ]",
                "    }",
                "  ],",
                '  "databases": [',
                "    {",
                '      "title": "Database Title",',
                '      "properties": {',
                '        "Name": {"title": {}},',
                '        "Status": {"select": {"options": [{"name": "Active"}, {"name": "Inactive"}]}}',
                "      }",
                "    }",
                "  ]",
                "}",
                "",
                "Ensure the template is practical and well-structured for Notion.",
            ]
        )

        return "\n".join(prompt_parts)

    def generate_template(
        self,
        template_type: str,
        title: str,
        description: str = "",
        features: Optional[List[str]] = None,
        custom_properties: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Generate a complete Notion template using AI.

        Args:
            template_type: Type of template to generate
            title: Title for the template
            description: Description of the template
            features: List of features to include
            custom_properties: Custom properties to add
            model: Model to use for generation
            temperature: Sampling temperature

        Returns:
            Generated template as dictionary with 'pages' and 'databases'

        Raises:
            ValueError: If the response cannot be parsed
            requests.HTTPError: If the API request fails
        """
        prompt = self.generate_template_prompt(
            template_type, description, features, custom_properties
        )

        messages = [
            {
                "role": "system",
                "content": "You are a Notion template generator. Generate detailed Notion page and database structures in valid JSON format.",
            },
            {"role": "user", "content": prompt},
        ]

        response = self.chat_completion(
            messages=messages, model=model, temperature=temperature, max_tokens=2000
        )

        # Extract the generated content
        if "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]

            # Try to parse as JSON
            try:
                # Remove markdown code blocks if present
                if content.startswith("```json"):
                    content = content[7:]
                if content.endswith("```"):
                    content = content[:-3]

                template_data = json.loads(content.strip())

                # Validate structure
                if not isinstance(template_data, dict):
                    raise ValueError("Response is not a valid JSON object")

                if "pages" not in template_data and "databases" not in template_data:
                    raise ValueError("Response must contain 'pages' or 'databases'")

                return template_data

            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse AI response as JSON: {e}")

        else:
            raise ValueError("No valid response received from OpenRouter API")

    def list_available_models(self) -> List[Dict[str, Any]]:
        """
        List available models from OpenRouter.

        Returns:
            List of available models
        """
        url = f"{self.BASE_URL}/models"
        response = self.session.get(url)
        response.raise_for_status()

        data = response.json()
        return data.get("data", [])

    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific model.

        Args:
            model_id: The model identifier

        Returns:
            Model information or None if not found
        """
        models = self.list_available_models()
        for model in models:
            if model.get("id") == model_id:
                return model
        return None


    def __str__(self) -> str:
        """String representation of the client."""
        return f"OpenRouterClient(model={self.default_model})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"OpenRouterClient(api_key={'*' * 8}, model={self.default_model!r})"
