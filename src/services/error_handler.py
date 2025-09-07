"""
Error handling service for the Notion Template Maker application.
Provides comprehensive error handling, recovery, and user-friendly error messages.
"""

import traceback
import sys
from typing import Dict, Any, Optional, Callable, List, Union
from datetime import datetime
from enum import Enum
from contextlib import contextmanager
import streamlit as st

from src.services.logging_service import get_logger

logger = get_logger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for better classification."""

    NETWORK = "network"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    VALIDATION = "validation"
    API = "api"
    DATABASE = "database"
    FILESYSTEM = "filesystem"
    CONFIGURATION = "configuration"
    BUSINESS_LOGIC = "business_logic"
    UNKNOWN = "unknown"


class AppError(Exception):
    """Base exception class for application errors."""

    def __init__(
        self,
        message: str,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        user_message: Optional[str] = None,
        recovery_suggestions: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize application error.

        Args:
            message: Technical error message
            category: Error category
            severity: Error severity
            user_message: User-friendly message
            recovery_suggestions: List of recovery suggestions
            context: Additional context information
        """
        super().__init__(message)
        self.message = message
        self.category = category
        self.severity = severity
        self.user_message = user_message or self._generate_user_message()
        self.recovery_suggestions = recovery_suggestions or []
        self.context = context or {}
        self.timestamp = datetime.now()
        self.traceback = traceback.format_exc()

    def _generate_user_message(self) -> str:
        """Generate user-friendly message based on error category."""
        category_messages = {
            ErrorCategory.NETWORK: "Network connection issue. Please check your internet connection.",
            ErrorCategory.AUTHENTICATION: "Authentication failed. Please check your credentials.",
            ErrorCategory.AUTHORIZATION: "Access denied. You may not have permission for this action.",
            ErrorCategory.VALIDATION: "Invalid input. Please check your data and try again.",
            ErrorCategory.API: "Service temporarily unavailable. Please try again later.",
            ErrorCategory.DATABASE: "Data storage issue. Your data is safe, but please try again.",
            ErrorCategory.FILESYSTEM: "File system error. Please check file permissions.",
            ErrorCategory.CONFIGURATION: "Configuration issue. Please contact support.",
            ErrorCategory.BUSINESS_LOGIC: "Operation cannot be completed. Please try a different approach.",
            ErrorCategory.UNKNOWN: "An unexpected error occurred. Please try again.",
        }
        return category_messages.get(
            self.category, category_messages[ErrorCategory.UNKNOWN]
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary."""
        return {
            "message": self.message,
            "category": self.category.value,
            "severity": self.severity.value,
            "user_message": self.user_message,
            "recovery_suggestions": self.recovery_suggestions,
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
            "traceback": self.traceback,
        }


class ErrorHandler:
    """Comprehensive error handling service."""

    def __init__(self):
        self.error_handlers: Dict[ErrorCategory, List[Callable]] = {}
        self.recovery_strategies: Dict[ErrorCategory, List[Callable]] = {}
        self.error_counts: Dict[str, int] = {}
        self.max_retries = 3

    def register_error_handler(self, category: ErrorCategory, handler: Callable):
        """
        Register an error handler for a specific category.

        Args:
            category: Error category
            handler: Handler function
        """
        if category not in self.error_handlers:
            self.error_handlers[category] = []
        self.error_handlers[category].append(handler)

    def register_recovery_strategy(self, category: ErrorCategory, strategy: Callable):
        """
        Register a recovery strategy for a specific category.

        Args:
            category: Error category
            strategy: Recovery function
        """
        if category not in self.recovery_strategies:
            self.recovery_strategies[category] = []
        self.recovery_strategies[category].append(strategy)

    def handle_error(
        self,
        error: Union[Exception, AppError],
        context: Optional[Dict[str, Any]] = None,
    ) -> AppError:
        """
        Handle an error comprehensively.

        Args:
            error: The error to handle
            context: Additional context

        Returns:
            AppError instance
        """
        # Convert to AppError if needed
        if isinstance(error, AppError):
            app_error = error
        else:
            app_error = self._classify_error(error)

        # Add context
        if context:
            app_error.context.update(context)

        # Log error
        logger.log_error(app_error, app_error.context, app_error.user_message)

        # Track error counts
        error_key = f"{app_error.category.value}:{type(error).__name__}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1

        # Run category-specific handlers
        for handler in self.error_handlers.get(app_error.category, []):
            try:
                handler(app_error)
            except Exception as handler_error:
                logger.error(f"Error handler failed: {handler_error}")

        # Attempt recovery
        if app_error.severity != ErrorSeverity.CRITICAL:
            self._attempt_recovery(app_error)

        return app_error

    def _classify_error(self, error: Exception) -> AppError:
        """Classify a generic exception into an AppError."""
        error_message = str(error)
        error_type = type(error).__name__

        # Network errors
        if any(
            keyword in error_message.lower()
            for keyword in ["connection", "timeout", "network", "dns", "ssl"]
        ):
            return AppError(
                error_message,
                ErrorCategory.NETWORK,
                ErrorSeverity.MEDIUM,
                context={"error_type": error_type},
            )

        # Authentication errors
        elif any(
            keyword in error_message.lower()
            for keyword in ["unauthorized", "authentication", "credentials", "login"]
        ):
            return AppError(
                error_message,
                ErrorCategory.AUTHENTICATION,
                ErrorSeverity.HIGH,
                context={"error_type": error_type},
            )

        # API errors
        elif any(
            keyword in error_message.lower()
            for keyword in ["api", "http", "request", "response", "status"]
        ):
            return AppError(
                error_message,
                ErrorCategory.API,
                ErrorSeverity.MEDIUM,
                context={"error_type": error_type},
            )

        # Validation errors
        elif any(
            keyword in error_message.lower()
            for keyword in ["validation", "invalid", "required", "format"]
        ):
            return AppError(
                error_message,
                ErrorCategory.VALIDATION,
                ErrorSeverity.LOW,
                context={"error_type": error_type},
            )

        # File system errors
        elif any(
            keyword in error_message.lower()
            for keyword in ["file", "directory", "permission", "access"]
        ):
            return AppError(
                error_message,
                ErrorCategory.FILESYSTEM,
                ErrorSeverity.MEDIUM,
                context={"error_type": error_type},
            )

        # Default to unknown
        else:
            return AppError(
                error_message,
                ErrorCategory.UNKNOWN,
                ErrorSeverity.MEDIUM,
                context={"error_type": error_type},
            )

    def _attempt_recovery(self, error: AppError) -> bool:
        """
        Attempt to recover from an error.

        Args:
            error: The error to recover from

        Returns:
            True if recovery successful
        """
        for strategy in self.recovery_strategies.get(error.category, []):
            try:
                if strategy(error):
                    logger.info(f"Recovery successful for {error.category.value} error")
                    return True
            except Exception as recovery_error:
                logger.error(f"Recovery strategy failed: {recovery_error}")

        return False

    @contextmanager
    def error_boundary(self, operation: str, context: Optional[Dict[str, Any]] = None):
        """
        Context manager for error boundaries.

        Args:
            operation: Operation description
            context: Additional context
        """
        try:
            with logger.create_context(operation=operation, **(context or {})):
                yield
        except Exception as e:
            app_error = self.handle_error(
                e, {"operation": operation, **(context or {})}
            )
            self._display_error_to_user(app_error)

    def retry_operation(
        self,
        operation: Callable,
        max_retries: Optional[int] = None,
        backoff_factor: float = 1.0,
        **kwargs,
    ) -> Any:
        """
        Retry an operation with exponential backoff.

        Args:
            operation: Operation to retry
            max_retries: Maximum number of retries
            backoff_factor: Backoff factor for delay
            **kwargs: Additional arguments for operation

        Returns:
            Operation result

        Raises:
            AppError: If all retries fail
        """
        retries = max_retries or self.max_retries
        last_error = None

        for attempt in range(retries + 1):
            try:
                return operation(**kwargs)
            except Exception as e:
                last_error = e
                if attempt < retries:
                    delay = backoff_factor * (2**attempt)
                    logger.warning(f"Operation failed, retrying in {delay}s: {e}")
                    import time

                    time.sleep(delay)
                else:
                    logger.error(f"Operation failed after {retries + 1} attempts: {e}")

        # All retries failed
        raise self.handle_error(last_error, {"retries": retries})

    def _display_error_to_user(self, error: AppError):
        """Display error to user in Streamlit interface."""
        try:
            if error.severity == ErrorSeverity.CRITICAL:
                st.error(f"🚨 Critical Error: {error.user_message}")
            elif error.severity == ErrorSeverity.HIGH:
                st.error(f"❌ Error: {error.user_message}")
            elif error.severity == ErrorSeverity.MEDIUM:
                st.warning(f"⚠️ Warning: {error.user_message}")
            else:
                st.info(f"ℹ️ {error.user_message}")

            # Show recovery suggestions
            if error.recovery_suggestions:
                with st.expander("💡 Suggestions"):
                    for suggestion in error.recovery_suggestions:
                        st.write(f"• {suggestion}")

            # Show detailed error in development/debug mode
            if st.session_state.get("debug_mode", False):
                with st.expander("🔧 Technical Details"):
                    st.code(error.message)
                    st.code(error.traceback)

        except Exception as display_error:
            # Fallback error display
            st.error("An error occurred while displaying the error message.")
            logger.error(f"Error display failed: {display_error}")

    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics."""
        return {
            "total_errors": sum(self.error_counts.values()),
            "error_counts": self.error_counts.copy(),
            "categories": list(self.error_handlers.keys()),
            "recovery_strategies": list(self.recovery_strategies.keys()),
        }

    def reset_error_counts(self):
        """Reset error count statistics."""
        self.error_counts.clear()


# Global error handler instance
error_handler = ErrorHandler()


def get_error_handler() -> ErrorHandler:
    """Get the global error handler instance."""
    return error_handler


def handle_errors(operation: str = None):
    """
    Decorator for comprehensive error handling.

    Args:
        operation: Operation description
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            op_name = operation or func.__name__
            with error_handler.error_boundary(op_name):
                return func(*args, **kwargs)

        return wrapper

    return decorator


# Convenience functions for common error types
def network_error(message: str, **context) -> AppError:
    """Create a network error."""
    return AppError(
        message,
        ErrorCategory.NETWORK,
        ErrorSeverity.MEDIUM,
        recovery_suggestions=[
            "Check your internet connection",
            "Try again in a few moments",
            "Contact support if the problem persists",
        ],
        context=context,
    )


def auth_error(message: str, **context) -> AppError:
    """Create an authentication error."""
    return AppError(
        message,
        ErrorCategory.AUTHENTICATION,
        ErrorSeverity.HIGH,
        recovery_suggestions=[
            "Verify your API credentials",
            "Check if your API key is still valid",
            "Re-authenticate if necessary",
        ],
        context=context,
    )


def validation_error(message: str, **context) -> AppError:
    """Create a validation error."""
    return AppError(
        message,
        ErrorCategory.VALIDATION,
        ErrorSeverity.LOW,
        recovery_suggestions=[
            "Review the input requirements",
            "Check data formats and constraints",
            "Ensure all required fields are filled",
        ],
        context=context,
    )


def api_error(message: str, status_code: Optional[int] = None, **context) -> AppError:
    """Create an API error."""
    severity = (
        ErrorSeverity.HIGH
        if status_code and status_code >= 500
        else ErrorSeverity.MEDIUM
    )
    return AppError(
        message,
        ErrorCategory.API,
        severity,
        recovery_suggestions=[
            "Try again in a few moments",
            "Check API service status",
            "Contact support if the problem persists",
        ],
        context={"status_code": status_code, **context},
    )
