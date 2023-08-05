import contextlib
import logging
import sys


SHORT_FORMATTER = logging.Formatter(
    "[%(asctime)s:%(levelname)s:%(name)s:%(funcName)s]: "
    "%(message)s"
)

LONG_FORMATTER = logging.Formatter(
    "[%(asctime)s:%(levelname)s:%(name)s:%(funcName)s] "
    "{%(filename)s:%(lineno)s} %(message)s"
)


def configure_logging(
    *, with_line_no=False, level=logging.INFO, log_file=None, file_mode="w",
):

    logging.getLogger().setLevel(level)

    if log_file is None:
        log_handler = logging.StreamHandler(sys.stdout)
    else:
        log_handler = logging.FileHandler(log_file, mode=file_mode)

    formatter = LONG_FORMATTER if with_line_no else SHORT_FORMATTER
    log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(log_handler)


@contextlib.contextmanager
def push_log_level(level):
    logger = logging.getLogger()
    old_level = logger.level
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)
