import collections
import logging
import typing

from lib.state import utils
from lib.state.user import UserState


logger = logging.getLogger(__name__)


class State(utils.DefaultState):
    def __init__(
        self,
        users_states: typing.Dict[int, UserState]=None,
    ):
        super().__init__()
        self.users_states = collections.defaultdict(
            UserState,
            users_states or {},
        )
        logger.info('State has been initialized')
    
    async def reset_users_habits(self, force: bool=False):
        logger.info(f'Resetting users habits {force = }')
        async with self._lock:
            for user_id in self.users_states:
                await self.users_states[user_id].reset_habits(force)
