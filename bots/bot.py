from collections import defaultdict

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from data_search.data_search import Users, Photo, Client
from data_base.db import engine, Session, User

from data_base.db_func import (write_msg, register_user,
                               add_user, add_to_black_list,
                               check_db_user, check_db_black,
                               check_db_favorites, check_db_master,
                               delete_db_blacklist, delete_db_favorites,
                               check_db_searcht)
from VK_token import (group_token, group_id,
                      user_token, VK_api_V)
from logers.logers import log
from pprint import pprint
import requests
from datetime import date
from bots.bot_message import (post1, post2, post3, hello_post,
                              bot_menu, info_post, post4, post5,
                              start_post, post6, ation1_post, ation2_post)
import threading
from requests import request
from threading import Thread
from bot_keybords.keyboard_bot import (keyboard3, keyboard2, send_keyboard)
from user_data.user_data import Self_user
# from libs import utils

# Для работы с вк_апи
vk = vk_api.VkApi(token=group_token)
longpoll = VkLongPoll(vk)
# Для работы с БД
session = Session()
connection = engine.connect()

global_result = {}
global_user_configs = defaultdict(dict)


class Bott:
    def __init__(self):
        self.user = User
        self.vk = vk_api.VkApi(token=group_token)
        self.vk_ = self.vk.get_api()
        self.longpoll = VkLongPoll(self.vk)
        self.session = requests.Session()
        self.connection = engine.connect()
        self._user = None
        self.search_sex = 0
        self.search_age_from = ''
        self.search_age_to = ''
        self.search_hometoun = ''
        self.search_id = ''


    def loop_bot(self):
        for this_event in longpoll.listen():
            if this_event.type == VkEventType.MESSAGE_NEW:
                if this_event.to_me:
                    message_text = this_event.text
                    return message_text, this_event.user_id

    def pattern_bot(self):
        request_session = requests.Session()
        vk_session = vk_api.VkApi(token=group_token)
        # vk = vk_session.get_api()
        # upload = VkUpload(vk_session)  # Для загрузки изображений
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW \
                    and event.to_me and event.text:
                print('id{}: "{}"'.format(event.user_id, event.text), end=' ')
                self._user = Self_user()
                self.f_name = f'{self._user.user_lastname(event.user_id)} ' \
                              f'{self._user.user_first_name(event.user_id)}'
                pprint(log(f'[пользователь - '
                           f'{self.f_name}'
                           f' dID - {event.user_id} '
                           f'\ndb object at {event} '
                           f'\nподключен к сессии - {request_session}]'))
                return event.text, event.user_id
            # else:
            #     return None, event.user_id


    @staticmethod
    def hi(user_id):
        write_msg(user_id,
                  hello_post)

    @staticmethod
    def menu_bot(user_id):
        write_msg(user_id,
                  bot_menu)

    @staticmethod
    def show_info(user_id):
        write_msg(user_id, info_post)

    @staticmethod
    def reg_new_user(id_num):
        write_msg(id_num, 'Вы прошли регистрацию.')
        write_msg(id_num,
                  start_post)
        register_user(id_num)

    def method_photo(self, photo, item_result, user_id, user_photo):
        sorted_user_photo = photo.sort_likes(user_photo)
        # Выводим отсортированные данные по анкетам
        write_msg(user_id, (
            f'\n{item_result["first_name"]}'
            f'{item_result["last_name"]} '
            f'{item_result["profile"]}',
        ))

        MAX_PHOTO_COUNT = 3  # можно вынесни на лобальный урвоень в  конфиге
        slice_step = -MAX_PHOTO_COUNT - 1
        for item_photo in sorted_user_photo[-1:slice_step:-1]:
            # [-1:-4:-1] вернет 3 эелемента с конца списка
            write_msg(user_id, 'фото:', attachment=item_photo[1])
        print(sorted_user_photo)

    @staticmethod
    def check_sex_message(_msg_text):
        search_sex = None
        if _msg_text == 'м ж':
            search_sex = 0
        elif _msg_text.lower() == 'девушка':
            search_sex = 1
        elif _msg_text.lower() == 'парень':
            search_sex = 2
        return search_sex

    def get_age_from(self):
        msg_text, user_id = self.loop_bot()
        write_msg(user_id,
                  'введите возраст '
                  'от - (минимальный возраст 18)')
        msg_text, user_id = self.pattern_bot()
        self.search_age_from = msg_text
        if int(self.search_age_from) < 18:
            write_msg(user_id, post1)
            self.search_age_from = 18

        else:
            self.search_age_from = msg_text

    def get_age_to(self):
        msg_text, user_id = self.loop_bot()
        write_msg(user_id, 'введите возраст до - ')
        msg_text, user_id = self.pattern_bot()
        self.search_age_to = msg_text

    def get_hometown(self):
        msg_text, user_id = self.loop_bot()
        write_msg(user_id, 'введите город - .')
        msg_text, user_id = self.pattern_bot()
        self.search_hometoun = msg_text

    def method_reg_user(self, user_id):
        _session = Session()
        current_user_id = check_db_master(user_id, _session)
        if not current_user_id:
            self.hi(user_id)
            # msg_text, user_id = self.pattern_bot()
            # write_msg(user_id, post4)

            self.reg_new_user(user_id)
            # sg_text, user_id = self.pattern_bot()
        return current_user_id, user_id


    def check_config_actions(self, user_id, _msg_text):
        conf = global_user_configs[user_id]
        _sex = self.check_sex_message(_msg_text)
        if _sex is not None:
            conf['sex'] = _sex

        elif _msg_text.startswith('от '):
            _from = int(_msg_text[2:].strip())
            conf['age_from'] = _from
            write_msg(user_id, f'вы выбрали {_msg_text}')
            if int(_from) < 18:
                write_msg(user_id, post1)
                conf['age_from'] = 18

        elif _msg_text.startswith('до '):
            _from = int(_msg_text[2:].strip())
            conf['age_to'] = _from
            if int(conf['age_to']) < int(conf['age_from']):
                write_msg(user_id,
                          'выбран неверный возрастной интервал')
                conf['age_to'] = conf['age_from']

        elif _msg_text.startswith('город '):
            self.search_hometoun = _msg_text[5:].strip()
            conf['hometown'] = self.search_hometoun
            if self.validation_user_settings(user_id):
                self.action_search(user_id)
        else:
            return


    def validation_user_settings(self, user_id):
        conf = global_user_configs[user_id]
        all_fields = ['sex', 'age_from', 'age_to', 'hometown']
        left_config = set(all_fields).difference(conf.keys())
        if len(left_config) == len(all_fields):
            write_msg(user_id, f'Приветствую Вас '
                               f'{self._user.user_first_name(user_id)}')
        result = False
        if not conf.get('sex'):
            keyboard2(user_id=user_id, vk=self.vk_)
        elif not conf.get('age_from'):
            write_msg(user_id, 'введите возраст: от (минимальный возраст 18)\n Например: <от 18>')
        elif not conf.get('age_to'):
            write_msg(user_id, 'введите возраст до - \n  Например: <до 18>')
        elif not conf.get('hometown'):
            write_msg(user_id, 'введите город - \n Например: <Город Москва>')
        else:
            result = True
        return result

    def run(self):
        # _session, user_id = self.run_bot()
        while True:
            msg_text, user_id = self.pattern_bot()
            msg_text = msg_text.strip().lower()
            current_user_id, user_id = self.method_reg_user(user_id)

            self.check_config_actions(user_id, msg_text)

            validated = self.validation_user_settings(user_id)
            if not validated:
                continue

            if msg_text == 'поиск':
                self.action_search(user_id)
            elif msg_text == 'далее':
                self.next_dating_result(user_id)
            elif msg_text == 'добавить в избранное':
                self.action_add_favorite(user_id, current_user_id)
            elif msg_text == 'заблокировать':
                self.action_add_blacklist(user_id, current_user_id)
            elif msg_text.lower() == 'выход':
                write_msg(user_id, start_post)
            elif msg_text == 'избранное':
                self.go_to_favorites(user_id)
            elif msg_text == 'спам':
                self.go_to_blacklist(user_id)
            else:
                self.menu_bot(user_id)
                send_keyboard(user_id)

    def action_search(self, user_id):
        """Запускает поиск с предварительной валидацией настройки"""

        conf = global_user_configs[user_id]
        user = Users(**conf)
        result = global_result.get(user_id)
        if not result:
            result = user.search_users()
            global_result[user_id] = result
        self._send_dating_result(user_id)
        keyboard3(user_id=user_id, vk=self.vk_)

    def action_add_blacklist(self, user_id, current_user_id):
        _result = global_result.get(user_id)
        if not _result:
            self.show_info(user_id)
            return
        result_item = _result.pop(0)
        is_black = add_to_black_list(
            user_id,
            result_item['id'], result_item['last_name'], result_item['first_name'],
            self.search_hometoun, result_item['profile'],
            current_user_id.id
        )
        if is_black:
            self.action_search(user_id)

    def action_add_favorite(self, user_id, current_user_id):
        _result = global_result.get(user_id)
        if not _result:
            self.show_info(user_id)
            return None
        result_item = _result.pop(0)
        # Пробуем добавить анкету в БД
        try:
            added = add_user(
                user_id,
                result_item['id'], result_item['last_name'], result_item['first_name'],
                self.search_hometoun, result_item['profile'],
                current_user_id.id,
            )
            #  можно передавать весь result_item, оставил функцию как есть
            if added:
                self.action_search(user_id)
        except AttributeError:
            write_msg(user_id, 'Вы не зарегистрировались!\n Введите start для перезагрузки бота')

    def next_dating_result(self, user_id):
        #  вырезаем крайнего кандидата из буфера после того как вернули
        _result = global_result.get(user_id)
        if not _result:
            self.show_info(user_id)
            return None
        _result.pop(0)
        self.action_search(user_id)

    def _send_dating_result(self, user_id):
        _result = global_result.get(user_id)
        if not _result:
            self.show_info(user_id)
            return None
        _result_item = _result[0]
        dating_user, blocked_user = check_db_user(_result_item['id'])
        # Получаем фото и сортируем по лайкам
        photo = Photo(_result_item['id'])
        user_photo = photo.get_photo()
        if (
            user_photo == 'нет доступа к фото'
            or dating_user is not None
            or blocked_user is not None
        ):
            _result.pop(0)
            return self._send_dating_result(user_id)

        self.method_photo(photo, _result_item, user_id, user_photo)
        write_msg(user_id, post3)
        return _result_item

    # просматриваем избранные анкеты
    def go_to_favorites(self, ids):
        alls_users = check_db_favorites(ids)
        write_msg(ids, 'Избранные анкеты:')
        for nums, users in enumerate(alls_users):
            write_msg(ids, f'{users.first_name}, '
                           f'{users.second_name}, '
                           f'{users.link}')
            write_msg(ids, ation1_post)
            msg_texts, user_ids = self.pattern_bot()
            if msg_texts == '0':
                if nums >= len(alls_users) - 1:
                    write_msg(user_ids, post6)
            # Удаляем запись из бд - избранное
            elif msg_texts == '1':
                delete_db_favorites(users.vk_id)
                write_msg(user_ids, 'Анкета успешно удалена.')
                if nums >= len(alls_users) - 1:
                    write_msg(user_ids, post6)
            elif msg_texts.lower() == 'q':
                write_msg(ids, start_post)
                break


    # переходим в черный список
    def go_to_blacklist(self, ids):
        all_users = check_db_black(ids)
        write_msg(ids, 'Анкеты в черном списке:')
        for num, user in enumerate(all_users):
            write_msg(ids, f'{user.first_name}, '
                           f'{user.second_name}, '
                           f'{user.link}, '
                           f'{user.link_photo}')
            write_msg(ids, '1 - Удалить из черного списка, '
                           '0 - Далее \n'
                           'q - Выход')
            msg_texts, user_ids = self.pattern_bot()
            if msg_texts == '0':
                if num >= len(all_users) - 1:
                    write_msg(user_ids, post6)
            # Удаляем запись из бд - черный список
            elif msg_texts == '1':
                print(user.id)
                delete_db_blacklist(user.vk_id)
                write_msg(user_ids, 'Анкета успешно удалена')
                if num >= len(all_users) - 1:
                    write_msg(user_ids, post6)
            elif msg_texts.lower() == 'q':
                write_msg(ids, start_post)
                break

    # проверяем посковый запрос пользователя
    def go_to_search(self, ids):
        all_users = check_db_searcht(ids)
        write_msg(ids, 'Анкеты:')
        for num, user in enumerate(all_users):
            write_msg(ids, f'{user.first_name}, '
                           f'{user.second_name}, '
                           f'{user.link}')
            write_msg(ids, ation2_post)
            msg_texts, user_ids = self.pattern_bot()
            if msg_texts == '0':
                if num >= len(all_users) - 1:
                    write_msg(user_ids, post6)
            # Удаляем запись из бд - черный список
            elif msg_texts == '1':
                print(user.id)
                delete_db_blacklist(user.vk_id)
                write_msg(user_ids, 'Анкета успешно удалена')
                if num >= len(all_users) - 1:
                    write_msg(user_ids, post5)
            elif msg_texts.lower() == 'q':
                write_msg(ids, start_post)
                break

    def method_favorits(self, current_user_id, hometown, i, result, user_id):
        add_user(user_id,
                 result[i]['id'],
                 result[i]['last_name'],
                 result[i]['first_name'],
                 hometown,
                 result[i]['profile'],
                 current_user_id.id)













    # def pattern_search(self, current_user_id, search_uss, session):
    # msg_text, user_id = self.pattern_bot()
    # sex = msg_text
    # if msg_text == 'М Ж':
    #     sex = 0
    #     search_uss.append(sex)
    # if msg_text.lower() == 'девушка':
    #     sex = 1
    #     search_uss.append(sex)
    # if msg_text.lower() == 'парень':
    #     sex = 2
    #     search_uss.append(sex)
    # write_msg(user_id,
    #           'введите возраст '
    #           'от - (минимальный возраст 18)')
    # msg_text, user_id = self.pattern_bot()
    # age_from = msg_text
    # if int(age_from) < 18:
    #     write_msg(user_id, post1)
    #     age_from = 18
    #     search_uss.append(age_from)
    # else:
    #     search_uss.append(age_from)
    # write_msg(user_id, 'введите возраст до - ')
    # msg_text, user_id = self.pattern_bot()
    # age_to = msg_text
    # search_uss.append(age_to)
    # write_msg(user_id, 'введите город - .')
    # msg_text, user_id = self.pattern_bot()
    # hometown = msg_text
    # search_uss.append(hometown)
    # # Ищем анкеты
    # user = Users(*search_uss)
    # result = user.search_users()
    # search_uss.clear()
    # # json_create(result)
    # current_user_id = check_db_master(
    #     user_id, session=session)
    # return current_user_id, hometown, result, user_id

    def method_auto_search(self, search_uss):
        msg_text, user_id = self.pattern_bot()
        sex = msg_text
        if msg_text == 'М Ж':
            sex = 0
            search_uss.append(sex)
        if msg_text.lower() == 'девушка':
            sex = 1
            search_uss.append(sex)
        if msg_text.lower() == 'парень':
            sex = 2
            search_uss.append(sex)
        client = Client(user_id)
        age_from = client.age - 3
        if age_from < 18:
            age_from = 18
            search_uss.append(age_from)
        age_at = client.age + 3
        search_uss.append(age_at)
        search_uss.append(client.age)
        hometown = client.city
        search_uss.append(hometown)
        user = Users(*search_uss)
        result = user.search_users()
        search_uss.clear()
        return result

    # def run_bot(self):
    #     msg_text, user_id = self.pattern_bot()
    #     _session = Session()
    #     current_user_id = check_db_master(user_id, _session)
    #     if not current_user_id:
    #         # msg_text, user_id = self.pattern_bot()
    #         write_msg(user_id, 'вы не зарегистрированы, пройдите регистрацию')
    #         self.reg_new_user(user_id)
    #     return _session, user_id



    def main_loop(self):
        """Main part of script"""

        # Define functions
        def run_listening():
            """Runs longpoll_m listening"""

            # Define functions for threads
            def thread_for_conversation(event_obj_th, command_centre_t):
                """Run command centre for conversation."""
                message_object = event_obj_th.object
                # Call command centre
                command_centre_t.run_function(message_object)

            def thread_for_user_chat(event_obj_th2, command_centre_t):
                """Run command centre for user chat."""
                message_object = event_obj_th2.object
                # Call command centre
                command_centre_t.run_function(message_object)

            # Init thread vars
            thread_Conv = False
            thread_UChat = False

            for event in longpoll.listen():
                # Check for Conversation
                if event.type == VkBotEventType.MESSAGE_NEW and event.object.text and event.from_chat:
                    if thread_Conv:
                        if thread_Conv.isAlive() is False:
                            # Stop thread when thread work finish.
                            thread_Conv.join()
                    # Make Thread
                    thread_Conv = Thread(target=thread_for_conversation, args=(event, command_centre_m))
                    # Start thread
                    thread_Conv.start()

                # Check for message from user.
                if event.type == VkBotEventType.MESSAGE_NEW and event.object.text and event.from_user:
                    if thread_UChat:
                        if thread_UChat.isAlive() is False:
                            # Stop thread when thread work finish.
                            thread_UChat.join()
                    # Make Thread
                    thread_UChat = Thread(target=thread_for_user_chat, args=(event, command_centre_m))
                    # Start thread
                    thread_UChat.start()

        def check_internet_connection():
            """Checks internet connection by sending a request to vk.com"""
            try:
                request = requests.get(url='https://vk.com/')
                if request.status_code == 200:
                    return True
                else:
                    return True
            except requests.exceptions.RequestException:
                return False

        # Prevent crash bot when the internet goes down
        while True:
            try:
                # Run longpoll_m listening.
                run_listening()
            except requests.exceptions.RequestException:
                while True:
                    # Check internet connection
                    internet_status = check_internet_connection()
                    # If everything is bad, we wait and try to connect again
                    if internet_status:
                        break
                    else:
                        print('VK_BOT [Longpoll Listening Error!]: Internet does not work!')
                    # Time to rest!
                    time.sleep(120)

    def _response(self, userState, userId):

        '''
        В случае линейной цепочки вопросов без возможности возврата назад
        Начало +-> Вопрос 1 +-> Вопрос 2 +-> Вопрос 3 +-> Конец
            ^   +        ^   +        ^   +
            +---+        +---+        +---+
        достаточно только хранить номер вопроса,
        на котором остановился пользователь.
        Если же диалог предполагается более сложны,
        разветвлённым и даже с возвратами на предыдущие шаги,
        Начало +-> Вопрос 1 +-> Вопрос 2 +-> Конец
                     +              ^
                     +-> Вопрос 3 +-+ '''


        users = []  # список пользователей
        # если произошло какое-то событие (пришло сообщение)
        for event in longpoll.listen():
              # если id пользователя нет в списке:
            if event.user_id not in users:
                # то он добавляется в список...
                users.append(event.user_id)
                # ...и для него создаётся новый поток
                thread = threading.Thread(target=self.chat1,
                                          args=(event.user_id, request))
                thread.start()
                 # тот поток, чей id совпадает с id пользователя, который прислал новое сообщение...
            if event.user_id == userId:
                  if userState == 1:
                      self.chat1(event.user_id, request)
                  elif userState == 2:
                      self.chat2(event.user_id, request)
