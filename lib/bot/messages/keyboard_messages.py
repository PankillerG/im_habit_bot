import itertools
import typing

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from lib import config
from lib.state.habit import HabitState


WAITING_FOR_HABIT_RESET_FREQ = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('Day', callback_data='day'),
        InlineKeyboardButton('Week', callback_data='week'),
        InlineKeyboardButton('Month', callback_data='month'),
    ],
])

WAITING_FOR_HABIT_GOAL_COUNT = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(f'{number}', callback_data=f'{number}')
        for number in row_numbers
    ]
    for row_numbers in itertools.batched(
        range(1, config.AVAILABLE_HABITS_GOALS_COUNT + 1),
        config.HABITS_GOALS_COUNT_PER_KEYBOARD_ROW,
    )
])


def get_show_habits(habits: typing.List[HabitState]):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=f'{habit.name} | {habit.done_count}/{habit.goal_count} per {habit.reset_freq}',
                callback_data=habit.id,
            )
        ]
        for habit in habits
    ])
