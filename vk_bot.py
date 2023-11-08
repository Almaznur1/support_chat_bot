import random
import logging
from dotenv import load_dotenv
from os import getenv
from telegram import Bot
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dialog_flow import detect_intent_texts
from tg_logger import TelegramLogsHandler


logger = logging.getLogger('vk_bot')


def send_dialog_flow_answer(event, vk_api, answer):
    vk_api.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.randint(1, 1000)
    )


if __name__ == '__main__':
    load_dotenv()
    logging_tg_bot_token = getenv('LOGGING_TG_BOT_TOKEN')
    tg_user_id = getenv('TG_USER_ID')
    project_id = getenv('PROJECT_ID')
    language_code = getenv('LANGUAGE_CODE')
    vk_api_key = getenv('VK_API_KEY')

    logger_bot = Bot(token=logging_tg_bot_token)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.addHandler(TelegramLogsHandler(logger_bot, tg_user_id))
    logger.info('Бот запущен!')

    try:
        vk_session = vk.VkApi(token=vk_api_key)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type != VkEventType.MESSAGE_NEW or not event.to_me:
                continue
            is_fallback, answer = detect_intent_texts(
                project_id=project_id,
                session_id=event.user_id,
                text=event.text,
                language_code=language_code
            )
            if not is_fallback:
                send_dialog_flow_answer(event, vk_api, answer)
    except Exception as error:
        logger.exception(error)
