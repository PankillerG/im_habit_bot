import typing

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

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
        InlineKeyboardButton('1', callback_data='1'),
        InlineKeyboardButton('2', callback_data='2'),
        InlineKeyboardButton('3', callback_data='3'),
    ],
    [
        InlineKeyboardButton('4', callback_data='4'),
        InlineKeyboardButton('5', callback_data='5'),
        InlineKeyboardButton('6', callback_data='6'),
    ],
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
