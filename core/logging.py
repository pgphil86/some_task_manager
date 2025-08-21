import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .config import settings

LOG_DIR = Path(settings.log_dir)
LOG_FILE = LOG_DIR / "app.log"


def configure_logging() -> None:
    """
    Базовые настройки логирования для Task Manager API.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
    formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.info(
        "Настроки логирования.",
        extra={
            "log_level": settings.log_level,
            "log_dir": str(LOG_DIR),
        }
    )


logger = logging.getLogger(__name__)
