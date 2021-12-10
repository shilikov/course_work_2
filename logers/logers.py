import logging
import datetime

def set_logger(name):
    """ задает параметры логгера"""

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)-23s '
                                  '%(levelname)-7s '
                                  '%(filename)-8s '
                                  '%(funcName)-14s '
                                  'line:%(lineno)-4s '
                                  '%(message)s')

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    file = logging.FileHandler(f'logs/{now}.log', encoding='utf-8')
    file.setLevel(logging.INFO)
    file.setFormatter(formatter)
    logger.addHandler(file)

    return logger



from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from VK_token import group_token



vk = vk_api.VkApi(token=group_token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")