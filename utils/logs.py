# log.py
import logging
import sys
from logging import Logger


def create_logs() -> Logger:

    logging.getLogger().setLevel(logging.DEBUG)

    log = logging.getLogger(__name__)

    log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler(sys.stdout)

    console_handler.setLevel(logging.INFO)

    console_handler.setFormatter(log_format)

    log.addHandler(console_handler)

    return log
