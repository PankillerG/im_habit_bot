import logging

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from lib import config
from lib.bot import jobs
from lib.bot.context_utils import ContextFields
from lib.bot.handlers import command_handlers, text_handlers, button_handlers


logger = logging.getLogger(__name__)


class BotRunner:
    def __init__(self, token, state_client):
        logger.info('BotRunner initialization')
        self.token = token
        self.state_client = state_client
    
    def initialize_data(self):
        logger.info('Data initialization')
        self.application.bot_data = {
            ContextFields.state_client: self.state_client
        }

    def add_handlers(self):
        logger.info('Handlers initialization')
        self.application.add_handler(CommandHandler('start', command_handlers.start))
        self.application.add_handler(CommandHandler('help', command_handlers.help))
        self.application.add_handler(CommandHandler('add', command_handlers.add))
        self.application.add_handler(CommandHandler('remove', command_handlers.remove))
        self.application.add_handler(CommandHandler('show', command_handlers.show))
        self.application.add_handler(CommandHandler('show_all', command_handlers.show_all))
        self.application.add_handler(CommandHandler('reset_all', command_handlers.reset_all))
        self.application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), text_handlers.text))
        self.application.add_handler(CallbackQueryHandler(button_handlers.button))

    def add_jobs(self):
        logger.info('Jobs initialization')
        self.application.job_queue.run_repeating(
            jobs.dump_state,
            interval=config.Jobs.DumpState.interval,
            first=config.Jobs.DumpState.first,
        )
        self.application.job_queue.run_repeating(
            jobs.reset_users_habits,
            interval=config.Jobs.ResetUsersHabits.interval,
            first=config.Jobs.ResetUsersHabits.first,
        )

    def run(self):
        self.application = Application.builder().token(self.token).build()
        self.initialize_data()
        self.add_handlers()
        self.add_jobs()
        logger.info('Bot running')
        self.application.run_polling()
 