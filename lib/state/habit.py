import logging
import uuid

from lib import time_utils
from lib.state import utils


logger = logging.getLogger(__name__)


class HabitState(utils.DefaultState):
    def __init__(
        self,
        name: str,
        goal_count: int,
        reset_freq: str,
        id: str = None,
        done_count: int=0,
        last_reset_timestamp: int = None,
    ):
        super().__init__()
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.done_count = done_count
        self.goal_count = goal_count
        self.reset_freq = reset_freq
        self.last_reset_timestamp = last_reset_timestamp or time_utils.get_current_timestamp()
        logger.info(f'HabitState has been initialized: {self.to_dict()}')

    def _need_to_reset(self):
        return not time_utils.is_equal(
            timestamp1=self.last_reset_timestamp,
            timestamp2=time_utils.get_current_timestamp(),
            datetime_type=self.reset_freq,
        )

    def _reset_done_count(self):
        self.done_count = 0
        self.last_reset_timestamp = time_utils.get_current_timestamp()

    def _is_actual(self):
        return self.done_count < self.goal_count

    async def increase_done_count(self, count: int=1):
        async with self._lock:
            logging.info(f'Increasing done_count by {count} for {self.name}')
            self.done_count += count

    async def reset_done_count(self, force: bool=True):
        async with self._lock:
            logging.info(f'Resetting done_count for {self.name} {force = }')
            if force or self._need_to_reset():
                self._reset_done_count()
                return True
            return False
    