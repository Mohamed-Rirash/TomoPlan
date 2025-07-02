from loguru import logger
import sys

logger.remove()
logger.add(
    "./app.json",
    level="ERROR",
    retention="1 day",
    rotation="1 GB",
)
logger.add(sys.stderr, level="INFO")
