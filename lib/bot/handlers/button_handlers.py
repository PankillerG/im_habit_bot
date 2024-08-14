import logging

from telegram import Update
from telegram.ext import ContextTypes

from lib.bot.context_utils import ContextFields
from lib.bot.messages import (
    keyboard_messages,
    text_messages,
)
from lib.state.client import StateClient
from lib.state.user import ConvStatuses


logger = logging.getLogger(__name__)


async def waiting_for_habit_reset_freq(state_client: StateClient, user_id, query):
    reset_freq = query.data
    state_client.state.users_states[user_id].conv_data.habit_reset_freq = reset_freq
    state_client.state.users_states[user_id].conv_status = ConvStatuses.waiting_for_habit_goal_count

    habit_name = state_client.state.users_states[user_id].conv_data.habit_name
    await query.edit_message_text(
        text=text_messages.WAITING_FOR_HABIT_GOAL_COUNT.format(habit_name=habit_name, habit_reset_freq=reset_freq),
        reply_markup=keyboard_messages.WAITING_FOR_HABIT_GOAL_COUNT,
    )


async def waiting_for_habit_goal_count(state_client: StateClient, user_id, query):
    state_client.state.users_states[user_id].conv_data.habit_goal_count = query.data
    state_client.state.users_states[user_id].conv_status = ConvStatuses.default

    conv_data = state_client.state.users_states[user_id].conv_data
    await state_client.state.users_states[user_id].add_habit(
        name=conv_data.habit_name,
        goal_count=int(conv_data.habit_goal_count),
        reset_freq=conv_data.habit_reset_freq,
    )
    await query.edit_message_text(text_messages.HABIT_HAS_BEEN_ADDED.format(
        habit_name=conv_data.habit_name,
        habit_reset_freq=conv_data.habit_reset_freq,
        habit_goal_count=conv_data.habit_goal_count,
    ))


async def remove_habits(state_client: StateClient, user_id, query):
    habit_id = query.data
    await state_client.state.users_states[user_id].remove_habit(habit_id)

    habits = await state_client.state.users_states[user_id].get_habits()
    await query.edit_message_text(
        text=text_messages.get_remove_habits(not habits),
        reply_markup=keyboard_messages.get_show_habits(habits),
    )


async def show_habits(state_client: StateClient, user_id, query):
    habit_id = query.data
    await state_client.state.users_states[user_id].habits[habit_id].increase_done_count()
    habits = await state_client.state.users_states[user_id].get_habits()
    await query.edit_message_text(
        text=text_messages.get_show_habits(not habits),
        reply_markup=keyboard_messages.get_show_habits(habits),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    state_client: StateClient = context.bot_data[ContextFields.state_client]
    user_id = query.from_user.id
    conv_status = state_client.state.users_states[user_id].conv_status
    logger.info(f'{user_id = }; click on button; {conv_status = }')

    if conv_status == ConvStatuses.waiting_for_habit_reset_freq:
        await waiting_for_habit_reset_freq(state_client, user_id, query)

    elif conv_status == ConvStatuses.waiting_for_habit_goal_count:
        await waiting_for_habit_goal_count(state_client, user_id, query)
    
    elif conv_status == ConvStatuses.remove_habits:
        await remove_habits(state_client, user_id, query)

    elif conv_status == ConvStatuses.show_habits:
        await show_habits(state_client, user_id, query)