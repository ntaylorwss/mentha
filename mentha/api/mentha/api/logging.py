import logging
from typing import Any

try:
    import gunicorn.glogging

except ImportError:
    gunicorn = None

CORN_LOGGERS = ["gunicorn.error", "gunicorn.access", "uvicorn.error", "uvicorn.access"]

# clear gunicorn and uvicorn loggers
for logger_name in CORN_LOGGERS:
    logger = logging.getLogger(logger_name)
    logger.handlers.clear()
    logger.level = logging.NOTSET
    logger.propagate = False

# configure root logger
root_logger = logging.getLogger()
root_logger.handlers.clear()
logging.basicConfig(
    format="[%(name)s] %(levelname)s --- %(asctime)s --- %(message)s",
    level=logging.INFO,
)

# create gunicorn custom logger class
if gunicorn is not None:

    class GunicornLogger(gunicorn.glogging.Logger):
        def setup(self, cfg: Any) -> None:
            super().setup(cfg)
            self.access_log.propagate = False
            self.error_log.propagate = False
            logger = logging.getLogger("gunicorn.error")
            logger.handlers.clear()
