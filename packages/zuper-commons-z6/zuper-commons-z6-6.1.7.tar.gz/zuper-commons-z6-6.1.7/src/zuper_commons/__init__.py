__version__ = "6.1.7"

import logging

logging.basicConfig()
logger = logging.getLogger("commons")
logger.setLevel(logging.DEBUG)

logger.debug(f"version: {__version__} *")
