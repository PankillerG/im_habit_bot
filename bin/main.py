import logging

from lib import (
    config,
    logging_utils,
)
from lib.bot.bot import BotRunner
from lib.state.client import StateClient


logging_utils.configure_logging(
    filename=logging_utils.get_log_file_path(),
)
logger = logging.getLogger(__name__)


def main():
    logger.info('Starting')

    state_client = StateClient(config.STATE_FILE)
    BotRunner(
        token='',
        state_client=state_client,
    ).run()


if __name__ == '__main__':
    main()
