"""
Session management service for the Notion Template Maker application.
Handles user sessions, API keys, and secure storage.
"""

import os
import json
import base64
from typing import Optional, Dict, Any, Union
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets


class SessionManager:
    """Service for managing user sessions and secure data storage."""

    # Session constants
    SESSION_TIMEOUT_HOURS = 24
    MAX_SESSIONS_PER_USER = 5
    ENCRYPTION_KEY_LENGTH = 32

    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize session manager.

        Args:
            encryption_key: Base64-encoded encryption key (optional)
        """
        self.encryption_key = encryption_key or self._generate_encryption_key()
        self._fernet = Fernet(self.encryption_key)
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def _generate_encryption_key(self) -> str:
        """
        Generate a new encryption key for session data.

        Returns:
            Base64-encoded encryption key
        """
        # Use PBKDF2 to derive a key from a random salt
        salt = secrets.token_bytes(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.ENCRYPTION_KEY_LENGTH,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(secrets.token_bytes(32)))
        return key.decode()

    def create_session(
        self, user_id: str, user_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new session for a user.

        Args:
            user_id: Unique user identifier
            user_data: Additional user data to store

        Returns:
            Session ID
        """
        # Clean up expired sessions first
        self._cleanup_expired_sessions()

        # Check session limit
        user_sessions = [
            s for s in self._sessions.values() if s.get("user_id") == user_id
        ]
        if len(user_sessions) >= self.MAX_SESSIONS_PER_USER:
            # Remove oldest session
            oldest_session = min(
                user_sessions, key=lambda s: s.get("created_at", datetime.min)
            )
            self._sessions = {
                k: v for k, v in self._sessions.items() if v != oldest_session
            }

        # Generate session ID
        session_id = secrets.token_urlsafe(32)

        # Create session data
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "expires_at": (
                datetime.now() + timedelta(hours=self.SESSION_TIMEOUT_HOURS)
            ).isoformat(),
            "user_data": user_data or {},
            "api_keys": {},
            "preferences": {},
        }

        # Encrypt sensitive data
        session_data["encrypted_data"] = self._encrypt_session_data(session_data)

        self._sessions[session_id] = session_data

        return session_id

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve session data by session ID.

        Args:
            session_id: Session identifier

        Returns:
            Session data or None if not found/expired
        """
        session = self._sessions.get(session_id)
        if not session:
            return None

        # Check if session is expired
        expires_at = datetime.fromisoformat(session.get("expires_at", ""))
        if datetime.now() > expires_at:
            self.delete_session(session_id)
            return None

        # Decrypt and return session data
        try:
            decrypted_data = self._decrypt_session_data(
                session.get("encrypted_data", "")
            )
            return decrypted_data
        except Exception:
            # If decryption fails, session is invalid
            self.delete_session(session_id)
            return None

    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update session data.

        Args:
            session_id: Session identifier
            updates: Data to update

        Returns:
            True if update successful, False otherwise
        """
        session = self._sessions.get(session_id)
        if not session:
            return False

        # Check if session is expired
        expires_at = datetime.fromisoformat(session.get("expires_at", ""))
        if datetime.now() > expires_at:
            self.delete_session(session_id)
            return False

        # Update session data
        for key, value in updates.items():
            if key in ["session_id", "created_at", "expires_at"]:
                continue  # Don't allow updating system fields
            session[key] = value

        # Re-encrypt sensitive data
        session["encrypted_data"] = self._encrypt_session_data(session)

        return True

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.

        Args:
            session_id: Session identifier

        Returns:
            True if deletion successful, False otherwise
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def store_api_key(self, session_id: str, provider: str, api_key: str) -> bool:
        """
        Store an API key securely in the session.

        Args:
            session_id: Session identifier
            provider: API provider name (e.g., 'openrouter', 'notion')
            api_key: API key to store

        Returns:
            True if storage successful, False otherwise
        """
        session = self._sessions.get(session_id)
        if not session:
            return False

        # Encrypt the API key
        encrypted_key = self._fernet.encrypt(api_key.encode()).decode()

        # Store in session
        if "api_keys" not in session:
            session["api_keys"] = {}
        session["api_keys"][provider] = {
            "encrypted_key": encrypted_key,
            "stored_at": datetime.now().isoformat(),
        }

        # Update encrypted data
        session["encrypted_data"] = self._encrypt_session_data(session)

        return True

    def get_api_key(self, session_id: str, provider: str) -> Optional[str]:
        """
        Retrieve an API key from the session.

        Args:
            session_id: Session identifier
            provider: API provider name

        Returns:
            Decrypted API key or None if not found
        """
        session = self._sessions.get(session_id)
        if not session:
            return None

        api_keys = session.get("api_keys", {})
        key_data = api_keys.get(provider)
        if not key_data:
            return None

        try:
            encrypted_key = key_data.get("encrypted_key", "")
            decrypted_key = self._fernet.decrypt(encrypted_key.encode()).decode()
            return decrypted_key
        except Exception:
            return None

    def remove_api_key(self, session_id: str, provider: str) -> bool:
        """
        Remove an API key from the session.

        Args:
            session_id: Session identifier
            provider: API provider name

        Returns:
            True if removal successful, False otherwise
        """
        session = self._sessions.get(session_id)
        if not session:
            return False

        api_keys = session.get("api_keys", {})
        if provider in api_keys:
            del api_keys[provider]
            session["encrypted_data"] = self._encrypt_session_data(session)
            return True
        return False

    def store_oauth_data(self, session_id: str, oauth_data: Dict[str, Any]) -> bool:
        """
        Store OAuth token data securely in the session.

        Args:
            session_id: Session identifier
            oauth_data: OAuth token data to store

        Returns:
            True if storage successful, False otherwise
        """
        session = self._sessions.get(session_id)
        if not session:
            return False

        # Encrypt sensitive OAuth data
        encrypted_oauth = {}
        for key, value in oauth_data.items():
            if key in ["access_token", "refresh_token"]:
                encrypted_oauth[key] = self._fernet.encrypt(
                    str(value).encode()
                ).decode()
            else:
                encrypted_oauth[key] = value

        # Store in session
        session["oauth_data"] = {
            "encrypted_data": encrypted_oauth,
            "stored_at": datetime.now().isoformat(),
        }

        # Update encrypted data
        session["encrypted_data"] = self._encrypt_session_data(session)

        return True

    def get_oauth_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve OAuth token data from the session.

        Args:
            session_id: Session identifier

        Returns:
            Decrypted OAuth data or None if not found
        """
        session = self._sessions.get(session_id)
        if not session:
            return None

        oauth_info = session.get("oauth_data")
        if not oauth_info:
            return None

        try:
            encrypted_data = oauth_info.get("encrypted_data", {})
            decrypted_data = {}

            # Decrypt sensitive fields
            for key, value in encrypted_data.items():
                if key in ["access_token", "refresh_token"]:
                    decrypted_data[key] = self._fernet.decrypt(value.encode()).decode()
                else:
                    decrypted_data[key] = value

            return decrypted_data
        except Exception:
            return None

    def remove_oauth_data(self, session_id: str) -> bool:
        """
        Remove OAuth data from the session.

        Args:
            session_id: Session identifier

        Returns:
            True if removal successful, False otherwise
        """
        session = self._sessions.get(session_id)
        if not session:
            return False

        if "oauth_data" in session:
            del session["oauth_data"]
            session["encrypted_data"] = self._encrypt_session_data(session)
            return True
        return False

    def extend_session(
        self, session_id: str, hours: int = SESSION_TIMEOUT_HOURS
    ) -> bool:
        """
        Extend session expiration time.

        Args:
            session_id: Session identifier
            hours: Hours to extend

        Returns:
            True if extension successful, False otherwise
        """
        session = self._sessions.get(session_id)
        if not session:
            return False

        new_expires_at = datetime.now() + timedelta(hours=hours)
        session["expires_at"] = new_expires_at.isoformat()
        session["encrypted_data"] = self._encrypt_session_data(session)

        return True

    def get_user_sessions(self, user_id: str) -> list:
        """
        Get all active sessions for a user.

        Args:
            user_id: User identifier

        Returns:
            List of session data dictionaries
        """
        user_sessions = []
        for session in self._sessions.values():
            if session.get("user_id") == user_id:
                expires_at = datetime.fromisoformat(session.get("expires_at", ""))
                if datetime.now() <= expires_at:
                    user_sessions.append(
                        {
                            "session_id": session.get("session_id"),
                            "created_at": session.get("created_at"),
                            "expires_at": session.get("expires_at"),
                        }
                    )

        return user_sessions

    def _encrypt_session_data(self, session_data: Dict[str, Any]) -> str:
        """
        Encrypt sensitive session data.

        Args:
            session_data: Session data to encrypt

        Returns:
            Encrypted data as base64 string
        """
        # Extract sensitive data
        sensitive_data = {
            "user_data": session_data.get("user_data", {}),
            "api_keys": session_data.get("api_keys", {}),
            "oauth_data": session_data.get("oauth_data", {}),
            "preferences": session_data.get("preferences", {}),
        }

        # Encrypt
        json_data = json.dumps(sensitive_data)
        encrypted = self._fernet.encrypt(json_data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def _decrypt_session_data(self, encrypted_data: str) -> Dict[str, Any]:
        """
        Decrypt session data.

        Args:
            encrypted_data: Encrypted data as base64 string

        Returns:
            Decrypted session data
        """
        encrypted = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = self._fernet.decrypt(encrypted)
        return json.loads(decrypted.decode())

    def _cleanup_expired_sessions(self):
        """Remove expired sessions from memory."""
        current_time = datetime.now()
        expired_sessions = []

        for session_id, session in self._sessions.items():
            expires_at = datetime.fromisoformat(session.get("expires_at", ""))
            if current_time > expires_at:
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            del self._sessions[session_id]

    def get_session_stats(self) -> Dict[str, Any]:
        """
        Get session statistics.

        Returns:
            Dictionary with session statistics
        """
        total_sessions = len(self._sessions)
        active_sessions = 0
        expired_sessions = 0

        for session in self._sessions.values():
            expires_at = datetime.fromisoformat(session.get("expires_at", ""))
            if datetime.now() <= expires_at:
                active_sessions += 1
            else:
                expired_sessions += 1

        return {
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "expired_sessions": expired_sessions,
        }

    def rotate_encryption_key(self) -> bool:
        """
        Rotate the encryption key for enhanced security.
        This will re-encrypt all existing session data with a new key.

        Returns:
            True if rotation successful, False otherwise
        """
        try:
            # Generate new key
            new_key = self._generate_encryption_key()
            new_fernet = Fernet(new_key)

            # Re-encrypt all sessions
            for session_id, session in self._sessions.items():
                if "encrypted_data" in session:
                    # Decrypt with old key
                    old_encrypted = base64.urlsafe_b64decode(
                        session["encrypted_data"].encode()
                    )
                    decrypted = self._fernet.decrypt(old_encrypted)
                    json_data = decrypted.decode()

                    # Re-encrypt with new key
                    new_encrypted = new_fernet.encrypt(json_data.encode())
                    session["encrypted_data"] = base64.urlsafe_b64encode(
                        new_encrypted
                    ).decode()

            # Update to new key
            self.encryption_key = new_key
            self._fernet = new_fernet

            return True
        except Exception:
            return False

    def validate_encryption_key(self) -> bool:
        """
        Validate that the current encryption key is working properly.

        Returns:
            True if key is valid, False otherwise
        """
        try:
            # Test encryption/decryption with dummy data
            test_data = {"test": "data"}
            json_data = json.dumps(test_data)
            encrypted = self._fernet.encrypt(json_data.encode())
            decrypted = self._fernet.decrypt(encrypted)
            result = json.loads(decrypted.decode())

            return result == test_data
        except Exception:
            return False

    def get_encryption_info(self) -> Dict[str, Any]:
        """
        Get information about the current encryption setup.

        Returns:
            Dictionary with encryption information
        """
        return {
            "key_valid": self.validate_encryption_key(),
            "total_sessions": len(self._sessions),
            "encrypted_sessions": sum(
                1 for s in self._sessions.values() if "encrypted_data" in s
            ),
            "key_rotation_available": True,
        }
        """String representation of the session manager."""
        stats = self.get_session_stats()
        return f"SessionManager(active_sessions={stats['active_sessions']})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        stats = self.get_session_stats()
        return f"SessionManager(total={stats['total_sessions']}, active={stats['active_sessions']}, expired={stats['expired_sessions']})"
