import logging
from telegram import Update
from telegram.ext import (Updater, CommandHandler, CallbackContext,
                          MessageHandler, Filters)

from config import tg_bot_token, project_id, language_code
from dialog_flow import detect_intent_texts


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте'
    )


def send_dialog_flow_answer(update: Update, context: CallbackContext):
    text = detect_intent_texts(
        project_id=project_id,
        session_id=update.effective_chat.id,
        text=update.message.text,
        language_code=language_code
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )


def main():
    updater = Updater(token=tg_bot_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    echo_handler = MessageHandler(
        Filters.text & (~Filters.command),
        send_dialog_flow_answer
    )
    dispatcher.add_handler(echo_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
