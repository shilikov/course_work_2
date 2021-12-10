import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from VK_token import group_token
from random import randrange
import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, func
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from keyboards.keyboards import *
from sqlalchemy.orm import relationship
from data_search.const import RATINGS

from vk_api.keyboard import VkKeyboard


# Подключение к БД
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


# Пользователь бота ВК
#
# class Users(Base):
#     __tablename__ = 'users'
#     id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
#     vk_id = sq.Column(sq.String(20), unique=True, nullable=False)
#     fname = sq.Column(sq.String(300), nullable=False)
#     lname = sq.Column(sq.String(300))
#     domain = sq.Column(sq.String(50))
#     country_id = sq.Column(sq.Integer)
#     country_name = sq.Column(sq.String(100))
#     city_id = sq.Column(sq.Integer)
#     city_name = sq.Column(sq.String(200))
#     hometown = sq.Column(sq.String(300))
#     birth_date = sq.Column(sq.TIMESTAMP(timezone=True))
#     birth_day = sq.Column(sq.Integer)
#     birth_month = sq.Column(sq.Integer)
#     birth_year = sq.Column(sq.Integer)
#     sex_id = sq.Column(sq.Integer)
#     updated = sq.Column(sq.TIMESTAMP(timezone=True), default=func.now())
#     raters = relationship('Clients', secondary='clients_users')
#     searches = relationship('Searches', secondary='searches_users')

    # def convert_to_ApiUser(self, rating_id=RATINGS['new']) -> ApiUser:
    #     """
    #     Needed when we restore from DB previously saved users
    #     """
    #     bdate = [str(self.birth_day) if self.birth_day is not None else '',
    #              str(self.birth_month) if self.birth_month is not None else '',
    #              str(self.birth_year) if self.birth_year is not None else '']
    #     row = {'id': self.vk_id,
    #            'first_name': self.fname,
    #            'last_name': self.lname,
    #            'sex': self.sex_id,
    #            'country': {
    #                'id': self.country_id,
    #                'title': self.country_name
    #            },
    #            'last_seen': {
    #                'time': None,
    #            },
    #            'domain': self.domain,
    #            'bdate': '.'.join(bdate),
    #            }
    #     return ApiUser(row, rating_id=rating_id)

class User(Base):
    __tablename__ = 'user'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)








# Анкеты добавленные в избранное
class DatingUser(Base):
    __tablename__ = 'dating_user'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String)
    second_name = sq.Column(sq.String)
    city = sq.Column(sq.String)
    link = sq.Column(sq.String)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))


# Фото избранных анкет
class Photos(Base):
    __tablename__ = 'photos'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    link_photo = sq.Column(sq.String)
    count_likes = sq.Column(sq.Integer)
    id_dating_user = sq.Column(sq.Integer, sq.ForeignKey('dating_user.id', ondelete='CASCADE'))


# Анкеты в черном списке
class BlackList(Base):
    __tablename__ = 'black_list'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String)
    second_name = sq.Column(sq.String)
    city = sq.Column(sq.String)
    link = sq.Column(sq.String)
    link_photo = sq.Column(sq.String)
    count_likes = sq.Column(sq.Integer)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))

#
class Searches(Base):
    __tablename__ = 'searches'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String)
    second_name = sq.Column(sq.String)
    city = sq.Column(sq.String)
    link = sq.Column(sq.String)
    link_photo = sq.Column(sq.String)
    count_likes = sq.Column(sq.Integer)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))

# class SearchesUsers(Base):
#     __tablename__ = 'searches_users'
#     __table_args__ = (PrimaryKeyConstraint('search_id', 'user_id'),)
#     search_id = sq.Column(sq.Integer, ForeignKey('searches.id', ondelete='CASCADE'), nullable=False)
#     user_id = sq.Column(sq.Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)







# class Clients(Base):
#     __tablename__ = 'clients'
#     id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
#     vk_id = sq.Column(sq.String(20), unique=True, nullable=False)
#     fname = sq.Column(sq.String(300), nullable=False)
#     lname = sq.Column(sq.String(300))
#     domain = sq.Column(sq.String(50))
#     country_id = sq.Column(sq.Integer)
#     country_name = sq.Column(sq.String(100))
#     city_id = sq.Column(sq.Integer)
#     city_name = sq.Column(sq.String(200))
#     hometown = sq.Column(sq.String(300))
#     birth_date = sq.Column(sq.TIMESTAMP(timezone=True))
#     birth_day = sq.Column(sq.Integer)
#     birth_month = sq.Column(sq.Integer)
#     birth_year = sq.Column(sq.Integer)
#     sex_id = sq.Column(sq.Integer)
#     updated = sq.Column(sq.TIMESTAMP(timezone=True), default=func.now())
#     rated_users = relationship('Users', secondary='clients_users')
#     tagged_photos = relationship('Photos', secondary='clients_userphotos')
#
#     def convert_to_ApiUser(self, rating_id=RATINGS['new']) -> ApiUser:
#         """
#         Needed when we restore from DB previously saved users
#         """
#         bdate = [str(self.birth_day) if self.birth_day is not None else '',
#                  str(self.birth_month) if self.birth_month is not None else '',
#                  str(self.birth_year) if self.birth_year is not None else '']
#         row = {'id': self.vk_id,
#                'first_name': self.fname,
#                'last_name': self.lname,
#                'sex': self.sex_id,
#                'country': {
#                    'id': self.country_id,
#                    'title': self.country_name
#                },
#                'last_seen': {
#                    'time': None,
#                },
#                'domain': self.domain,
#                'bdate': '.'.join(bdate),
#                }
#         return ApiUser(row, rating_id=rating_id)





# class ClientsUsers(Base):
#     __tablename__ = 'clients_users'
#     __table_args__ = (PrimaryKeyConstraint('client_id', 'user_id'),)
#     client_id = sq.Column(sq.Integer, ForeignKey('clients.id', ondelete='CASCADE'))
#     user_id = sq.Column(sq.Integer, ForeignKey('users.id', ondelete='CASCADE'))
#     rating_id = sq.Column(sq.Integer)
#     updated = sq.Column(sq.TIMESTAMP(timezone=True), default=func.now())
#
#     def __init__(self, client_id=None, user_id=None, rating_id=None, updated=func.now()):
#         self.client_id = client_id
#         self.user_id = user_id
#         self.rating_id = rating_id
#         self.updated = updated
#
#
# class Photos(Base):
#     __tablename__ = 'photos'
#     id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
#     url = sq.Column(sq.String(2048))
#     likes_count = sq.Column(sq.Integer)
#     comments_count = sq.Column(sq.Integer)
#     reposts_count = sq.Column(sq.Integer)
#     photo_id = sq.Column(sq.String(20), nullable=False)
#     owner_id = sq.Column(sq.Integer, ForeignKey('users.id'), nullable=False)
#     updated = sq.Column(sq.TIMESTAMP(timezone=True), default=func.now())
#     tagged_clients = relationship('Clients', secondary='clients_userphotos')
#
#     def __init__(self, url=None, likes_count=None, comments_count=None, photo_id=None, owner_db_id=None,
#                  reposts_count=None, updated=func.now()):
#         self.url = url
#         self.likes_count = likes_count
#         self.comments_count = comments_count
#         self.reposts_count = reposts_count
#         self.photo_id = photo_id
#         self.owner_id = owner_db_id
#         self.updated = updated
#
#
# class ClientsUserPhotos(Base):
#     __tablename__ = 'clients_userphotos'
#     __table_args__ = (PrimaryKeyConstraint('client_id', 'photo_id'),)
#     client_id = sq.Column(sq.Integer, ForeignKey('clients.id', ondelete='CASCADE'))
#     photo_id = sq.Column(sq.Integer, ForeignKey('photos.id', ondelete='CASCADE'))
#
#
# class Searches(Base):
#     __tablename__ = 'searches'
#     id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
#     client_id = sq.Column(sq.Integer, ForeignKey('clients.id'), nullable=False)
#     min_age = sq.Column(sq.Integer)
#     max_age = sq.Column(sq.Integer)
#     sex_id = sq.Column(sq.Integer)
#     status_id = sq.Column(sq.Integer)
#     city_id = sq.Column(sq.Integer)
#     city_name = sq.Column(sq.String(100))
#     updated = sq.Column(sq.TIMESTAMP(timezone=True), default=func.now())
#     found_users = relationship('Users', secondary='searches_users')
#
#
# class SearchesUsers(Base):
#     __tablename__ = 'searches_users'
#     __table_args__ = (PrimaryKeyConstraint('search_id', 'user_id'),)
#     search_id = sq.Column(sq.Integer, ForeignKey('searches.id', ondelete='CASCADE'), nullable=False)
#     user_id = sq.Column(sq.Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)















"""
ФУНКЦИИ РАБОТЫ С БД
"""


# Удаляет пользователя из черного списка
def delete_db_blacklist(ids):
    current_user = session.query(BlackList).filter_by(vk_id=ids).first()
    session.delete(current_user)
    session.commit()


# Удаляет пользователя из избранного
def delete_db_favorites(ids):
    current_user = session.query(DatingUser).filter_by(vk_id=ids).first()
    session.delete(current_user)
    session.commit()


# проверят зареган ли пользователь бота в БД
def check_db_master(ids):
    current_user_id = session.query(User).filter_by(vk_id=ids).first()
    return current_user_id


# проверят есть ли юзер в бд
def check_db_user(ids):
    dating_user = session.query(DatingUser).filter_by(
        vk_id=ids).first()
    blocked_user = session.query(BlackList).filter_by(
        vk_id=ids).first()
    return dating_user, blocked_user


# Проверят есть ли юзер в черном списке
def check_db_black(ids):
    current_users_id = session.query(User).filter_by(vk_id=ids).first()
    # Находим все анкеты из избранного которые добавил данный юзер
    all_users = session.query(BlackList).filter_by(id_user=current_users_id.id).all()
    return all_users


# Проверяет есть ли юзер в избранном
def check_db_favorites(ids):
    current_users_id = session.query(User).filter_by(vk_id=ids).first()
    # Находим все анкеты из избранного которые добавил данный юзер
    alls_users = session.query(DatingUser).filter_by(id_user=current_users_id.id).all()
    return alls_users








# Пишет сообщение пользователю
def write_msg(user_id, message, attachment=None, keboard = None):
    vk.method('messages.send',
              {'user_id': user_id,
               'message': message,
               'random_id': randrange(10 ** 7),
               'attachment': attachment,
               'keboard': keboard})


# Регистрация пользователя
def register_user(vk_id):
    try:
        new_user = User(
            vk_id=vk_id
        )
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        return False


# Сохранение выбранного пользователя в БД
def add_user(event_id, vk_id, first_name, second_name, city, link, id_user):
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


# Сохранение в БД фото добавленного пользователя


def add_user_photos(event_id, link_photo, count_likes, id_dating_user):
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


# Добавление пользователя в черный список
def add_to_black_list(event_id, vk_id, first_name, second_name, city, link, link_photo, count_likes, id_user):
    try:
        new_user = BlackList(
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





def add_to_searcht(event_id, vk_id, first_name, second_name, city, link, link_photo, count_likes, id_user):
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


if __name__ == '__main__':
    Base.metadata.create_all(engine)
