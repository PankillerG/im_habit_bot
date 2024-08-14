import json
import logging
import os

from lib.state.state import State


logger = logging.getLogger(__name__)


class StateClient:
    def __init__(self, file_path: str):
        logger.info('StateClient initialization')
        self.file_path: str = file_path
        self.state: State = self.load_or_create()
        logger.info('StateClient has been initialized')

    def load(self):
        logger.info(f'Loading state from the file "{self.file_path}"')
        with open(self.file_path, 'r') as state_file:
            return State.from_dict(json.load(state_file))

    def load_or_create(self):
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            logger.info(f'Creating empty state')
            return State()
        return self.load()
    
    def dump(self):
        logger.info(f'Dumping state to "{self.file_path}"')
        with open(self.file_path, 'w') as state_file:
            json.dump(self.state.to_dict(), state_file)
