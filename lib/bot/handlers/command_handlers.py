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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state_client: StateClient = context.bot_data[ContextFields.state_client]
    user_id = update.message.from_user.id
    state_client.state.users_states[user_id].conv_status = ConvStatuses.default
    logger.info(f'{user_id = }; command = "start"')
    await update.message.reply_text(text_messages.START)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state_client: StateClient = context.bot_data[ContextFields.state_client]
    user_id = update.message.from_user.id
    state_client.state.users_states[user_id].conv_status = ConvStatuses.default
    logger.info(f'{user_id = }; command = "help"')
    await update.message.reply_text(text_messages.HELP)


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state_client: StateClient = context.bot_data[ContextFields.state_client]
    user_id = update.message.from_user.id
    state_client.state.users_states[user_id].conv_status = ConvStatuses.waiting_for_habit_name
    logger.info(f'{user_id = }; command = "add"')
    await update.message.reply_text(text_messages.WAITING_FOR_HABIT_NAME)


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state_client: StateClient = context.bot_data[ContextFields.state_client]
    user_id = update.message.from_user.id
    state_client.state.users_states[user_id].conv_status = ConvStatuses.remove_habits
    logger.info(f'{user_id = }; command = "remove"')

    habits = await state_client.state.users_states[user_id].get_habits()
    await update.message.reply_text(
        text=text_messages.get_remove_habits(not habits),
        reply_markup=keyboard_messages.get_show_habits(habits),
    )

async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state_client: StateClient = context.bot_data[ContextFields.state_client]
    user_id = update.message.from_user.id
    state_client.state.users_states[user_id].conv_status = ConvStatuses.show_habits
    logger.info(f'{user_id = }; command = "show"')

    habits = await state_client.state.users_states[user_id].get_habits()
    replied_message = await update.message.reply_text(
        text=text_messages.get_show_habits(not habits),
        reply_markup=keyboard_messages.get_show_habits(habits),
    )
    state_client.state.users_states[user_id].conv_data.last_replied_message_id = replied_message.message_id
    

async def show_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state_client: StateClient = context.bot_data[ContextFields.state_client]
    user_id = update.message.from_user.id
    state_client.state.users_states[user_id].conv_status = ConvStatuses.default
    logger.info(f'{user_id = }; command = "show_all"')

    habits = await state_client.state.users_states[user_id].get_habits(actual=False)
    await update.message.reply_text(
        text=text_messages.get_show_habits(not habits),
        reply_markup=keyboard_messages.get_show_habits(habits),
    )


async def reset_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state_client: StateClient = context.bot_data[ContextFields.state_client]
    user_id = update.message.from_user.id
    state_client.state.users_states[user_id].conv_status = ConvStatuses.default
    logger.info(f'{user_id = }; command = "reset_all"')

    await state_client.state.users_states[user_id].remove_all_habits()
    await update.message.reply_text(text_messages.RESET_ALL)
