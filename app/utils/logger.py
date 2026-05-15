# region Docs
"""
Dedicated Logging Module

Made from code for working with observability tools

Variables:
    logHandler (StreamHandler): Tool for handling the shape of the log
    logger (getLogger): Actual logger for usage
"""
# endregion

import logging

logger = logging.getLogger("flux")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s:%(message)s")
    )
    logger.addHandler(h)
    logger.setLevel(logging.INFO)
    logger.propagate = False
