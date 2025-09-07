"""
API Configuration UI Component for Notion Template Maker.
Handles API key input and validation display.
"""

import streamlit as st
from typing import Dict, Any, Optional, Callable
import re
from src.utils.input_validator import InputValidator


def render_api_config(
    on_api_key_change: Optional[Callable[[str, str], None]] = None,
    session_manager: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Render the API configuration component.

    Args:
        on_api_key_change: Callback function when API keys change
        session_manager: Session manager instance

    Returns:
        Dictionary with current API configuration status
    """
    st.header("🔧 API Configuration")

    config_status = {
        "openrouter_configured": False,
        "notion_configured": False,
        "all_configured": False,
    }

    # OpenRouter API Configuration
    st.subheader("🤖 OpenRouter API")
    openrouter_config = _render_openrouter_config(on_api_key_change, session_manager)
    config_status["openrouter_configured"] = openrouter_config["configured"]

    st.divider()

    # Notion API Configuration
    st.subheader("📝 Notion Integration")
    notion_config = _render_notion_config(on_api_key_change, session_manager)
    config_status["notion_configured"] = notion_config["configured"]

    # Overall status
    config_status["all_configured"] = (
        config_status["openrouter_configured"] and config_status["notion_configured"]
    )

    # Status summary
    _render_config_status(config_status)

    return config_status


def _render_openrouter_config(
    on_api_key_change: Optional[Callable[[str, str], None]],
    session_manager: Optional[Any],
) -> Dict[str, Any]:
    """
    Render OpenRouter API configuration section.

    Returns:
        Configuration status dictionary
    """
    config_status = {"configured": False, "api_key": None, "valid": False}

    # Get existing API key from session
    existing_key = None
    if (
        session_manager
        and hasattr(st, "session_state")
        and st.session_state.get("session_id")
    ):
        existing_key = session_manager.get_api_key(
            st.session_state.session_id, "openrouter"
        )

    # API Key input
    api_key = st.text_input(
        "OpenRouter API Key",
        value=existing_key or "",
        type="password",
        help="Get your API key from https://openrouter.ai/keys",
        key="openrouter_api_key",
    )

    # Validate API key format
    if api_key:
        validation_result = InputValidator.validate_api_key(api_key, "openrouter")
        config_status["valid"] = validation_result["valid"]
        config_status["api_key"] = api_key

        if validation_result["valid"]:
            st.success("✅ Valid API key format")
            config_status["configured"] = True

            # Store in session if session manager provided
            if (
                session_manager
                and hasattr(st, "session_state")
                and st.session_state.get("session_id")
            ):
                session_manager.store_api_key(
                    st.session_state.session_id, "openrouter", api_key
                )

            # Call callback if provided
            if on_api_key_change:
                on_api_key_change("openrouter", api_key)
        else:
            for error in validation_result["errors"]:
                st.error(f"❌ {error}")
            config_status["configured"] = False
    else:
        st.info(
            "🔑 Enter your OpenRouter API key to enable AI-powered template generation"
        )
        config_status["configured"] = False

    # Additional information
    with st.expander("ℹ️ How to get an OpenRouter API key"):
        st.markdown(
            """
        1. Visit [OpenRouter.ai](https://openrouter.ai)
        2. Sign up for an account
        3. Navigate to the API Keys section
        4. Create a new API key
        5. Copy and paste it here

        **Note:** OpenRouter provides access to multiple AI models including GPT, Claude, and others.
        """
        )

    return config_status


def _render_notion_config(
    on_api_key_change: Optional[Callable[[str, str], None]],
    session_manager: Optional[Any],
) -> Dict[str, Any]:
    """
    Render Notion API configuration section.

    Returns:
        Configuration status dictionary
    """
    config_status = {
        "configured": False,
        "integration_token": None,
        "oauth_connected": False,
    }

    # Option 1: OAuth Flow (Recommended)
    st.markdown("**Option 1: OAuth Integration (Recommended)**")
    if st.button(
        "🔗 Connect with Notion OAuth", type="primary", use_container_width=True
    ):
        _initiate_notion_oauth()

    st.caption("Secure, no API key needed. Allows full workspace access.")

    st.divider()

    # Option 2: Integration Token (Advanced)
    st.markdown("**Option 2: Integration Token (Advanced)**")

    # Workspace restriction notice for integration token
    st.warning("⚠️ **Workspace Restriction:** This integration token only works with Niraj's Notion workspace. To change workspace, you would need to create a new integration in your own Notion account.")

    # Get existing token from session
    existing_token = None
    if (
        session_manager
        and hasattr(st, "session_state")
        and st.session_state.get("session_id")
    ):
        existing_token = session_manager.get_api_key(
            st.session_state.session_id, "notion"
        )

    integration_token = st.text_input(
        "Notion Integration Token",
        value=existing_token or "",
        type="password",
        help="Create an integration at https://developers.notion.com",
        key="notion_integration_token",
    )

    if integration_token:
        validation_result = InputValidator.validate_api_key(integration_token, "notion")
        if validation_result["valid"]:
            st.success("✅ Valid integration token format")
            config_status["configured"] = True
            config_status["integration_token"] = integration_token

            # Test connection button
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🔍 Test Connection", key="test_notion_connection"):
                    with st.spinner("Testing connection..."):
                        try:
                            from src.api.notion_client import NotionClient
                            client = NotionClient(integration_token=integration_token)
                            test_result = client.test_integration_connection()

                            if test_result["connected"]:
                                st.success("✅ Connection successful!")
                                if test_result["user_info"]:
                                    st.info(f"Connected as: {test_result['user_info'].get('name', 'Unknown User')}")
                            else:
                                st.error(f"❌ Connection failed: {test_result['error']}")
                        except Exception as e:
                            st.error(f"❌ Test failed: {str(e)}")

            with col2:
                if st.button("🔄 Refresh Token", key="refresh_notion_token"):
                    st.rerun()

            # Store in session if session manager provided
            if (
                session_manager
                and hasattr(st, "session_state")
                and st.session_state.session_id
            ):
                session_manager.store_api_key(
                    st.session_state.session_id, "notion", integration_token
                )

            # Call callback if provided
            if on_api_key_change:
                on_api_key_change("notion", integration_token)
        else:
            for error in validation_result["errors"]:
                st.error(f"❌ {error}")
            config_status["configured"] = False
    else:
        st.info("🔑 Or enter your Notion Integration Token for advanced access")
        config_status["configured"] = False

    # Additional information
    with st.expander("ℹ️ How to set up Notion Integration"):
        st.markdown(
            """
        **For Integration Token:**
        1. Go to [Notion Developers](https://developers.notion.com)
        2. Create a new integration
        3. Copy the Internal Integration Token
        4. Share your pages/databases with the integration
        5. Paste the token here

        **⚠️ Important Notes:**
        - This integration token is configured to work only with Niraj's Notion workspace
        - If you need to access a different workspace, create your own integration
        - Make sure the integration has the necessary permissions for your use case

        **For OAuth:**
        - Click the "Connect with Notion OAuth" button above
        - Authorize the application
        - Automatic setup completed

        **Permissions needed:**
        - Read content
        - Update content
        - Insert content
        """
        )

    return config_status


def _render_config_status(config_status: Dict[str, Any]):
    """Render overall configuration status."""
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if config_status["openrouter_configured"]:
            st.success("✅ OpenRouter: Configured")
        else:
            st.error("❌ OpenRouter: Not configured")

    with col2:
        if config_status["notion_configured"]:
            st.success("✅ Notion: Configured")
        else:
            st.warning("⚠️ Notion: Not configured")

    # Overall status
    if config_status["all_configured"]:
        st.success("🎉 All APIs configured! You're ready to generate templates.")
    else:
        st.info("⚙️ Please configure all APIs to unlock full functionality.")


def _validate_openrouter_key(api_key: str) -> bool:
    """
    Validate OpenRouter API key format.

    Args:
        api_key: API key to validate

    Returns:
        True if valid format, False otherwise
    """
    if not api_key or not isinstance(api_key, str):
        return False

    # OpenRouter keys typically start with 'sk-or-v1-'
    pattern = r"^sk-or-v1-[a-f0-9]{64}$"
    return bool(re.match(pattern, api_key.strip()))


def _validate_notion_token(token: str) -> bool:
    """
    Validate Notion integration token format.

    Args:
        token: Integration token to validate

    Returns:
        True if valid format, False otherwise
    """
    if not token or not isinstance(token, str):
        return False

    # Notion integration tokens start with 'secret_'
    pattern = r"^secret_[a-zA-Z0-9]{43}$"
    return bool(re.match(pattern, token.strip()))


def _initiate_notion_oauth():
    """
    Initiate Notion OAuth flow.
    This would redirect to Notion's OAuth endpoint in a real implementation.
    """
    st.info("🔄 OAuth flow would be initiated here")
    st.markdown(
        """
    In a production app, this would:
    1. Redirect to Notion's OAuth authorization URL
    2. Handle the callback with authorization code
    3. Exchange code for access token
    4. Store the token securely
    """
    )


def get_api_config_status(session_manager: Optional[Any] = None) -> Dict[str, Any]:
    """
    Get current API configuration status.

    Args:
        session_manager: Session manager instance

    Returns:
        Configuration status dictionary
    """
    if (
        not session_manager
        or not hasattr(st, "session_state")
        or not st.session_state.get("session_id")
    ):
        return {
            "openrouter_configured": False,
            "notion_configured": False,
            "all_configured": False,
        }

    session_id = st.session_state.session_id

    return {
        "openrouter_configured": bool(
            session_manager.get_api_key(session_id, "openrouter")
        ),
        "notion_configured": bool(session_manager.get_api_key(session_id, "notion")),
        "all_configured": bool(
            session_manager.get_api_key(session_id, "openrouter")
            and session_manager.get_api_key(session_id, "notion")
        ),
    }


# Export the main function
__all__ = ["render_api_config", "get_api_config_status"]
