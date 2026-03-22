"""
Logging Configuration

This module sets up structured logging for the application.
"""
import logging
import sys
from pathlib import Path

from app.core.config import settings


def setup_logging() -> None:
    """
    Configure application logging.

    Sets up:
    - Log format with timestamps
    - Console handler for development
    - File handler for production (optional)
    - Log level based on environment
    """
    log_level = logging.INFO

    # Create formatters
    console_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level)

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)

    # Reduce noise from third-party libraries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    logging.info("Logging configured successfully")
