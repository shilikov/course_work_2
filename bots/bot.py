import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from data_search.data_search import Users, Photo
from data_base.db import engine, Session
from data_base.db_func import write_msg, \
    register_user, add_user, \
    add_to_black_list, \
    check_db_user, check_db_black, \
    check_db_favorites, check_db_master, \
    delete_db_blacklist, delete_db_favorites, \
    check_db_searcht, add_to_searcht
from VK_token import group_token
from logers.logers import log
from pprint import pprint
from vk_api.utils import get_random_id
import requests
from bots.bot_message import post1


class Bot:
    def __init__(self):
        self.vk = vk_api.VkApi(token=group_token)
        self.longpoll = VkLongPoll(self.vk)
        self.session = requests.Session()
        self.connection = engine.connect()


    def pattern_bot(self):
        session = requests.Session()
        vk_session = vk_api.VkApi(token=group_token)
        # vk = vk_session.get_api()
        # upload = VkUpload(vk_session)  # Для загрузки изображений
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW \
                    and event.to_me and event.text:
                print('id{}: "{}"'.format(event.user_id, event.text), end=' ')
                pprint(log(f'[пользователь с ID - {event.user_id} '
                           f'\ndb object at {event} '
                           f'\nподключен к сессии - {session}]'))
                return event.text, event.user_id

    def hi(self, id_num):
        self.id_num = id_num
        write_msg(self.id_num,
                  "Вас приветствует бот - vkinder\n"
                  "для продолжения введите - start")

    def menu_bot(self, id_num):
        self.id_num = id_num
        write_msg(self.id_num,
                  "\nДля поиска - введите - поиск \n"
                  "Перейти в избранное нажмите - избранное\n"
                  "Перейти в черный список - спам")

    def show_info(self, user_id):

        write_msg(user_id, 'Вы посмотрели все анкеты.'
                           'Перейти в избранное - избранное'
                           'Перейти в черный список - спам'
                           'Меню бота - start')

    def reg_new_user(self, id_num):
        write_msg(id_num, 'Вы прошли регистрацию.')
        write_msg(id_num,
                  "start - для активации бота\n")
        register_user(id_num)

    def go_to_favorites(self, ids):
        alls_users = check_db_favorites(ids)
        write_msg(ids, 'Избранные анкеты:')
        for nums, users in enumerate(alls_users):
            write_msg(ids, f'{users.first_name}, '
                           f'{users.second_name}, '
                           f'{users.link}')
            write_msg(ids, '1 - Удалить из избранного, 0 - Далее \nq - Выход')
            msg_texts, user_ids = Bot.pattern_bot()
            if msg_texts == '0':
                if nums >= len(alls_users) - 1:
                    write_msg(user_ids, 'Это была последняя анкета.\n'
                                        'start - вернуться в меню\n')
            # Удаляем запись из бд - избранное
            elif msg_texts == '1':
                delete_db_favorites(users.vk_id)
                write_msg(user_ids, 'Анкета успешно удалена.')
                if nums >= len(alls_users) - 1:
                    write_msg(user_ids, 'Это была последняя анкета.\n'
                                        'start - вернуться в меню\n')
            elif msg_texts.lower() == 'q':
                write_msg(ids, 'Vkinder - для активации бота.')
                break

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
            msg_texts, user_ids = Bot.pattern_bot()
            if msg_texts == '0':
                if num >= len(all_users) - 1:
                    write_msg(user_ids, 'Это была последняя анкета.\n'
                                        'start - вернуться в меню\n')
            # Удаляем запись из бд - черный список
            elif msg_texts == '1':
                print(user.id)
                delete_db_blacklist(user.vk_id)
                write_msg(user_ids, 'Анкета успешно удалена')
                if num >= len(all_users) - 1:
                    write_msg(user_ids, 'Это была последняя анкета.\n'
                                        'start - вернуться в меню\n')
            elif msg_texts.lower() == 'q':
                write_msg(ids, 'start - для активации бота.')
                break

    # проверяем посковый запрос пользователя
    def go_to_search(self, ids):
        all_users = check_db_searcht(ids)
        write_msg(ids, 'Анкеты:')
        for num, user in enumerate(all_users):
            write_msg(ids, f'{user.first_name}, '
                           f'{user.second_name}, '
                           f'{user.link}')
            write_msg(ids, '1 - Удалить из черного списка,'
                           ' 0 - Далее \nq - Выход')
            msg_texts, user_ids = Bot.pattern_bot()
            if msg_texts == '0':
                if num >= len(all_users) - 1:
                    write_msg(user_ids, 'Это была последняя анкета.\n'
                                        'start - вернуться в меню\n')
            # Удаляем запись из бд - черный список
            elif msg_texts == '1':
                print(user.id)
                delete_db_blacklist(user.vk_id)
                write_msg(user_ids, 'Анкета успешно удалена')
                if num >= len(all_users) - 1:
                    write_msg(user_ids, 'Это была последняя анкета.\n'
                                        'start - вернуться в меню\n')
            elif msg_texts.lower() == 'q':
                write_msg(ids, 'Vkinder - для активации бота.')
                break

    def method_photo(self, i, photo, result, user_id, user_photo):
        sorted_user_photo = photo.sort_likes(
            user_photo)
        # Выводим отсортированные
        # данные
        # по анкетам
        write_msg(
            user_id, f'\n{result[i]["first_name"]}'
                     f'{result[i]["last_name"]} '
                     f'{result[i]["profile"]}', )
        try:
            write_msg(user_id, 'фото:',
                      attachment=','.join
                      ([sorted_user_photo[-1][1],
                        sorted_user_photo[-2][1],
                        sorted_user_photo[-3][1]]))
            print(sorted_user_photo)
        except IndexError:
            for photo in range(len(sorted_user_photo)):
                write_msg(user_id, 'фото:',
                          attachment=sorted_user_photo[
                              photo][1])

    def pattern_search(self, current_user_id, search_uss, session):
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
        write_msg(user_id,
                  'введите возраст '
                  'от - (минимальный возраст 18)')
        msg_text, user_id = self.pattern_bot()
        age_from = msg_text
        if int(age_from) < 18:
            write_msg(user_id, post1)
            age_from = 18
            search_uss.append(age_from)
        else:
            search_uss.append(age_from)
        write_msg(user_id, 'введите возраст до - ')
        msg_text, user_id = self.pattern_bot()
        age_to = msg_text
        search_uss.append(age_to)
        write_msg(user_id, 'введите город - .')
        msg_text, user_id = self.pattern_bot()
        hometown = msg_text
        search_uss.append(hometown)
        # Ищем анкеты
        user = Users(*search_uss)
        result = user.search_users()
        search_uss.clear()
        # json_create(result)
        current_user_id = check_db_master(
            user_id, session=session)
        return current_user_id, hometown, result, user_id

    def keyboard3(self, user_id, vk):
        keyboard3 = VkKeyboard(one_time=True)
        keyboard3.get_empty_keyboard()
        keyboard3.add_button('добавить в избранное',
                             VkKeyboardColor.SECONDARY)
        keyboard3.add_button('заблокировать',
                             VkKeyboardColor.POSITIVE)
        keyboard3.add_line()
        keyboard3.add_button('далее',
                             VkKeyboardColor.NEGATIVE)
        keyboard3.add_button('выход',
                             VkKeyboardColor.NEGATIVE)
        vk.messages.send(
            peer_id=user_id,
            random_id=get_random_id(),
            keyboard=keyboard3.get_keyboard(),
            message='введите пол кого хотите найти'
        )

    def keyboard2(self, user_id, vk):
        keyboard2 = VkKeyboard(one_time=True)
        keyboard2.get_empty_keyboard()
        keyboard2.add_button('М Ж',
                             VkKeyboardColor.SECONDARY)
        keyboard2.add_button('девушка',
                             VkKeyboardColor.POSITIVE)
        keyboard2.add_button('парень',
                             VkKeyboardColor.NEGATIVE)
        vk.messages.send(
            peer_id=user_id,
            random_id=get_random_id(),
            keyboard=keyboard2.get_keyboard(),
            message='введите пол кого хотите найти'
        )

    def keyboard1(self):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('поиск',
                            color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('избранное',
                            color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('спам',
                            color=VkKeyboardColor.NEGATIVE)
        return keyboard

    def method_reg_user(self, session, user_id):
        current_user_id = check_db_master(user_id, session)
        if not current_user_id:
            msg_text, user_id = self.pattern_bot()
            write_msg(user_id, 'вы не зарегистрированы, '
                               'пройдите регистрацию')

            self.reg_new_user(user_id)
            sg_text, user_id = self.pattern_bot()

            # Регистрируем пользователя в БД
            # if msg_text.lower() == 'да':
            #     bot.reg_new_user(user_id)
        return current_user_id, user_id

    def run_bot(self):
        msg_text, user_id = self.pattern_bot()
        session = Session()
        current_user_id = check_db_master(user_id, session)
        if not current_user_id:
            msg_text, user_id = self.pattern_bot()
            write_msg(user_id, 'вы не зарегистрированы, пройдите регистрацию')
            self.reg_new_user(user_id)
        return session, user_id





    def run(self):
        session, user_id = self.run_bot()
        while True:
            self.hi(user_id)
            msg_text, user_id = self.pattern_bot()
            if msg_text == "start":
                current_user_id, user_id = self.method_reg_user(session, user_id)
                if current_user_id:
                    search_uss = []
                    # msg_text, user_id = bot.loop_bot()
                    write_msg(user_id, 'Выберите действие')
                    vk_session = vk_api.VkApi(token=group_token)
                    vk = vk_session.get_api()
                    keyboard = self.keyboard1()
                    for event in self.longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW:
                            if event.to_me:
                                ...
                        vk.messages.send(
                            peer_id=user_id,
                            random_id=get_random_id(),
                            keyboard=keyboard.get_keyboard(),
                            message='Пример клавиатуры'
                        )
                        self.menu_bot(user_id)
                        # msg_text, user_id = bot.pats

                        msg_text, user_id = self.pattern_bot()
                        if msg_text == 'поиск':
                            self.keyboard2(user_id, vk)

                            write_msg(user_id,
                                      'введите пол кого хотите найти')
                            current_user_id, hometown, \
                            result, user_id = self.pattern_search(current_user_id,
                                                                  search_uss, session)
                            # Производим отбор анкет
                            for i in range(len(result)):
                                # print(result[i]['id'],
                                # result[i]['last_name'],
                                #       result[i]['first_name'],
                                #       hometown,
                                #       result[i]['profile'])
                                dating_user, blocked_user = check_db_user(
                                    result[i]['id'])
                                # Получаем фото и сортируем по лайкам
                                photo = Photo(result[i]['id'])
                                user_photo = photo.get_photo()
                                if user_photo == 'нет ' \
                                                 'доступа ' \
                                                 'к фото' or dating_user \
                                        is not None or \
                                        blocked_user is not None:
                                    continue
                                self.method_photo(i, photo, result, user_id, user_photo)

                                # Ждем пользовательский ввод

                                write_msg(user_id, '1 - Добавить, '
                                                   '2 - Заблокировать, '
                                                   '0 - Далее, \n'
                                                   'q - выход из поиска')
                                self.keyboard3(user_id, vk)
                                msg_text, user_id = self.pattern_bot()

                                if msg_text == 'далее':
                                    # Проверка на последнюю запись
                                    if i >= len(result) - 1:
                                        self.show_info(user_id)
                                # Добавляем пользователя в избранное
                                elif msg_text == 'добавить в избранное':
                                    # Проверка на последнюю запись
                                    if i >= len(result) - 1:
                                        self.show_info(user_id)
                                        break
                                    # Пробуем добавить анкету в БД
                                    try:
                                        add_user(user_id, result[i]['id'],
                                                 result[i]['last_name'],
                                                 result[i]['first_name'],
                                                 hometown,
                                                 result[i]['profile'],
                                                 current_user_id.id)
                                    except AttributeError:
                                        write_msg(user_id,
                                                  'Вы не зарегистрировались!'
                                                  '\n Введите start '
                                                  'для перезагрузки бота')
                                        break
                                # Добавляем пользователя в черный список
                                elif msg_text == 'заблокировать':
                                    # Проверка на последнюю запись
                                    if i >= len(result) - 1:
                                        self.show_info(user_id)
                                    # Блокируем
                                    add_to_black_list(user_id,
                                                      result[i]['id'],
                                                      result[i]['last_name'],
                                                      result[i]['first_name'],
                                                      hometown,
                                                      result[i]['profile'],
                                                      current_user_id.id)
                                elif msg_text.lower() == 'выход':
                                    write_msg(user_id, 'Введите start '
                                                       'для активации бота')
                                    break

                        # Переходим в избранное
                        elif msg_text == 'избранное':
                            self.go_to_favorites(user_id)

                        # Переходим в черный список
                        elif msg_text == 'спам':
                            self.go_to_blacklist(user_id)






