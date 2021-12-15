import vk_api, json
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# class Keyboards:
#     @staticmethod
#     def show_default():
#         keyboard = VkKeyboard(one_time=False)
#         keyboard.add_button('Поиск', color=VkKeyboardColor.PRIMARY)
#         keyboard.add_button('Картинка', color=VkKeyboardColor.PRIMARY)
#         keyboard.add_line()
#         keyboard.add_button('Спрячь клавиатуру', color=VkKeyboardColor.POSITIVE)
#         keyboard.add_line()
#         keyboard.add_openlink_button('RICKROLL', link='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
#         return keyboard.get_keyboard()
#
#     @staticmethod
#     def hide():
#         return VkKeyboard.get_empty_keyboard()








from enum import Enum
# class Keyboards:
#     @staticmethod
#     def show_default():
#         keyboard = VkKeyboard(one_time=False)
#         keyboard.add_button('Поиск', color=VkKeyboardColor.PRIMARY)
#         keyboard.add_line()
#         keyboard.add_button('Спрячь клавиатуру', color=VkKeyboardColor.POSITIVE)
#         keyboard.add_line()
#         return keyboard.get_keyboard()
#
#     @staticmethod
#     def hide():
#         return VkKeyboard.get_empty_keyboard()
#
#
#
#
#
# class Commands(Enum):
#     start = ('начать', 'привет', 'здравствуй', 'здоров', 'старт', 'погнали', 'hi')
#     show_keyboard = ('меню', 'menu', 'клавиатура', 'keyboard', 'клавиши', 'покажи меню', 'покажи клавиатуру')
#     hide_keyboard = ('убрать меню', 'убрать клавиатуру', 'спрячь меню', 'спрячь клавиатуру', 'скрыть клавиатуру')
#     search = ('искать', 'поиск', 'фас', 'ищи', 'найди')
#     picture = ('фото', 'картинка', 'мем', 'фоточка', 'изображение')
#     # bye = ('пока', 'досвидания', 'bye-bye', 'good bye', 'пока-пока', 'bye')

#
#
#
#
#
#
#
#
#
# import vk_api, json
# from vk_api.longpoll import VkLongPoll, VkEventType
# from vk_api.keyboard import VkKeyboard, VkKeyboardColor
# from VK_token import group_token
#
# vk_session = vk_api.VkApi(token=group_token)
# vk = vk_session.get_api()
# longpol = VkLongPoll(vk_session)
#
#
def get_but(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


keyboards = {
    "one_time": True,
    "buttons": [
        [get_but('начать поиск', 'positive'), get_but('посмотреть избранное', 'positive')],
        [get_but('посмотреть заблокированых', 'positive'), get_but('поиграть', 'positive')]
    ]
}
keyboards = json.dumps(keyboards, ensure_ascii=False).encode('utf-8')
keyboards = str(keyboards.decode('utf-8'))

#
# def sender(id, text):
#     vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0, 'keyboard': keyboard})
#
#
# def main():
#     for event in longpol.listen():
#         if event.type == VkEventType.MESSAGE_NEW:
#             if event.to_me:
#                 id = event.user_id
#                 msg = event.text.lower()
#
#                 sender(id, msg.upper())
#
#
# # while True:
#     # main()



import vk_api, json
# from vk_api.longpoll import VkLongPoll, VkEventType


# vk_session = vk_api.VkApi(token = tok)
# longpoll = VkLongPoll(vk_session)

# class User:
# 	def __init__(self, id):
# 		self.id = id
# 		self.mode = 'start'
# 		self.money = 1000000
# 		self.stone = 0
# 		self.wood = 0

# def sender(id, text, key):
# 	vk_session.method('messages.send', {'user_id' : id, 'message' : text, 'random_id' : 0, 'keyboard' : key})

def get_keyboard(buts):
    nb = []
    for i in range(len(buts)):
        nb.append([])
        for k in range(len(buts[i])):
            nb[i].append(None)
            for i in range(len(buts)):
                for k in range(len(buts[i])):
                    text = buts[i][k][0]
                    color = {'зеленый' : 'positive', 'красный' : 'negative', 'синий' : 'primary'}[buts[i][k][1]]
                    nb[i][k] = {"action": {"type": "text", "payload": "{\"button\": \"" + "1" + "\"}", "label": f"{text}"}, "color": f"{color}"}
                    first_keyboard = {'one_time': True, 'buttons': nb, 'inline' : False}
                    first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode('utf-8')
                    first_keyboard = str(first_keyboard.decode('utf-8'))
                    return first_keyboard

clear_key = get_keyboard([])

menu_key = get_keyboard([
	[('Магазин', 'зеленый')],
	[('Ресурсы', 'синий')]
])

shop_key = get_keyboard([
	[('Дерево', 'синий'), ('Камень', 'синий')],
	[('Назад', 'красный')]
])

back_key = get_keyboard([
	[('Назад', 'красный')]
])

# users = []

# for event in longpoll.listen():
# 	if event.type == VkEventType.MESSAGE_NEW:
# 		if event.to_me:
#
# 			id = event.user_id
# 			msg = event.text.lower()
#
# 			if msg == 'начать':
# 				flag = 0
# 				for user in users:
# 					if user.id == id:
# 						sender(id, 'Выберите действие:', menu_key)
# 						flag = 1
# 						break
# 				if flag == 0:
# 					users.append(User(id))
# 					sender(id, 'Выберите действие:', menu_key)
#
# 			else:
# 				for user in users:
# 					if user.id == id:
#
# 						if user.mode == 'start':
# 							if msg == 'магазин':
# 								sender(id, 'Выберите, что хотите купить:', shop_key)
# 								user.mode = 'shop'
#
# 							elif msg == 'ресурсы':
# 								sender(id, f'Ваши монеты: {user.money}\nВаше дерево: {user.wood}\nВаш камень: {user.stone}', menu_key)
#
# 						elif user.mode == 'shop':
# 							if msg == 'назад':
# 								sender(id, 'Выберите действие:', menu_key)
# 								user.mode = 'start'
#
# 							elif msg == 'дерево':
# 								sender(id, 'Сколько дерева вы хотите купить?:\nЦена за единицу дерева: 50 монет', back_key)
# 								user.mode = 'get_wood_count'
#
# 							elif msg == 'камень':
# 								sender(id, 'Сколько камня вы хотите купить?:\nЦена за единицу камня: 100 монет', back_key)
# 								user.mode = 'get_stone_count'
#
# 						elif user.mode == 'get_wood_count':
# 							if msg == 'назад':
# 								sender(id, 'Выберите действие:', menu_key)
# 								user.mode = 'start'
# 							else:
# 								try:
# 									col = int(msg)
# 									if user.money >= col*50:
# 										user.money -= col*50
# 										user.wood += col
# 										sender(id, f'Вы успешно совершили покупку {col} единиц дерева!', shop_key)
# 										user.mode = 'shop'
# 									else:
# 										sender(id, 'У вас не хватает монет!', shop_key)
# 										user.mode = 'shop'
# 								except Exception as e:
# 									sender(id, 'Неверно введены данные!', shop_key)
# 									user.mode = 'shop'
#
# 						elif user.mode == 'get_stone_count':
# 							if msg == 'назад':
# 								sender(id, 'Выберите действие:', menu_key)
# 								user.mode = 'start'
# 							else:
# 								try:
# 									col = int(msg)
# 									if user.money >= col*100:
# 										user.money -= col*100
# 										user.stone += col
# 										sender(id, f'Вы успешно совершили покупку {col} единиц камня!', shop_key)
# 										user.mode = 'shop'
# 									else:
# 										sender(id, 'У вас не хватает монет!', shop_key)
# 										user.mode = 'shop'
# 								except Exception as e:
# 									sender(id, 'Неверно введены данные!', shop_key)
# 									user.mode = 'shop'


