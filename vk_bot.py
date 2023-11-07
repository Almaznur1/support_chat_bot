import random
import logging
from dotenv import load_dotenv
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


def main():
    logger_bot = Bot(token=config.logging_tg_bot_token)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.addHandler(TelegramLogsHandler(logger_bot, config.tg_user_id))
    logger.info('Бот запущен!')

    try:
        vk_session = vk.VkApi(token=config.vk_api_key)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                is_fallback, answer = detect_intent_texts(
                    project_id=config.project_id,
                    session_id=event.user_id,
                    text=event.text,
                    language_code=config.language_code
                )
                if not is_fallback:
                    send_dialog_flow_answer(event, vk_api, answer)
    except Exception as error:
        logger.exception(error)


if __name__ == '__main__':
    load_dotenv()
    import config
    main()
