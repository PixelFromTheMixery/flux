"""
Dedicated Logging Module

Made from code for working with observability tools

Variables:
    logHandler (StreamHandler): Tool for handling the shape of the log
    logger (getLogger): Actual logger for usage
"""

import logging
from pythonjsonlogger import json

logHandler = logging.StreamHandler()
logHandler.setFormatter(json.JsonFormatter("%(asctime)s [%(levelname)s] %(message)s"))

logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
