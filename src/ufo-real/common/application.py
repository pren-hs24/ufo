# -*- coding: utf-8 -*-
"""Common application module"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from typing import Any
import time
import sys


def log_configuration() -> dict[str, Any]:
    """Return the logging configuration."""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": (
                    "%(asctime)s " + time.strftime("%Z") + " %(levelname)-7s "
                    "%(filename)-24s:%(lineno)3s:%(funcName)-22s: %(message)s"
                )
            }
        },
        "handlers": {
            "stdout": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
                "stream": sys.stdout,
            },
            "stderr": {
                "level": "ERROR",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
                "stream": sys.stderr,
            },
        },
        "loggers": {"asyncio": {"level": "INFO"}},
        "root": {"handlers": ["stdout"], "level": "DEBUG"},
    }
