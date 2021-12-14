from datetime import datetime
from time import time
import logging
from logging.handlers import RotatingFileHandler
from typing import Callable, Any
from pprint import pprint

def log_to_console(func):
    def loger(*args, **kwargs):
        date = datetime.date(datetime.now())
        times = datetime.time(datetime.now())
        func_name = func.__name__
        started_at = time()
        result = func(*args, **kwargs)
        ended_at = time()
        elapsed = round(ended_at - started_at, 4)
        print()

        pprint(
            f"date: {date}\n"
              f"time: {times}\n"
              f"name: {func_name}\n"
              f"args: {args, kwargs}\n"
              f"result: {result}\n"
              f'функция работала {elapsed} секунд(ы)'
              )


        return result
    return loger


#

# from random import randrange
#
# import vk_api
# from vk_api.longpoll import VkLongPoll, VkEventType
# from VK_token import group_token
#
#
#
# vk = vk_api.VkApi(token=group_token)
# longpoll = VkLongPoll(vk)
#
#
# def write_msg(user_id, message):
#     vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})
#
#
# for event in longpoll.listen():
#     if event.type == VkEventType.MESSAGE_NEW:
#
#         if event.to_me:
#             request = event.text
#
#             if request == "привет":
#                 write_msg(event.user_id, f"Хай, {event.user_id}")
#             elif request == "пока":
#                 write_msg(event.user_id, "Пока((")
#             else:
#                 write_msg(event.user_id, "Не поняла вашего ответа...")