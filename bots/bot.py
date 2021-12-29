from collections import defaultdict

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from data_search.data_search import Users, Photo
from data_base.db import engine, Session, User

from data_base.db_func import (write_msg, register_user,
                               add_user, add_to_black_list,
                               check_db_user, check_db_black,
                               check_db_favorites, check_db_master,
                               delete_db_blacklist, delete_db_favorites,
                               check_db_searcht)
from VK_token import (group_token)
from logers.logers import log
from pprint import pprint
import requests
from bots.bot_message import (post1, post3, hello_post,
                              bot_menu, info_post, post5,
                              start_post, post6, ation1_post, ation2_post)
# import threading
# from requests import request
# from threading import Thread
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
MAX_PHOTO_COUNT = 3  # можно вынесни на лобальный урвоень в  конфиге


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
        self.search_age_from = None
        self.search_age_to = None
        self.search_hometoun = None
        self.search_id = None

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
                f_name = f'{self._user.user_lastname(event.user_id)} ' \
                         f'{self._user.user_first_name(event.user_id)}'
                pprint(log(f'[пользователь - '
                           f'{f_name}'
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

    @staticmethod
    def start_keyboard(user_id):
        return send_keyboard(user_id)

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

        """
        функция просмотра избранных анкет
        пользователя сохраненных в БД
        """
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

    # просматриваем черный список
    def go_to_blacklist(self, ids):
        """
        функция просмотра черного списка
        пользователя сохраненного в БД
        """
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

    # сохраняем просмотренные пользователем анкеты
    def go_to_search(self, ids):
        """
        функция проверки поисковых
        запросов пользователя
        сохраненных в БД
        """
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





