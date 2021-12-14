import vk_api
from vk_api.longpoll import VkLongPoll
from VK_token import VK_api_V, user_token, group_token
from vk_api.exceptions import ApiError
from logers.logers import log_to_console



class Api_connect:
    def __init__(self):
        self.token = group_token
        self.vk = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(vk=self.vk)



class Users:
    def __init__(self,sex, age_from, age_to, hometown):
        self.age_from = age_from
        self.age_to = age_to
        self.sex = sex
        self.hometown = hometown

    @log_to_console
    def search_users(self):
        all_user = []
        profile = 'https://vk.com/id'
        vk_= vk_api.VkApi(token=user_token)
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
                                'fields': ['interests, music, movies, tv, books, games, sex, status']
                            })


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

@log_to_console
class Photo:
    def __init__(self, user_owner_id):
        self.user_owner_id = user_owner_id
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
                     'photo' + str(response['items'][i]['owner_id']) + '_' + str(response['items'][i]['id'])])
            except IndexError:
                users_photos.append(['нет фото.'])
        return users_photos


    def likes_add(self, owner_id):
        vk_ = vk_api.VkApi(token=user_token)
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





Api_connect()
# user = Users(1, 18, 20, 'москва')
# print(user.search_users())
# photo = Photo(686541705)
# print(photo.get_photo())

























# Для работы с вк_апи
# vk = vk_api.VkApi(token=group_token)
# longpoll = VkLongPoll(vk)



# def search_users(age_from, age_to, sex, city):
#     all_persons = []
#     profile = 'https://vk.com/id'
#     vk_= vk_api.VkApi(token=user_token)
#     response = vk_.method('users.search',
#                           {'sort':1,
#                            'count':20,
#                            'age_from':age_from,
#                            'age_to':age_to,
#                            'sex':sex,
#                            'has_photo':1,
#                            'hometown':city,
#                            'status':1,
#                            'online': 1})
#     for element in response['items']:
#         person = [
#             element['first_name'],
#             element['last_name'],
#             profile + str(element['id']),
#             element['id']
#         ]
#         all_persons.append(person)
#     return all_persons







# user_photo = []

# def photo_get(owner_id):
#     # user_photo = []
#     vk_= vk_api.VkApi(token=user_token)
#     try:
#         response = vk_.method('photos.get',
#                               {'extended': 1,
#                                'owner_id': owner_id,
#                                'album_id': 'profile',
#                                'photo_sizes': 1,
#                                'count': 20
#                                })
#     except ApiError:
#         return f'This profile is private - нет доступа к фото'
#
#
#     for i in response['items']:
#             user_photo.append([i['likes']['count'],
#                                'photo' + str(i['owner_id']) + '_' + str(i['id'])])
#     return sorted(user_photo)


























#
# def main():
#     """ Пример отображения 5 последних альбомов пользователя """
#
#     login, password = 'login', 'password'
#     vk_session = vk_api.VkApi(token=user_token)
#
#     try:
#         vk_session.auth()
#     except vk_api.AuthError as error_msg:
#         print(error_msg)
#         return
#
#     vkaudio = VkAudio(vk_session)
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



    # main()


# def json_create(lst):
#     today = datetime.date.today()
#     today_str = f'{today.day}.{today.month}.{today.year}'
#     res = {}
#     res_list = []
#     for num, info in enumerate(lst):
#         res['data'] = today_str
#         res['first_name'] = info[0]
#         res['second_name'] = info[1]
#         res['link'] = info[2]
#         res['id'] = info[3]
#         res_list.append(res.copy())
#
#     with open(result.json", "a", encoding='UTF-8') as write_file:
#         json.dump(res_list, write_file, ensure_ascii=False)
#
#     print(f'Информация о загруженных файлах успешно записана в json файл.')














# search_users(1, 'москва', 25, 35)
# photo_get(633463935)
# photo_get(687346003)
# print(photo_get(691145507))






