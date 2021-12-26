from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from VK_token import group_token
import vk_api



def send_keyboard(user_id):
    vk_session = vk_api.VkApi(token=group_token)
    vk = vk_session.get_api()
    keyboard = keyboard1()
    vk.messages.send(
        peer_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message='Пример клавиатуры'
    )
    return vk





def keyboard3(user_id, vk):
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
        message='Выберите действие для кандидата'
    )


def keyboard2(user_id, vk):
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


def keyboard1():
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