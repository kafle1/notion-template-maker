"""
Error Handler UI Component for Notion Template Maker.
Handles and displays errors in a user-friendly way.
"""

import streamlit as st
from typing import Any, Optional, Dict, List, Union
import traceback
import json
from datetime import datetime


def handle_error(
    error: Union[Exception, str],
    context: Optional[str] = None,
    show_traceback: bool = False,
    recovery_options: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Handle and display errors in a user-friendly way.

    Args:
        error: Exception object or error message string
        context: Additional context about where the error occurred
        show_traceback: Whether to show full traceback (debug mode)
        recovery_options: List of recovery action dictionaries

    Returns:
        Error handling result dictionary
    """
    # Extract error information
    error_info = _extract_error_info(error)

    # Log error for debugging
    _log_error(error_info, context)

    # Display error to user
    result = _display_error_ui(error_info, context, show_traceback, recovery_options)

    return result


def _extract_error_info(error: Union[Exception, str]) -> Dict[str, Any]:
    """
    Extract information from error object.

    Args:
        error: Exception or error string

    Returns:
        Error information dictionary
    """
    if isinstance(error, str):
        return {
            "type": "StringError",
            "message": error,
            "traceback": None,
            "module": None,
            "line": None,
        }

    error_type = type(error).__name__
    error_message = str(error)

    # Get traceback
    tb_str = None
    try:
        tb_str = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
    except:
        tb_str = "Could not extract traceback"

    # Extract module and line info
    module = None
    line = None
    if hasattr(error, "__traceback__") and error.__traceback__:
        tb_frame = error.__traceback__
        while tb_frame:
            if tb_frame.tb_frame.f_code.co_name not in [
                "handle_error",
                "_extract_error_info",
            ]:
                module = tb_frame.tb_frame.f_code.co_filename
                line = tb_frame.tb_lineno
                break
            tb_frame = tb_frame.tb_next

    return {
        "type": error_type,
        "message": error_message,
        "traceback": tb_str,
        "module": module,
        "line": line,
        "timestamp": datetime.now().isoformat(),
    }


def _log_error(error_info: Dict[str, Any], context: Optional[str]):
    """
    Log error for debugging purposes.

    Args:
        error_info: Error information dictionary
        context: Additional context
    """
    # In a real application, this would log to a file or external service
    print(
        f"ERROR [{error_info['timestamp']}]: {error_info['type']}: {error_info['message']}"
    )
    if context:
        print(f"CONTEXT: {context}")
    if error_info["module"] and error_info["line"]:
        print(f"LOCATION: {error_info['module']}:{error_info['line']}")


def _display_error_ui(
    error_info: Dict[str, Any],
    context: Optional[str],
    show_traceback: bool,
    recovery_options: Optional[List[Dict[str, Any]]],
) -> Dict[str, Any]:
    """
    Display error information in the UI.

    Args:
        error_info: Error information dictionary
        context: Additional context
        show_traceback: Whether to show traceback
        recovery_options: Recovery action options

    Returns:
        User action result
    """
    # Error header
    st.error("❌ Something went wrong")

    # Error message
    st.markdown(f"**Error:** {error_info['message']}")

    # Context information
    if context:
        st.info(f"**Context:** {context}")

    # Error type and location
    with st.expander("🔍 Error Details", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Type:** {error_info['type']}")
            if error_info["module"]:
                st.markdown(f"**File:** {error_info['module']}")
            if error_info["line"]:
                st.markdown(f"**Line:** {error_info['line']}")

        with col2:
            st.markdown(f"**Time:** {error_info['timestamp']}")

        # Traceback (if enabled)
        if show_traceback and error_info["traceback"]:
            st.markdown("**Traceback:**")
            st.code(error_info["traceback"], language="text")

    # Recovery options
    if recovery_options:
        st.subheader("🔧 Recovery Options")

        for option in recovery_options:
            if st.button(
                option.get("label", "Try Again"),
                key=f"recovery_{option.get('key', 'default')}",
                help=option.get("help", ""),
            ):
                return {
                    "action": "recovery",
                    "recovery_key": option.get("key"),
                    "error_info": error_info,
                }

    # Default actions
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Try Again", use_container_width=True):
            return {"action": "retry", "error_info": error_info}

    with col2:
        if st.button("🏠 Go Home", use_container_width=True):
            return {"action": "home", "error_info": error_info}

    with col3:
        if st.button("📧 Report Issue", use_container_width=True):
            return {"action": "report", "error_info": error_info}

    return {"action": "displayed", "error_info": error_info}


def handle_api_error(
    response: Dict[str, Any], operation: str = "API call"
) -> Optional[Dict[str, Any]]:
    """
    Handle API-specific errors.

    Args:
        response: API response dictionary
        operation: Description of the operation that failed

    Returns:
        Error handling result or None if no error
    """
    if not isinstance(response, dict):
        handle_error(f"Invalid API response format for {operation}")
        return {"action": "error", "type": "invalid_response"}

    # Check for common API error patterns
    if response.get("error"):
        error_msg = response["error"].get("message", "Unknown API error")
        handle_error(f"API Error in {operation}: {error_msg}")
        return {"action": "api_error", "error": response["error"]}

    if response.get("status") == "error":
        error_msg = response.get("message", "API operation failed")
        handle_error(f"API Error in {operation}: {error_msg}")
        return {"action": "api_error", "message": error_msg}

    # HTTP status codes
    status_code = response.get("status_code", response.get("status"))
    if status_code and status_code >= 400:
        error_msg = response.get(
            "detail", response.get("message", f"HTTP {status_code}")
        )
        handle_error(f"HTTP Error in {operation}: {error_msg}")
        return {"action": "http_error", "status_code": status_code}

    return None  # No error


def handle_validation_error(
    errors: Union[List[str], Dict[str, Any]], field_name: str = "input"
) -> Dict[str, Any]:
    """
    Handle validation errors.

    Args:
        errors: List of error messages or error dictionary
        field_name: Name of the field being validated

    Returns:
        Error handling result
    """
    if isinstance(errors, list):
        error_messages = errors
    elif isinstance(errors, dict):
        error_messages = []
        for field, field_errors in errors.items():
            if isinstance(field_errors, list):
                for error in field_errors:
                    error_messages.append(f"{field}: {error}")
            else:
                error_messages.append(f"{field}: {field_errors}")
    else:
        error_messages = [str(errors)]

    # Display validation errors
    st.warning(f"⚠️ Validation Issues with {field_name}")

    for error in error_messages:
        st.error(f"• {error}")

    # Provide help
    with st.expander("💡 How to fix", expanded=False):
        st.markdown(
            """
        **Common fixes:**
        - Check that all required fields are filled
        - Ensure text lengths are within limits
        - Verify email formats are correct
        - Make sure dates are in the correct format
        - Confirm API keys are valid
        """
        )

    return {"action": "validation_error", "errors": error_messages, "field": field_name}


def handle_connection_error(
    service_name: str, retry_count: int = 0, max_retries: int = 3
) -> Dict[str, Any]:
    """
    Handle connection/network errors.

    Args:
        service_name: Name of the service that failed
        retry_count: Current retry attempt
        max_retries: Maximum retry attempts

    Returns:
        Error handling result
    """
    st.error(f"🔌 Connection Error: Cannot connect to {service_name}")

    st.info("This might be due to:")
    st.markdown("- Network connectivity issues")
    st.markdown("- Service temporarily unavailable")
    st.markdown("- Firewall or proxy settings")
    st.markdown(f"- {service_name} service maintenance")

    # Retry options
    if retry_count < max_retries:
        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                f"🔄 Retry ({retry_count + 1}/{max_retries})", use_container_width=True
            ):
                return {
                    "action": "retry",
                    "retry_count": retry_count + 1,
                    "service": service_name,
                }

        with col2:
            if st.button("⚙️ Check Settings", use_container_width=True):
                return {"action": "check_settings", "service": service_name}
    else:
        st.warning(f"Maximum retries ({max_retries}) exceeded for {service_name}")

        if st.button("🏠 Return to Home", use_container_width=True):
            return {"action": "home", "service": service_name}

    return {
        "action": "connection_error",
        "service": service_name,
        "retry_count": retry_count,
    }


def handle_permission_error(
    resource: str, required_permission: str = "access"
) -> Dict[str, Any]:
    """
    Handle permission/authorization errors.

    Args:
        resource: Resource that requires permission
        required_permission: Type of permission needed

    Returns:
        Error handling result
    """
    st.error(f"🔒 Permission Denied: Cannot {required_permission} {resource}")

    st.info("This might be because:")
    st.markdown("- You don't have the required permissions")
    st.markdown("- Your session has expired")
    st.markdown("- The resource is restricted")
    st.markdown("- API keys have insufficient scope")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔑 Update Permissions", use_container_width=True):
            return {
                "action": "update_permissions",
                "resource": resource,
                "permission": required_permission,
            }

    with col2:
        if st.button("🔄 Re-authenticate", use_container_width=True):
            return {"action": "re_authenticate", "resource": resource}

    return {
        "action": "permission_error",
        "resource": resource,
        "permission": required_permission,
    }


def create_error_boundary(func: callable) -> callable:
    """
    Create an error boundary wrapper for functions.

    Args:
        func: Function to wrap

    Returns:
        Wrapped function with error handling
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            result = handle_error(e, f"Error in {func.__name__}")
            return None  # Or appropriate default value

    return wrapper


class ErrorHandler:
    """Class-based error handler for more complex scenarios."""

    def __init__(self):
        self.errors = []
        self.warnings = []

    def add_error(self, error: Union[Exception, str], context: Optional[str] = None):
        """Add an error to the handler."""
        error_info = _extract_error_info(error)
        if context:
            error_info["context"] = context
        self.errors.append(error_info)

    def add_warning(self, warning: str, context: Optional[str] = None):
        """Add a warning to the handler."""
        self.warnings.append(
            {
                "message": warning,
                "context": context,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0

    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0

    def display_all(self, show_traceback: bool = False):
        """Display all errors and warnings."""
        # Display errors
        for error in self.errors:
            handle_error(error, error.get("context"), show_traceback)

        # Display warnings
        for warning in self.warnings:
            st.warning(f"⚠️ {warning['message']}")
            if warning.get("context"):
                st.caption(f"Context: {warning['context']}")

    def clear(self):
        """Clear all errors and warnings."""
        self.errors.clear()
        self.warnings.clear()

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of errors and warnings."""
        return {
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "has_errors": self.has_errors(),
            "has_warnings": self.has_warnings(),
        }


# Export functions and classes
__all__ = [
    "handle_error",
    "handle_api_error",
    "handle_validation_error",
    "handle_connection_error",
    "handle_permission_error",
    "create_error_boundary",
    "ErrorHandler",
]
