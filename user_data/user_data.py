
import vk_api
from VK_token import group_token, group_id
from vk_api.bot_longpoll import VkBotLongPoll
from datetime import date


class SelfUser:

    def __init__(self):
        self.vk_session = vk_api.VkApi(token=group_token)
        self.longpoll = VkBotLongPoll(self.vk_session, group_id)
        self.session_api = self.vk_session.get_api()
        self.members_list = None
        self.first_name = None
        self.last_name = None
        self.country = None
        self.city = None
        self.sex = None
        self.age = None
        self.id = None

    def user_lastname(self, user_id):
        self.id = user_id
        self.members_list = self.vk_session.method(
            'messages.getConversationMembers', {
                'peer_id': self.id})
        self.last_name = self.members_list['profiles'][0]['last_name']
        return self.last_name

    def user_first_name(self, user_id):
        self.id = user_id
        self.members_list = self.vk_session.method(
            'messages.getConversationMembers', {
                'peer_id': self.id})
        self.first_name = self.members_list['profiles'][0]['first_name']
        return self.first_name

    def user_bdate(self, user_id):
        self.id = user_id
        self.members_list = self.vk_session.method(
            'messages.getConversationMembers', {
                'peer_id': self.id, 'fields': ['bdate']})
        birth_date = self.members_list['profiles'][0]['bdate'].split('.')
        today = date.today()
        self.age = today.year - int(birth_date[2])
        return self.age

    def user_city(self, user_id):
        self.id = user_id
        self.members_list = self.vk_session.method(
            'messages.getConversationMembers', {
                'peer_id': self.id, 'fields': 'city'})

        self.city = self.members_list['profiles'][0]['city']['title']
        return self.city

    def user_info(self, user_id):
        user = self.vk_session.method('users.get', {'user_id': user_id,
                                                    'fields': 'relation, '
                                                              'sex, '
                                                              'hometown, '
                                                              'bdate'})
        return user
