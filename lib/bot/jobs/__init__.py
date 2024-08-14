import logging

from telegram.ext import ContextTypes

from lib.bot.context_utils import ContextFields
from lib.bot.messages import (
    keyboard_messages,
    text_messages,
)
from lib.state.client import StateClient
from lib.state.user import ConvStatuses


logger = logging.getLogger(__name__)


async def dump_state(context: ContextTypes.DEFAULT_TYPE):
    state_client: StateClient = context.bot_data[ContextFields.state_client]
    state_client.dump()


async def reset_users_habits(context: ContextTypes.DEFAULT_TYPE):
    state_client: StateClient = context.bot_data[ContextFields.state_client]

    for user_id in state_client.state.users_states:
        if state_client.state.users_states[user_id].conv_status != ConvStatuses.show_habits:
            continue

        reset_status = await state_client.state.users_states[user_id].reset_habits()
        if not reset_status:
            continue

        habits = await state_client.state.users_states[user_id].get_habits()
        message_id = state_client.state.users_states[user_id].conv_data.last_replied_message_id
        await context.bot.edit_message_text(
            text=text_messages.get_show_habits(not habits),
            chat_id=user_id,
            message_id=message_id,
            reply_markup=keyboard_messages.get_show_habits(habits),
        )
