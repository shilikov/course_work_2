import pytest
from data_search.data_search import Users, Photo
from data_base.db_func import register_user, add_user,\
    add_user_photos, add_to_black_list


class TestVkinder:

    def setup_class(self):
        print('method setup_class')

    def setup(self):
        print('method setup')

    def teardown(self):
        print('method teardown')

    # Тесты по работе приложения
    # Проверка поиска анкет
    @pytest.mark.parametrize('sex, age_from, age_to, hometown, result', [
        (1, 18, 20, 'москва', None)])
    def test_search_users(self, sex, age_from, age_to, hometown, result):
        user = Users(sex, age_from, age_to, hometown)
        assert user.search_users() == result

    # Тест поиска фотографий
    @pytest.mark.parametrize('user_id, result', [('688986469', str)])
    def test_get_photo(self, user_id, result):
        photo = Photo(user_id)
        assert photo.get_photo() == result

    # Тест сортировки по лайкам
    @pytest.mark.parametrize('list_photos, result',
                             [(['1',
                                'photo_1',
                                '2', 'photo_2',
                                '3',
                                'photo_3'],
                               ['1',
                                '2',
                                '3',
                                'photo_1',
                                'photo_2',
                                'photo_3']), ])
    def test_sort_likes(self, list_photos, result):
        photo = Photo(list_photos)
        assert photo.sort_likes(list_photos) == result

    # Тест первичной регистрации юзера
    @pytest.mark.parametrize('vk_id, result', [('1', False),
                                               ('1', False),
                                               ('336261034', False)])
    def test_register_user(self, vk_id, result):
        assert register_user(vk_id) == result

    # Тест добавление пользователя
    @pytest.mark.parametrize('event_id, vk_id, '
                             'first_name, second_name, '
                             'city, link, id_user, result',
                             [('7717001', '2', 'goga',
                               'boba', 'Turkey',
                               'www.vkman.ru', '1', False)])
    def test_add_user(self, event_id, vk_id,
                      first_name, second_name,
                      city, link, id_user, result):
        assert add_user(event_id, vk_id,
                        first_name, second_name,
                        city, link, id_user) == result

    # Тест добавление фото анкеты в БД
    @pytest.mark.parametrize('event_id, link_photo, '
                             'count_likes, '
                             'id_dating_user, '
                             'result',
                             [('123', 'link_link',
                               '2', '33502052', False)])
    def test_add_user_photos(self, event_id,
                             link_photo, count_likes,
                             id_dating_user, result):
        assert add_user_photos(event_id, link_photo,
                               count_likes, id_dating_user) == result

    # Добавление в черный список
    @pytest.mark.parametrize(
        'event_id, vk_id, first_name, '
        'second_name, city, link, link_photo, '
        'count_likes, id_user, result',
        [('123', '12', '12434',
          '1251231', 'sdfsdfs', 'sfsdfsdfds',
          'fsdfsdfs', '12', '123', False)])
    def test_add_user_to_black_list(self, event_id, vk_id,
                                    first_name, second_name,
                                    city, link, link_photo,
                                    count_likes,
                                    id_user, result):
        assert add_to_black_list(event_id, vk_id,
                                 first_name, second_name,
                                 city, link, link_photo,
                                 count_likes,
                                 id_user) == result

    def teardown_class(self):
        print('method teardown_class')
