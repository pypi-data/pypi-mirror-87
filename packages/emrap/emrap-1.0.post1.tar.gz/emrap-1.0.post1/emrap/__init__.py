import logging
import colorlog
import sys
from logging import NullHandler

logging.TRACE = 1
logging.addLevelName(logging.TRACE, 'TRACE')
class TraceLogger(logging.Logger):
    def trace(self, *args, **kargs):
        return super(TraceLogger, self).log(
            logging.TRACE, *args, **kargs)


logging.setLoggerClass(TraceLogger)
logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


def setup_logger(verbosity=None):
    handler = colorlog.StreamHandler(sys.stderr)
    handler.setFormatter(
        colorlog.ColoredFormatter(
            '%(log_color)s[%(levelname)s] %(message)s',
            log_colors={
                'TRACE': 'blue',
                'DEBUG': 'purple',
                'INFO': 'bold_green',
                'WARNING': 'bold_yellow',
                'ERROR': 'bold_red',
                'CRITICAL': 'bold_white,bg_red'}))
    handler.setLevel(logging.TRACE)  # no filtering per-handler

    if verbosity is None:
        logger.setLevel(logging.WARNING)
    elif verbosity > 2:
        logger.setLevel(logging.TRACE)
    elif verbosity > 1:
        logger.setLevel(logging.DEBUG)
    elif verbosity > 0:
        logger.setLevel(logging.INFO)
    logger.addHandler(handler)


from .gmail import Gmail

__all__ = [
    'setup_logger',
    'Gmail'
]
