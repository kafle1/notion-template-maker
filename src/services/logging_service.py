"""
Logging service for the Notion Template Maker application.
Provides comprehensive logging, error tracking, and monitoring capabilities.
"""

import logging
import logging.handlers
import json
import sys
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import traceback
import threading
from queue import Queue
import os


class LogContext:
    """Context manager for adding context to log messages."""

    def __init__(self, logger: "AppLogger", **context):
        self.logger = logger
        self.context = context
        self.old_context = {}

    def __enter__(self):
        # Save old context
        for key in self.context:
            if hasattr(self.logger, f"_context_{key}"):
                self.old_context[key] = getattr(self.logger, f"_context_{key}")

        # Set new context
        for key, value in self.context.items():
            setattr(self.logger, f"_context_{key}", value)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore old context
        for key, value in self.old_context.items():
            setattr(self.logger, f"_context_{key}", value)
        else:
            # Clear context if no old value
            for key in self.context:
                if hasattr(self.logger, f"_context_{key}"):
                    delattr(self.logger, f"_context_{key}")


class AppLogger:
    """Comprehensive logging service for the application."""

    # Log levels
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __init__(
        self, name: str = "notion-template-maker", log_level: int = logging.INFO
    ):
        """
        Initialize the application logger.

        Args:
            name: Logger name
            log_level: Logging level
        """
        self.name = name
        self.log_level = log_level
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()

        # Create logs directory
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)

        # Setup handlers
        self._setup_handlers()

        # Context attributes
        self._context_user_id = None
        self._context_session_id = None
        self._context_request_id = None
        self._context_component = None

        # Error tracking
        self.error_queue = Queue()
        self.error_handler_thread = threading.Thread(
            target=self._process_errors, daemon=True
        )
        self.error_handler_thread.start()

    def _setup_handlers(self):
        """Setup logging handlers."""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler for all logs
        file_handler = logging.handlers.RotatingFileHandler(
            self.logs_dir / "app.log", maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Error file handler
        error_handler = logging.handlers.RotatingFileHandler(
            self.logs_dir / "error.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        self.logger.addHandler(error_handler)

        # JSON handler for structured logging
        json_handler = logging.handlers.RotatingFileHandler(
            self.logs_dir / "app.json", maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
        )
        json_handler.setLevel(logging.INFO)
        json_formatter = JsonFormatter()
        json_handler.setFormatter(json_formatter)
        self.logger.addHandler(json_handler)

    def _get_context_dict(self) -> Dict[str, Any]:
        """Get current logging context."""
        context = {}
        if self._context_user_id:
            context["user_id"] = self._context_user_id
        if self._context_session_id:
            context["session_id"] = self._context_session_id
        if self._context_request_id:
            context["request_id"] = self._context_request_id
        if self._context_component:
            context["component"] = self._context_component
        return context

    def _log_with_context(self, level: int, message: str, *args, **kwargs):
        """Log message with context."""
        context = self._get_context_dict()
        if context:
            message = f"{message} | Context: {context}"

        extra = kwargs.get("extra", {})
        extra.update(context)
        kwargs["extra"] = extra

        self.logger.log(level, message, *args, **kwargs)

    def debug(self, message: str, *args, **kwargs):
        """Log debug message."""
        self._log_with_context(self.DEBUG, message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Log info message."""
        self._log_with_context(self.INFO, message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """Log warning message."""
        self._log_with_context(self.WARNING, message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """Log error message."""
        self._log_with_context(self.ERROR, message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """Log critical message."""
        self._log_with_context(self.CRITICAL, message, *args, **kwargs)

    def exception(self, message: str, *args, **kwargs):
        """Log exception with traceback."""
        if "exc_info" not in kwargs:
            kwargs["exc_info"] = True
        self._log_with_context(self.ERROR, message, *args, **kwargs)

    def log_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        user_message: Optional[str] = None,
    ):
        """
        Log an error with comprehensive information.

        Args:
            error: The exception that occurred
            context: Additional context information
            user_message: User-friendly message
        """
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat(),
            "context": context or {},
            "user_message": user_message,
        }

        # Add to error queue for processing
        self.error_queue.put(error_info)

        # Log immediately
        self.error(f"Error occurred: {error_info['error_message']}", extra=error_info)

    def log_api_call(
        self,
        service: str,
        method: str,
        url: str,
        status_code: Optional[int] = None,
        duration: Optional[float] = None,
        error: Optional[str] = None,
    ):
        """
        Log API call information.

        Args:
            service: Service name (e.g., 'openrouter', 'notion')
            method: HTTP method
            url: Request URL
            status_code: HTTP status code
            duration: Request duration in seconds
            error: Error message if any
        """
        log_data = {
            "service": service,
            "method": method,
            "url": url,
            "status_code": status_code,
            "duration": duration,
            "error": error,
            "timestamp": datetime.now().isoformat(),
        }

        level = self.INFO if status_code and 200 <= status_code < 300 else self.WARNING
        self.logger.log(level, f"API Call: {service} {method} {url}", extra=log_data)

    def log_user_action(
        self,
        action: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        **kwargs,
    ):
        """
        Log user action for analytics.

        Args:
            action: Action performed
            user_id: User identifier
            session_id: Session identifier
            **kwargs: Additional action data
        """
        action_data = {
            "action": action,
            "user_id": user_id or self._context_user_id,
            "session_id": session_id or self._context_session_id,
            "timestamp": datetime.now().isoformat(),
            **kwargs,
        }

        self.info(f"User Action: {action}", extra=action_data)

    def log_performance(
        self, operation: str, duration: float, metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Log performance metrics.

        Args:
            operation: Operation name
            duration: Duration in seconds
            metadata: Additional metadata
        """
        perf_data = {
            "operation": operation,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        }

        level = self.WARNING if duration > 10 else self.INFO  # Warn if > 10 seconds
        self.logger.log(
            level, f"Performance: {operation} took {duration:.2f}s", extra=perf_data
        )

    def create_context(self, **context) -> LogContext:
        """
        Create a logging context manager.

        Args:
            **context: Context key-value pairs

        Returns:
            LogContext manager
        """
        return LogContext(self, **context)

    def _process_errors(self):
        """Process errors from the error queue."""
        while True:
            try:
                error_info = self.error_queue.get(timeout=1)
                self._handle_error(error_info)
                self.error_queue.task_done()
            except:
                continue  # Continue processing even if error handling fails

    def _handle_error(self, error_info: Dict[str, Any]):
        """Handle error information."""
        # Here you could send to error tracking service like Sentry
        # For now, just ensure it's logged with full context
        pass

    def get_log_files(self) -> List[Path]:
        """Get list of log files."""
        return list(self.logs_dir.glob("*.log")) + list(self.logs_dir.glob("*.json"))

    def cleanup_old_logs(self, days: int = 30):
        """
        Clean up log files older than specified days.

        Args:
            days: Number of days to keep logs
        """
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)

        for log_file in self.get_log_files():
            if log_file.stat().st_mtime < cutoff:
                log_file.unlink()

    def __str__(self) -> str:
        """String representation."""
        return f"AppLogger(name={self.name}, level={self.log_level})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"AppLogger(name={self.name}, level={self.log_level}, handlers={len(self.logger.handlers)})"


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record):
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "__dict__"):
            for key, value in record.__dict__.items():
                if key not in [
                    "name",
                    "msg",
                    "args",
                    "levelname",
                    "levelno",
                    "pathname",
                    "filename",
                    "module",
                    "exc_info",
                    "exc_text",
                    "stack_info",
                    "lineno",
                    "funcName",
                    "created",
                    "msecs",
                    "relativeCreated",
                    "thread",
                    "threadName",
                    "processName",
                    "process",
                    "message",
                ]:
                    log_entry[key] = value

        return json.dumps(log_entry, default=str)


# Global logger instance
logger = AppLogger()


def get_logger(name: str = None) -> AppLogger:
    """
    Get logger instance.

    Args:
        name: Logger name (optional)

    Returns:
        AppLogger instance
    """
    if name:
        return AppLogger(name)
    return logger


def log_function_call(func_name: str = None):
    """
    Decorator to log function calls.

    Args:
        func_name: Function name override
    """

    def decorator(func):
        name = func_name or func.__name__

        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            try:
                logger.debug(f"Calling function: {name}")
                result = func(*args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds()
                logger.debug(f"Function {name} completed in {duration:.2f}s")
                return result
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                logger.log_error(e, {"function": name, "duration": duration})
                raise

        return wrapper

    return decorator


class LoggingService:
    """Service wrapper for AppLogger to provide a simple interface."""

    def __init__(self):
        self.logger = AppLogger()

    def log_info(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log an info message."""
        self.logger.info(message, context)

    def log_error(
        self,
        message: str,
        error: Optional[Exception] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Log an error message."""
        self.logger.error(message, error, context)

    def log_warning(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log a warning message."""
        self.logger.warning(message, context)

    def log_debug(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log a debug message."""
        self.logger.debug(message, context)
