import vk_api
from vk_api.longpoll import VkLongPoll
from VK_token import VK_api_V, user_token
from vk_api.exceptions import ApiError
from logers.logers import log_to_console


class Api_connect:

    def __init__(self):
        self.token = user_token
        self.vk = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(vk=self.vk)
        self.vk_ = self.vk.get_api()

    def _get_user_name(self, user_id):
        return self.vk_.users.get(user_id=user_id)[0].get('first_name')


class Users:
    def __init__(self, sex, age_from, age_to, hometown):
        self.age_from = age_from
        self.age_to = age_to
        self.sex = sex
        self.hometown = hometown

    @property
    def params(self):
        return {
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
                       'status']}

    @property
    def params_get_foto(self):
        return {
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
                       'status']}

    @log_to_console
    def search_users(self):
        all_user = []
        profile = 'https://vk.com/id'
        vk_ = vk_api.VkApi(token=user_token)
        response = vk_.method('users.search',
                              self.params)

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
        # print(None if len(response['items']) < 1 else response['items'])
        return None if len(response['items']) < 1 else all_user


class Photo:
    def __init__(self, user_owner_id):
        self.user_owner_id = user_owner_id

    # @classmethod
    @property
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
