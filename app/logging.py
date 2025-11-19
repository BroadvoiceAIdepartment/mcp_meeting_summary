import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Optional
import os


def _is_filesystem_writable(path: Path) -> bool:
    """Check if the filesystem at the given path is writable.
    
    Returns True if we can create/write files, False otherwise.
    """
    try:
        # Try to create a test file in the directory
        test_file = path / ".write_test"
        if path.exists():
            test_file.touch()
            test_file.unlink()
            return True
        else:
            # Try to create the directory
            path.mkdir(parents=True, exist_ok=True)
            test_file.touch()
            test_file.unlink()
            return True
    except (OSError, PermissionError):
        return False


def configure_logging(log_dir: Optional[str] = None, level: str = "INFO") -> None:
    """Configure root logging with both console and daily rotating file handlers.

    - Logs are written to <repo_root>/logs/app.log by default (if filesystem is writable).
    - File logs rotate daily and keep 7 days of history.
    - Uvicorn access/error and Starlette/FastAPI logs are also captured to the file.
    - In read-only filesystem environments (e.g., FastMCP Cloud), only console logging is used.
    """
    # Determine logs directory relative to repository root
    app_dir = Path(__file__).resolve().parent
    repo_root = app_dir.parent
    logs_path = Path(log_dir) if log_dir else repo_root / "app/utils/logs"

    # Basic formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler (always available)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # Try to create file handler only if filesystem is writable
    file_handler = None
    if _is_filesystem_writable(logs_path):
        try:
            logfile = logs_path / "app.log"
            file_handler = TimedRotatingFileHandler(
                filename=str(logfile), when="D", interval=1, backupCount=7, encoding="utf-8"
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
        except (OSError, PermissionError) as e:
            # If file handler creation fails, log to console only
            logging.warning(f"Could not create file handler (filesystem may be read-only): {e}")
            file_handler = None

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Avoid adding duplicate handlers if configure_logging is called multiple times
    if file_handler and not any(isinstance(h, TimedRotatingFileHandler) for h in root_logger.handlers):
        root_logger.addHandler(file_handler)
    if not any(isinstance(h, logging.StreamHandler) and not isinstance(h, TimedRotatingFileHandler) for h in root_logger.handlers):
        root_logger.addHandler(console_handler)

    # Also attach file handler to Uvicorn and Starlette/FastAPI loggers so their output goes to file
    # (only if file handler was successfully created)
    if file_handler:
        for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi", "starlette"):
            logger = logging.getLogger(logger_name)
            logger.setLevel(level)
            # Only add the file handler if this logger doesn't already have a TimedRotatingFileHandler
            if not any(isinstance(h, TimedRotatingFileHandler) for h in logger.handlers):
                logger.addHandler(file_handler)
        # Keep their existing console handlers; no need to modify propagation here
