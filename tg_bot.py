import logging
from dotenv import load_dotenv
from os import getenv
from telegram import Bot, Update
from telegram.ext import (Updater, CommandHandler, CallbackContext,
                          MessageHandler, Filters)

from dialog_flow import detect_intent_texts
from tg_logger import TelegramLogsHandler


logger = logging.getLogger('tg_bot')


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте'
    )


def send_dialog_flow_answer(update: Update, context: CallbackContext,
                            project_id, language_code):
    try:
        is_fallback, text = detect_intent_texts(
            project_id=project_id,
            session_id=update.effective_chat.id,
            text=update.message.text,
            language_code=language_code
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text
        )
    except Exception as error:
        logger.exception(error)


if __name__ == '__main__':
    load_dotenv()
    tg_bot_token = getenv('TG_BOT_TOKEN')
    logging_tg_bot_token = getenv('LOGGING_TG_BOT_TOKEN')
    tg_user_id = getenv('TG_USER_ID')
    project_id = getenv('PROJECT_ID')
    language_code = getenv('LANGUAGE_CODE')

    updater = Updater(token=tg_bot_token)
    dispatcher = updater.dispatcher
    logger_bot = Bot(token=logging_tg_bot_token)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.addHandler(TelegramLogsHandler(logger_bot, tg_user_id))

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    dialog_flow_handler = MessageHandler(
        Filters.text & (~Filters.command),
        lambda update, context: send_dialog_flow_answer(
            update, context, project_id, language_code
        )
    )
    dispatcher.add_handler(dialog_flow_handler)

    logger.info('Бот запущен!')
    updater.start_polling()
