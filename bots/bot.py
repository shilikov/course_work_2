import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from data_search.data_search import Users, Photo
from data_base.db import engine, Session
from data_base.db_func import write_msg, register_user, add_user, add_user_photos, add_to_black_list, \
    check_db_user, check_db_black, check_db_favorites, check_db_master, delete_db_blacklist, delete_db_favorites, \
    add_to_searcht, check_db_searcht
from VK_token import group_token
from keyboards.keyboards import *
from logers.logers import log_to_console, log




class Bot:

    def __init__(self):

        self.vk = vk_api.VkApi(token=group_token)
        self.longpoll = VkLongPoll(self.vk)
        self.session = Session()
        self.connection = engine.connect()


    @staticmethod

    def pattern_bot():
        bot = Bot()

        for this_event in bot.longpoll.listen():
            if this_event.type == VkEventType.MESSAGE_NEW:
                if this_event.to_me:
                    user_id = this_event.user_id
                    session = Session()
                    print(log(f'[пользователь с ID - {user_id} подключен к сессии - {session}]'))

                    check_db_master(user_id, session=session)
                    message_text = this_event.text
                    return message_text, this_event.user_id

    def hi(self, id_num):
        self.id_num = id_num
        write_msg(self.id_num,
                  f"Вас приветствует бот - vkinder\n"
                  f"для продолжения введите - start")

    def menu_bot(self, id_num):
        self.id_num = id_num
        write_msg(self.id_num,
                  f"\nДля поиска - введите - поиск \n"
                  f"Перейти в избранное нажмите - избранное\n"
                  f"Перейти в черный список - спам")


    def show_info(self, user_id):
        self.user_id = user_id
        write_msg(self.user_id, f'Вы посмотрели все анкеты.'
                           f'Перейти в избранное - избранное'
                           f'Перейти в черный список - спам'
                           f'Меню бота - start')


    def reg_new_user(self, id_num):
        write_msg(id_num, 'Вы прошли регистрацию.')
        write_msg(id_num,
                  f"start - для активации бота\n")
        register_user(id_num)


    def go_to_favorites(self, ids):
        alls_users = check_db_favorites(ids)
        write_msg(ids, f'Избранные анкеты:')
        for nums, users in enumerate(alls_users):
            write_msg(ids, f'{users.first_name}, {users.second_name}, {users.link}')
            write_msg(ids, '1 - Удалить из избранного, 0 - Далее \nq - Выход')
            msg_texts, user_ids = Bot.pattern_bot()
            if msg_texts == '0':
                if nums >= len(alls_users) - 1:
                    write_msg(user_ids, f'Это была последняя анкета.\n'
                                        f'start - вернуться в меню\n')
            # Удаляем запись из бд - избранное
            elif msg_texts == '1':
                delete_db_favorites(users.vk_id)
                write_msg(user_ids, f'Анкета успешно удалена.')
                if nums >= len(alls_users) - 1:
                    write_msg(user_ids, f'Это была последняя анкета.\n'
                                        f'start - вернуться в меню\n')
            elif msg_texts.lower() == 'q':
                write_msg(ids, 'Vkinder - для активации бота.')
                break


    def go_to_blacklist(self, ids):
        all_users = check_db_black(ids)
        write_msg(ids, f'Анкеты в черном списке:')
        for num, user in enumerate(all_users):
            write_msg(ids, f'{user.first_name}, {user.second_name}, {user.link}')
            write_msg(ids, '1 - Удалить из черного списка, 0 - Далее \nq - Выход')
            msg_texts, user_ids = Bot.pattern_bot()
            if msg_texts == '0':
                if num >= len(all_users) - 1:
                    write_msg(user_ids, f'Это была последняя анкета.\n'
                                        f'start - вернуться в меню\n')
            # Удаляем запись из бд - черный список
            elif msg_texts == '1':
                print(user.id)
                delete_db_blacklist(user.vk_id)
                write_msg(user_ids, f'Анкета успешно удалена')
                if num >= len(all_users) - 1:
                    write_msg(user_ids, f'Это была последняя анкета.\n'
                                        f'start - вернуться в меню\n')
            elif msg_texts.lower() == 'q':
                write_msg(ids, 'Vkinder - для активации бота.')
                break

    # проверяем посковый запрос пользователя
    def go_to_search(self, ids):
        all_users = check_db_searcht(ids)
        write_msg(ids, f'Анкеты:')
        for num, user in enumerate(all_users):
            write_msg(ids, f'{user.first_name}, {user.second_name}, {user.link}')
            write_msg(ids, '1 - Удалить из черного списка, 0 - Далее \nq - Выход')
            msg_texts, user_ids = Bot.pattern_bot()
            if msg_texts == '0':
                if num >= len(all_users) - 1:
                    write_msg(user_ids, f'Это была последняя анкета.\n'
                                        f'start - вернуться в меню\n')
            # Удаляем запись из бд - черный список
            elif msg_texts == '1':
                print(user.id)
                delete_db_blacklist(user.vk_id)
                write_msg(user_ids, f'Анкета успешно удалена')
                if num >= len(all_users) - 1:
                    write_msg(user_ids, f'Это была последняя анкета.\n'
                                        f'start - вернуться в меню\n')
            elif msg_texts.lower() == 'q':
                write_msg(ids, 'Vkinder - для активации бота.')
                break




    def run(self):

        bot = Bot()
        while True:



            msg_text, user_id = bot.pattern_bot()
            session = Session()
            # current_user_id = check_db_master(user_id, session)

            bot.hi(user_id)

            if msg_text == "start":
                # current_user_id = check_db_master(user_id)
                current_user_id = check_db_master(user_id, session)
                if not current_user_id:
                    msg_text, user_id = bot.pattern_bot()
                    write_msg(user_id, 'вы не зарегистрированы, пройдите регистрацию')
                    bot.reg_new_user(user_id)
                    sg_text, user_id = bot.pattern_bot()

                    # Регистрируем пользователя в БД
                    # if msg_text.lower() == 'да':
                    #     bot.reg_new_user(user_id)
                if current_user_id:
                    search_uss = []
                    # msg_text, user_id = bot.loop_bot()
                    write_msg(user_id, 'Выберите действие', shop_key)
                    bot.menu_bot(user_id)

                    msg_text, user_id = bot.pattern_bot()
                    if msg_text == 'поиск':
                        write_msg(user_id, 'введите пол кого хотите найти')
                        msg_text, user_id = bot.pattern_bot()
                        sex = msg_text
                        if msg_text == 'М Ж':
                            sex = 0
                            search_uss.append(sex)
                        if msg_text.lower() == 'девушка':
                            sex = 1
                            search_uss.append(sex)
                        if msg_text.lower() == 'мужчина':
                            sex = 2
                            search_uss.append(sex)
                        write_msg(user_id, 'введите возраст от - (минимальный возраст 18)')

                        msg_text, user_id = bot.pattern_bot()

                        age_from = msg_text

                        if int(age_from) < 18:
                            write_msg(user_id, f'вами был выставлен возраст ниже допустимого,'
                                               f'алгоритм поиска оптимизирован'
                                               f'выставлен минимальный допустимый возраст 18лет')
                            age_from = 18
                            search_uss.append(age_from)
                        else:
                            search_uss.append(age_from)

                        write_msg(user_id, 'введите возраст до - ')

                        msg_text, user_id = bot.pattern_bot()
                        age_to = msg_text
                        search_uss.append(age_to)

                        write_msg(user_id, 'введите город - .')

                        msg_text, user_id = bot.pattern_bot()
                        hometown = msg_text
                        search_uss.append(hometown)


                        # Ищем анкеты
                        user = Users(*search_uss)
                        result = user.search_users()
                        # json_create(result)
                        current_user_id = check_db_master(user_id,session=session)

                        # Производим отбор анкет
                        for i in range(len(result)):
                            print(result[i]['id'], result[i]['last_name'],
                                  result[i]['first_name'], hometown, result[i]['profile'])
                            dating_user, blocked_user = check_db_user(result[i]['id'])
                            # Получаем фото и сортируем по лайкам
                            photo = Photo(result[i]['id'])
                            user_photo = photo.get_photo()
                            if user_photo == 'нет доступа к фото' or dating_user is not None or blocked_user is not None:
                                continue
                            sorted_user_photo = photo.sort_likes(user_photo)
                            # Выводим отсортированные данные по анкетам
                            write_msg(user_id, f'\n{result[i]["first_name"]}  '
                                               f'{result[i]["last_name"]}  '
                                               f'{result[i]["profile"]}', )
                            try:
                                write_msg(user_id, f'фото:',
                                          attachment=','.join
                                          ([sorted_user_photo[-1][1], sorted_user_photo[-2][1],
                                            sorted_user_photo[-3][1]]))
                            except IndexError:
                                for photo in range(len(sorted_user_photo)):
                                    write_msg(user_id, f'фото:',
                                              attachment=sorted_user_photo[photo][1])


                            # Ждем пользовательский ввод
                            # if i >= len(result) - 1:
                            #     bot.show_info(user_id)
                            #
                            # try:
                            #
                            #     add_to_searcht(user_id, result[i]['id'], result[i]['last_name'],
                            #                    result[i]['first_name'], hometown, result[i]['profile'],
                            #                    sorted_user_photo[-1][1], result[i]['id'], current_user_id.id)
                            # except IndexError:
                            #     for photo in range(len(sorted_user_photo)):
                            #         add_to_searcht(user_id, result[i]['id'], result[i]['last_name'],
                            #                        result[i]['first_name'], hometown, result[i]['profile'],
                            #                        sorted_user_photo[photo][1], result[i]['id'], current_user_id.id)

                            write_msg(user_id, '1 - Добавить, 2 - Заблокировать, 0 - Далее, \nq - выход из поиска')
                            msg_text, user_id = bot.pattern_bot()
                            if msg_text == '0':
                                # Проверка на последнюю запись
                                if i >= len(result) - 1:
                                    bot.show_info(user_id)
                            # Добавляем пользователя в избранное
                            elif msg_text == '1':
                                # Проверка на последнюю запись
                                if i >= len(result) - 1:
                                    bot.show_info(user_id)
                                    break
                                # Пробуем добавить анкету в БД
                                try:
                                    add_user(user_id, result[i]['id'], result[i]['last_name'],
                                             result[i]['first_name'], hometown, result[i]['profile'],
                                             current_user_id.id)
                                    # Пробуем добавить фото анкеты в БД
                                    add_user_photos(user_id, sorted_user_photo[0][1],
                                                    sorted_user_photo[0][0], current_user_id.id)
                                except AttributeError:
                                    write_msg(user_id,
                                              'Вы не зарегистрировались!\n Введите start для перезагрузки бота')
                                    break
                            # Добавляем пользователя в черный список
                            elif msg_text == '2':
                                # Проверка на последнюю запись
                                if i >= len(result) - 1:
                                    bot.show_info(user_id)
                                # Блокируем
                                add_to_black_list(user_id, result[i]['id'], result[i]['last_name'],
                                                  result[i]['first_name'], hometown, result[i]['profile'],
                                                  sorted_user_photo[0][1],
                                                  sorted_user_photo[0][0], current_user_id.id)
                            elif msg_text.lower() == 'q':
                                write_msg(user_id, 'Введите start для активации бота')
                                break

                    # Переходим в избранное
                    elif msg_text == 'избранное':
                        bot.go_to_favorites(user_id)

                    # Переходим в черный список
                    elif msg_text == 'спам':
                        bot.go_to_blacklist(user_id)




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