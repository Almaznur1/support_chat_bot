import logging
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import (Updater, CommandHandler, CallbackContext,
                          MessageHandler, Filters)

from dialog_flow import detect_intent_texts


logger = logging.getLogger('tg_bot')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        log_entry = log_entry[:4096]
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте'
    )


def send_dialog_flow_answer(update: Update, context: CallbackContext):
    try:
        is_fallback, text = detect_intent_texts(
            project_id=config.project_id,
            session_id=update.effective_chat.id,
            text=update.message.text,
            language_code=config.language_code
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text
        )
    except Exception as error:
        logger.exception(error)


def main():
    load_dotenv()

    updater = Updater(token=config.tg_bot_token)
    dispatcher = updater.dispatcher
    logger_bot = Bot(token=config.logging_tg_bot_token)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.addHandler(TelegramLogsHandler(logger_bot, config.tg_user_id))

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dialog_flow_handler = MessageHandler(
        Filters.text & (~Filters.command),
        send_dialog_flow_answer
    )
    dispatcher.add_handler(dialog_flow_handler)

    logger.info('Бот запущен!')
    updater.start_polling()


if __name__ == '__main__':
    load_dotenv()
    import config
    main()
