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


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state_client: StateClient = context.bot_data[ContextFields.state_client]
    user_id = update.message.from_user.id
    conv_status = state_client.state.users_states[user_id].conv_status

    if conv_status == ConvStatuses.waiting_for_habit_name:
        habit_name = update.message.text
        logger.info(f'{user_id = }; text = "{habit_name}"')
        state_client.state.users_states[user_id].conv_data.habit_name = habit_name
        state_client.state.users_states[user_id].conv_status = ConvStatuses.waiting_for_habit_reset_freq
        await update.message.reply_text(
            text=text_messages.WAITING_FOR_HABIT_RESET_FREQ.format(habit_name=habit_name),
            reply_markup=keyboard_messages.WAITING_FOR_HABIT_RESET_FREQ,
        )
