from loguru import logger


logger.add('app/log/debug.txt', level="DEBUG", enqueue=True,
           colorize=True, format="{time} {level} {message}")
