import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
from config import token_api, group_id
bot = telebot.TeleBot(token_api)

user_info = {
    'name': 'asd',
    'phone_number': 0,
    'language': 'asd'
}

buttons = {
    'btn1': KeyboardButton(text='Узб'),
    'btn2': KeyboardButton(text='Рус'),
    'btn3': KeyboardButton(text='Записаться на консультацию'),
    'btn4': KeyboardButton(text='Записаться на вебинар'),
    'btn9': KeyboardButton(text='Отправить номер', request_contact=True),
    'btn10': InlineKeyboardButton(text="Отправить другу", switch_inline_query='/start'),

}
a = ReplyKeyboardRemove()


@bot.message_handler(commands=['start'])
def start(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(buttons['btn1'], buttons['btn2'])
    bot.send_photo(message.chat.id, open('foto1.jpg', 'rb'), 'Добро пожаловать в бот академии.')
    bot.send_message(message.chat.id, 'Выберите язык', reply_markup=kb)


@bot.message_handler(content_types=['text'])
def func_service(message):

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(buttons['btn3'], buttons['btn4'])

    if message.text == 'Узб':
        bot.send_message(message.chat.id, 'Выберите услугу', reply_markup=kb)
        user_info['language'] = 'Узб'

    elif message.text == 'Рус':
        bot.send_message(message.chat.id, 'Выберите услугу', reply_markup=kb)
        user_info['language'] = 'Рус'

    elif message.text == "Записаться на консультацию":
        bot.send_message(message.chat.id, 'Отлично, тогда начнем регистрацию!', reply_markup=a)
        user_name = bot.send_message(message.chat.id, "Отправьте свое имя:")
        bot.register_next_step_handler(user_name, name)

    elif message.text == "Записаться на вебинар":
        bot.send_photo(message.chat.id, open('foto1.jpg', 'rb'))
        bot.send_message(message.chat.id, "Выберите дату открытого урока")


def name(message):
    phone_btn = ReplyKeyboardMarkup(resize_keyboard=True)
    phone_btn.add(buttons['btn9'])
    user_phone = bot.send_message(message.chat.id, "Сейчас отправь свой номер телефона, пожалуйста. "
                                                   "Это можно сделать используя кнопку внизу, "
                                                   "либо отправить сообщение в формате 998XXXXXXXXX",
                                  reply_markup=phone_btn)
    bot.register_next_step_handler(user_phone, phone_number)
    user_info['name'] = message.text


def phone_number(message):
    if message.content_type == 'contact':
        markup = InlineKeyboardMarkup()
        markup.add(buttons['btn10'])
        bot.send_message(message.chat.id, "Супер, ты зареган! Наш менеджер с тобой скоро свяжется и напомнит о лекции!"
                                          " А сейчас подпишись на наш telegram канал"
                                          " 👉  https://www.instagram.com/itacademy_uz/", reply_markup=a)

        bot.send_message(message.chat.id, 'Вместе учиться всегда веселее! Приглашай друзей и получи скидку 5%',
                         reply_markup=markup)
        user_info['phone_number'] = int(message.contact.phone_number)
        list01 = list(user_info.values())
        bot.send_message(group_id, f"Имя: {list01[0]}\n"
                                   f"контакт: {list01[1]}\n"
                                   f"Язык: {list01[2]}")
    else:
        markup = InlineKeyboardMarkup()
        markup.add(buttons['btn10'])
        bot.send_message(message.chat.id, "Супер, ты зареган! Наш менеджер с тобой скоро свяжется и напомнит о лекции!"
                                          " А сейчас подпишись на наш telegram канал"
                                          " 👉  https://www.instagram.com/itacademy_uz/", reply_markup=a)

        bot.send_message(message.chat.id, 'Вместе учиться всегда веселее! Приглашай друзей и получи скидку 5%',
                         reply_markup=markup)
        user_info['phone_number'] = int(message.text)
        list01 = list(user_info.values())
        bot.send_message(group_id, f"Имя: {list01[0]}\n"
                                   f"контакт: {list01[1]}\n"
                                   f"Язык: {list01[2]}")