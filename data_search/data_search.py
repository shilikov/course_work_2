import vk_api
from vk_api.longpoll import VkLongPoll
from VK_token import VK_api_V, user_token, group_token, group_id
from vk_api.exceptions import ApiError
from logers.logers import log_to_console
from vk_api.bot_longpoll import VkBotLongPoll
from datetime import date
# import collections
# from vk_api.audio import VkAudio


class Api_connect:
    def __init__(self):
        self.token = user_token
        self.vk = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(vk=self.vk)

    def user_info(self, user_id):
        user_search_dict = {}
        vk_ = vk_api.VkApi(token=user_token)
        user = vk_.method('users.get', {'user_id': user_id,
                                        'fields': ['relation, '
                                                   'sex, '
                                                   'hometown, '
                                                   'bdate']})
        user = user[0]
        # user_search_dict.fromkeys(['hometown']) = user['hometown']
        # user_search_dict['sex'] = user['sex']
        # user_search_dict['status'] = '1'
        # user_search_dict['age_from'] = age_from_to_list[0]
        # user_search_dict['age_to'] = age_from_to_list[1]
        print(user_search_dict)


class Users:
    def __init__(self, sex, age_from, age_to, hometown):
        self.age_from = age_from
        self.age_to = age_to
        self.sex = sex
        self.hometown = hometown

    @log_to_console
    def search_users(self):
        all_user = []
        profile = 'https://vk.com/id'
        vk_ = vk_api.VkApi(token=user_token)
        response = vk_.method('users.search',
                              {
                                  'sort': 1,
                                  'count': 20,
                                  'sex': self.sex,
                                  'hometown': self.hometown,
                                  'status': 1,
                                  'age_from': self.age_from,
                                  'age_to': self.age_to,
                                  'online': 1,
                                  'fields': ['interests, '
                                             'music, '
                                             'movies, '
                                             'tv, '
                                             'books, '
                                             'games, '
                                             'sex, '
                                             'status']})

        for element in response['items']:
            person = [
                element['first_name'],
                element['last_name'],
                profile + str(element['id']),
                element['id']
            ]
            s = ['first_name', 'last_name', 'profile', 'id']
            p = dict(zip(s, person))
            all_user.append(p)
        return all_user


    # @log_to_console
class Photo:
    def __init__(self, user_owner_id):
        self.user_owner_id = user_owner_id

    # @classmethod
    def get_photo(self):
        vk_ = vk_api.VkApi(token=user_token)
        try:
            response = vk_.method('photos.get',
                                  {
                                      'access_token': user_token,
                                      'v': VK_api_V,
                                      'owner_id': self.user_owner_id,
                                      'album_id': 'profile',
                                      'count': 10,
                                      'extended': 1,
                                      'photo_sizes': 1,
                                  })
        except ApiError:
            return 'нет доступа к фото'
        users_photos = []
        for i in range(10):
            try:
                users_photos.append(
                    [response['items'][i]['likes']['count'],
                     'photo' + str(response['items'][i]['owner_id']) +
                     '_' + str(response['items'][i]['id'])])
            except IndexError:
                users_photos.append(['нет фото.'])
        return users_photos

    def likes_add(self, owner_id):
        ...

    def sort_likes(self, photos):
        result = []
        for element in photos:
            if element != ['нет фото.'] and photos != 'нет доступа к фото':
                result.append(element)
        return sorted(result)


class Music:
    def __init__(self):
        ...


class Cities:

    def __init__(self):
        res = []
        vk_ = vk_api.VkApi(token=user_token)
        response = vk_.method('database.getCities', {
            'country_id': 1,
            'need_all': 0,
            'count': 100})

        print(response)
        res.append(response['items'])

        for i in res:
            for x in i:
                print('Москва' in x['title'])


class Client:
    def __init__(self, user_id):
        self.user_id = user_id

    def user_data(self):
        self.vk_session = vk_api.VkApi(token=group_token)
        self.longpoll = VkBotLongPoll(self.vk_session, group_id)
        self.session_api = self.vk_session.get_api()
        self.members_list = self.vk_session.method(
            'messages.getConversationMembers', {
                'peer_id': self.user_id, 'fields': ['city']})

        self.city = self.members_list['profiles'][0]['city']['title']
        self.members_list = self.vk_session.method(
            'messages.getConversationMembers', {
                'peer_id': self.user_id, 'fields': ['bdate']})
        birth_date = self.members_list['profiles'][0]['bdate'].split('.')
        today = date.today()
        self.age = today.year - int(birth_date[2])
        self.name = self.members_list['profiles'][0]['first_name']
        # print(self.name)

        return self.city, self.age, self.name

    # def music(self):
    #     """ Пример составления топа исполнителей для профиля вк """
    #
    #     try:
    #         self.vk_session.auth()
    #     except vk_api.AuthError as error_msg:
    #         print(error_msg)
    #         return
    #
    #     vkaudio = VkAudio(self.vk_session)
    #
    #     artists = collections.Counter(
    #         track['artist'] for track in vkaudio.get_iter()
    #     )
    #
    #     # Составляем рейтинг первых 15
    #     print('Top 15:')
    #     for artist, tracks in artists.most_common(15):
    #         print('{} - {} tracks'.format(artist, tracks))
    #
    #     # Ищем треки самого популярного
    #     most_common_artist = artists.most_common(1)[0][0]
    #
    #     print('\nSearching for {}:'.format(most_common_artist))
    #
    #     tracks = vkaudio.search(q=most_common_artist, count=10)
    #
    #     for n, track in enumerate(tracks, 1):
    #         print('{}. {} {}'.format(n, track['title'], track['url']))
    #
    # def albumi(self):
    #     """ Пример отображения 5 последних альбомов пользователя """
    #     try:
    #         self.vk_session.auth()
    #     except vk_api.AuthError as error_msg:
    #         print(error_msg)
    #         return
    #
    #     vkaudio = VkAudio(self.vk_session)
    #
    #     albums = vkaudio.get_albums(194957739)
    #
    #     print('\nLast 5:')
    #     for album in albums[:5]:
    #         print(album['title'])
    #
    #     # Ищем треки последнего альбома
    #     print('\nSearch for', albums[0]['title'])
    #     tracks = vkaudio.get(album_id=albums[0]['id'])
    #
    #     for n, track in enumerate(tracks, 1):
    #         print('{}. {} {}'.format(n, track['title'], track['url']))


# if __name__ == "__main__":
#
#     # slient = Client(683858243)
#     # print(slient.albumi())
#     # return sorted(response['items'])
#
#     # api = Api_connect()
#     # api.user_info(686541705)
#     # sity = Cities()
#
#     user = Users(1, 18, 20, 'москва')
#     user.search_users()


# photo = Photo(686541705)
# print(photo.get_photo())
