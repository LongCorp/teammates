import logging
from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class LoggerHandlers:
    file_handler: Final[logging.FileHandler] = logging.FileHandler("./logs/service.log")
    console_handler: Final[logging.StreamHandler] = logging.StreamHandler()
