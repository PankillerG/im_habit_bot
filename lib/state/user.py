import logging
import typing

from lib.state import utils
from lib.state.habit import HabitState


logger = logging.getLogger(__name__)


class ConvStatuses:
    default = 'default'
    waiting_for_habit_name = 'waiting_for_habit_name'
    waiting_for_habit_reset_freq = 'waiting_for_habit_reset_freq'
    waiting_for_habit_goal_count = 'waiting_for_habit_goal_count'
    show_habits = 'show_habits'
    remove_habits = 'remove_habits'


class ConvData(utils.DefaultState):
    def __init__(self, last_replied_message_id: int = 0):
        super().__init__()
        self.habit_name: str = ''
        self.habit_reset_freq: int = 0
        self.habit_goal_count: int = 0
        self.last_replied_message_id: int = last_replied_message_id
        logger.info(f'ConvData has been initialized: {self.to_dict()}')


class UserState(utils.DefaultState):
    def __init__(
        self,
        habits: typing.Dict[str, HabitState]=None,
        conv_status: str = ConvStatuses.default,
        conv_data: ConvData = None,
    ):
        super().__init__()
        self.habits = habits or dict()
        self.conv_status: str = conv_status
        self.conv_data: ConvData = conv_data or ConvData()
        logger.info(f'UserState has been initialized: {self.to_dict()}')
    
    async def add_habit(self, name: str, goal_count: int, reset_freq: str):
        async with self._lock:
            habit = HabitState(
                name=name,
                goal_count=goal_count,
                reset_freq=reset_freq,
            )
            self.habits[habit.id] = habit
            logger.info(f'New habit has been added: {habit}')
    
    async def remove_habit(self, id: str):
        async with (
            self._lock,
            self.habits[id]._lock,
        ):
            logger.info(f'Removing habit with id {id}')
            self.habits.pop(id, None)
    
    async def remove_all_habits(self):
        async with self._lock:
            logger.info(f'Removing all habits')
            for habit_id in self.habits:
                async with self.habits[habit_id]._lock:
                    logger.info(f'Removing habit with id {habit_id}')
                    self.habits.pop(habit_id, None)

    async def get_habits(self, actual: bool=True, sort: bool=True):
        logger.info(f'Getting habits {actual = }')
        habits = self.habits.values()
        if actual:
            habits = list(filter(lambda habit: habit._is_actual(), habits))
        if sort:
            habits = sorted(habits, key=lambda habit: habit._get_sort_key())
        return habits

    async def reset_habits(self, force: bool=False):
        async with self._lock:
            logger.info(f'Resetting habits {force = }')
            status = False
            for habit_id in self.habits:
                status |= await self.habits[habit_id].reset_done_count(force)
            return status
