
from data_base.db import Searches, BlackList, User, DatingUser, Photos
from sqlalchemy.exc import IntegrityError, InvalidRequestError
import vk_api
from vk_api.longpoll import VkLongPoll
from VK_token import group_token
from random import randrange
import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
ФУНКЦИИ РАБОТЫ С БД
"""
Base = declarative_base()
engine = sq.create_engine('postgresql://postgres@localhost:5432/vkinder',
                          client_encoding='utf8')
Session = sessionmaker(bind=engine)

# Для работы с ВК
vk = vk_api.VkApi(token=group_token)
longpoll = VkLongPoll(vk)
# Для работы с БД
session = Session()
connection = engine.connect()


def delete_db_blacklist(ids):
    # Удаляет пользователя из черного списка
    current_user = session.query(
        BlackList).filter_by(
        vk_id=ids).first()
    session.delete(current_user)
    session.commit()


def delete_db_favorites(ids):
    # Удаляет пользователя из избранного
    current_user = session.query(
        DatingUser).filter_by(
        vk_id=ids).first()
    session.delete(current_user)
    session.commit()


def check_db_master(ids, session):
    # проверят зареган ли пользователь бота в БД
    current_user_id = session.query(
        User).filter_by(
        vk_id=ids).first()
    return current_user_id


def check_db_user(ids):
    # проверят есть ли юзер в бд
    dating_user = session.query(DatingUser).filter_by(
        vk_id=ids).first()
    blocked_user = session.query(BlackList).filter_by(
        vk_id=ids).first()

    return dating_user, blocked_user


def check_db_black(ids):
    # Проверят есть ли юзер в черном списке
    current_users_id = session.query(User).filter_by(vk_id=ids).first()
    # Находим все анкеты из избранного которые добавил данный юзер
    all_users = session.query(
        BlackList).filter_by(
        id_user=current_users_id.id).all()
    return all_users


def check_db_favorites(ids):
    # Проверяет есть ли юзер в избранном
    current_users_id = session.query(
        User).filter_by(
        vk_id=ids).first()
    # Находим все анкеты из избранного которые добавил данный юзер
    alls_users = session.query(
        DatingUser).filter_by(
        id_user=current_users_id.id).all()
    return alls_users


def check_db_searcht(ids):
    current_users_id = session.query(
        User).filter_by(vk_id=ids).first()
    # Находим все анкеты из избранного которые добавил данный юзер
    all_users = \
        session.query(Searches).filter_by(
            id_user=current_users_id.id).all()
    return all_users


def write_msg(user_id, message, keyboard=None, attachment=None):
    # Пишет сообщение пользователю

    vk.method('messages.send',
              {'user_id': user_id,
               'message': message,
               'random_id': randrange(10 ** 7),
               'attachment': attachment,
               'keboard': keyboard})


def register_user(vk_id):
    # Регистрация пользователя
    try:
        new_user = User(
            vk_id=vk_id
        )
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        return False


def add_user(event_id, vk_id, first_name, second_name, city, link, id_user):
    # Сохранение выбранного пользователя в БД
    try:
        new_user = DatingUser(
            vk_id=vk_id,
            first_name=first_name,
            second_name=second_name,
            city=city,
            link=link,
            id_user=id_user
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id,
                  'ПОЛЬЗОВАТЕЛЬ УСПЕШНО ДОБАВЛЕН В ИЗБРАННОЕ')
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id,
                  'Пользователь уже в избранном.')
        return False


def add_user_photos(event_id, link_photo, count_likes, id_dating_user):
    # Сохранение в БД фото добавленного пользователя
    try:
        new_user = Photos(
            link_photo=link_photo,
            count_likes=count_likes,
            id_dating_user=id_dating_user
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id,
                  'Фото пользователя сохранено в избранном')
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id,
                  'Невозможно добавить фото этого пользователя(Уже сохранено)')
        return False


def add_to_black_list(event_id, vk_id,
                      first_name, second_name,
                      city, link, id_user):
    # Добавление пользователя в черный список
    try:
        new_user = BlackList(
            vk_id=vk_id,
            first_name=first_name,
            second_name=second_name,
            city=city,
            link=link,
            id_user=id_user
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id,
                  'Пользователь успешно заблокирован.')
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id,
                  'Пользователь уже в черном списке.')
        return False


def add_to_searcht(event_id, vk_id,
                   first_name, second_name,
                   city, link, link_photo,
                   count_likes, id_user):
    try:
        new_user = Searches(
            vk_id=vk_id,
            first_name=first_name,
            second_name=second_name,
            city=city,
            link=link,
            link_photo=link_photo,
            count_likes=count_likes,
            id_user=id_user
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id,
                  'Пользователь успешно заблокирован.')
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id,
                  'Пользователь уже в черном списке.')
        return False
