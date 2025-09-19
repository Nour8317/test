import logging
from enum import StrEnum

LOG_FORMAT_DEBUG = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

def configure_logging(level: LogLevel = LogLevel.INFO) -> None:
    logging.basicConfig(
        level=level.value,
        format=LOG_FORMAT_DEBUG if level == LogLevel.DEBUG else "%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.getLogger("some_noisy_library").setLevel(logging.WARNING) 