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



if __name__ == '__main__':
    Base.metadata.create_all(engine)
