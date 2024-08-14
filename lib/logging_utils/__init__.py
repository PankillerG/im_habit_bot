import logging
import os

from lib import (
    config,
    time_utils,
)


def configure_logging(filename):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    logging.basicConfig(
        filename=filename,
        format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        level=logging.INFO,
    )

def get_log_file_path():
    return os.path.join(config.LOGS_DIR, f'{time_utils.get_current_timestamp()}.txt')
