# -*- coding: utf-8 -*-
"""pytest configuration"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."


import logging
import logging.config

from common.application import log_configuration

logging.config.dictConfig(log_configuration())
