import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from config import vk_api_key
from dialog_flow import detect_intent_texts
from config import project_id, language_code


def send_dialog_flow_answer(event, vk_api, answer):
    vk_api.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.randint(1, 1000)
    )


def main():
    vk_session = vk.VkApi(token=vk_api_key)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            is_fallback, answer = detect_intent_texts(
                project_id=project_id,
                session_id=event.user_id,
                text=event.text,
                language_code=language_code
            )
            if not is_fallback:
                send_dialog_flow_answer(event, vk_api, answer)


if __name__ == '__main__':
    main()
