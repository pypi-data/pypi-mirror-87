import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from telegram_group_bot.config import Config

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, config: Config):
        self.config = config
        self.updater = Updater(config.token, workers=10)

    def start(self):
        self.updater.start_polling(timeout=30, clean=True)
        self.updater.dispatcher.add_handler(CommandHandler("ping", self._ping_cmd_handler))

        self.updater.dispatcher.add_handler(MessageHandler(Filters.status_update, self._status_update_handler))
        logger.info("bot started")
        self.updater.idle()

    def stop(self):
        self.updater.stop()

    def _ping_cmd_handler(self, update: Update, context: CallbackContext):
        context.bot.send_message(update.message.chat_id, "pong")

    def _status_update_handler(self, update: Update, context: CallbackContext):
        if update.message.new_chat_members:
            for new_member in update.message.new_chat_members:
                if new_member.is_bot:
                    continue
                message = self.config.welcome_message.replace("${name}", new_member.name)
                context.bot.send_message(update.message.chat_id, message)
