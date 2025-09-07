"""
OAuth service for handling Notion OAuth authentication flow.
Manages authorization URLs, token exchange, and callback handling.
"""

import secrets
import hashlib
import base64
import json
from typing import Dict, Any, Optional, Tuple
from urllib.parse import urlencode, urlparse, parse_qs
import requests
from datetime import datetime, timedelta

from src.models.user import User


class NotionOAuthService:
    """Service for handling Notion OAuth authentication."""

    # Notion OAuth endpoints
    AUTHORIZATION_URL = "https://api.notion.com/v1/oauth/authorize"
    TOKEN_URL = "https://api.notion.com/v1/oauth/token"

    # Required OAuth scopes for template operations
    REQUIRED_SCOPES = ["pages:read", "pages:write", "databases:read", "databases:write"]

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        """
        Initialize OAuth service.

        Args:
            client_id: Notion OAuth client ID
            client_secret: Notion OAuth client secret
            redirect_uri: OAuth redirect URI
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def generate_state(self) -> str:
        """
        Generate a secure random state parameter for OAuth.

        Returns:
            Random state string
        """
        return secrets.token_urlsafe(32)

    def generate_code_verifier(self) -> str:
        """
        Generate a code verifier for PKCE (Proof Key for Code Exchange).

        Returns:
            Random code verifier string
        """
        return secrets.token_urlsafe(64)

    def generate_code_challenge(self, code_verifier: str) -> str:
        """
        Generate code challenge from code verifier using SHA256.

        Args:
            code_verifier: Code verifier string

        Returns:
            Base64-encoded SHA256 hash
        """
        sha256 = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        return base64.urlsafe_b64encode(sha256).decode("utf-8").rstrip("=")

    def get_authorization_url(
        self, state: Optional[str] = None, code_verifier: Optional[str] = None
    ) -> Tuple[str, str, str]:
        """
        Generate Notion OAuth authorization URL.

        Args:
            state: OAuth state parameter (generated if not provided)
            code_verifier: PKCE code verifier (generated if not provided)

        Returns:
            Tuple of (authorization_url, state, code_verifier)
        """
        if not state:
            state = self.generate_state()

        if not code_verifier:
            code_verifier = self.generate_code_verifier()

        code_challenge = self.generate_code_challenge(code_verifier)

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "owner": "user",
            "scope": " ".join(self.REQUIRED_SCOPES),
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }

        auth_url = f"{self.AUTHORIZATION_URL}?{urlencode(params)}"
        return auth_url, state, code_verifier

    def exchange_code_for_token(self, code: str, code_verifier: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.

        Args:
            code: Authorization code from callback
            code_verifier: PKCE code verifier

        Returns:
            Token response dictionary

        Raises:
            ValueError: If token exchange fails
        """
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "code_verifier": code_verifier,
        }

        # Create basic auth header
        auth = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            response = requests.post(self.TOKEN_URL, data=data, headers=headers)
            response.raise_for_status()

            token_data = response.json()

            # Validate required fields
            required_fields = ["access_token", "token_type", "workspace_id"]
            for field in required_fields:
                if field not in token_data:
                    raise ValueError(f"Missing required field: {field}")

            # Add token expiry if not provided
            if "expires_in" in token_data:
                token_data["expires_at"] = datetime.now() + timedelta(
                    seconds=token_data["expires_in"]
                )

            return token_data

        except requests.RequestException as e:
            raise ValueError(f"OAuth token exchange failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid token response: {str(e)}")

    def validate_token(self, token: str) -> bool:
        """
        Validate OAuth token format and basic structure.

        Args:
            token: Access token to validate

        Returns:
            True if token appears valid
        """
        if not token or not isinstance(token, str):
            return False

        # Basic format validation (Bearer tokens should be reasonably long)
        if len(token) < 10:
            return False

        # Check for common invalid patterns
        invalid_patterns = ["null", "undefined", "invalid", "expired"]
        if any(pattern in token.lower() for pattern in invalid_patterns):
            return False

        return True

    def validate_scopes(
        self, token_data: Dict[str, Any], required_scopes: Optional[list] = None
    ) -> bool:
        """
        Validate that token has required scopes.

        Args:
            token_data: Token response data
            required_scopes: List of required scopes (uses default if None)

        Returns:
            True if all required scopes are present
        """
        if required_scopes is None:
            required_scopes = self.REQUIRED_SCOPES

        if "scope" not in token_data:
            return False

        token_scopes = set(token_data["scope"].split())
        required_scopes_set = set(required_scopes)

        return required_scopes_set.issubset(token_scopes)

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh an expired access token.

        Args:
            refresh_token: Refresh token

        Returns:
            New token response dictionary

        Raises:
            ValueError: If token refresh fails
        """
        data = {"grant_type": "refresh_token", "refresh_token": refresh_token}

        # Create basic auth header
        auth = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            response = requests.post(self.TOKEN_URL, data=data, headers=headers)
            response.raise_for_status()

            token_data = response.json()

            # Add token expiry if not provided
            if "expires_in" in token_data:
                token_data["expires_at"] = datetime.now() + timedelta(
                    seconds=token_data["expires_in"]
                )

            return token_data

        except requests.RequestException as e:
            raise ValueError(f"Token refresh failed: {str(e)}")

    def parse_callback_url(self, callback_url: str) -> Dict[str, Any]:
        """
        Parse OAuth callback URL and extract parameters.

        Args:
            callback_url: Full callback URL with query parameters

        Returns:
            Dictionary with parsed parameters

        Raises:
            ValueError: If callback URL is malformed or contains errors
        """
        parsed_url = urlparse(callback_url)
        query_params = parse_qs(parsed_url.query)

        result = {}

        # Extract single-value parameters
        for param in ["code", "state", "error", "error_description"]:
            if param in query_params:
                result[param] = query_params[param][0]

        # Check for OAuth errors
        if "error" in result:
            error_msg = result.get("error_description", result["error"])
            raise ValueError(f"OAuth error: {error_msg}")

        # Validate required parameters for success
        if "code" not in result:
            raise ValueError("Missing authorization code in callback")

        if "state" not in result:
            raise ValueError("Missing state parameter in callback")

        return result

    def handle_oauth_callback(
        self, callback_url: str, expected_state: str, code_verifier: str
    ) -> Dict[str, Any]:
        """
        Complete OAuth flow by handling callback and exchanging code for token.

        Args:
            callback_url: OAuth callback URL
            expected_state: Expected state parameter for CSRF protection
            code_verifier: PKCE code verifier

        Returns:
            Token data dictionary

        Raises:
            ValueError: If OAuth flow fails
        """
        # Parse callback URL
        callback_data = self.parse_callback_url(callback_url)

        # Validate state parameter
        if callback_data["state"] != expected_state:
            raise ValueError("State parameter mismatch - possible CSRF attack")

        # Exchange code for token
        token_data = self.exchange_code_for_token(callback_data["code"], code_verifier)

        # Validate token and scopes
        if not self.validate_token(token_data["access_token"]):
            raise ValueError("Invalid access token received")

        if not self.validate_scopes(token_data):
            raise ValueError("Token missing required scopes")

        return token_data

    def create_user_from_token_data(self, token_data: Dict[str, Any]) -> User:
        """
        Create a User object from OAuth token data.

        Args:
            token_data: OAuth token response data

        Returns:
            User object with OAuth data
        """
        user = User()

        # Set basic user info
        if "owner" in token_data and token_data["owner"]["type"] == "user":
            owner_data = token_data["owner"]["user"]
            user.id = owner_data.get("id", "unknown")
            user.name = owner_data.get("name", "Unknown User")

        # Set OAuth data
        user.set_notion_oauth_data(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            workspace_id=token_data.get("workspace_id"),
            workspace_name=token_data.get("workspace_name"),
            token_expires_at=token_data.get("expires_at"),
        )

        return user

    def is_token_expired(self, token_data: Dict[str, Any]) -> bool:
        """
        Check if access token is expired.

        Args:
            token_data: Token data dictionary

        Returns:
            True if token is expired
        """
        if "expires_at" not in token_data:
            return False  # Assume not expired if no expiry info

        expires_at = token_data["expires_at"]
        if isinstance(expires_at, str):
            expires_at = datetime.fromisoformat(expires_at)

        return datetime.now() > expires_at

    def __str__(self) -> str:
        """String representation of OAuth service."""
        return f"NotionOAuthService(client_id={self.client_id[:8]}...)"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"NotionOAuthService(client_id={self.client_id[:8]}..., redirect_uri={self.redirect_uri})"
