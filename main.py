from pymongo import MongoClient
import telebot
import re
from config import TOKEN, user_info
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

bot = telebot.TeleBot(TOKEN)
cluster = MongoClient('mongodb+srv://sdovi:820722zz@cluster0.t5d9hdm.mongodb.net/DB?retryWrites=true&w=majority')
db = cluster['DB']
collection = db['Info']
text_btn = {
    'btn1': KeyboardButton(text='Uzbekcha🇺🇿'),
    'btn2': KeyboardButton(text='Русский🇷🇺'),
    'btn3': KeyboardButton(text='Отправить номер', request_contact=True),
    # не получается разделить по файлам, у меня логика не включается
    'btn4': KeyboardButton(text='Raqamni yuboring', request_contact=True),
}


@bot.message_handler(commands=["start"])
def start(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(text_btn['btn1'], text_btn['btn2'])
    bot.send_message(message.chat.id, 'Выберите язык', reply_markup=kb)
    user_info["_id"] = message.chat.id


@bot.message_handler(content_types=['text'])
def language(message):
    if message.text == 'Русский🇷🇺':
        user_info["language"] = 2
        from Languare_RU import text01
        global text01
        bot.send_message(message.chat.id, text01['national'], reply_markup=ReplyKeyboardRemove())
        Rulanguare = bot.send_message(message.chat.id, text01['national2'])  # Напишите свое имя
        bot.register_next_step_handler(Rulanguare, Rulan)
    elif message.text == 'Uzbekcha🇺🇿':
        user_info["language"] = 1
        from languare_UZ import text01
        bot.send_message(message.chat.id, text01['national'], reply_markup=ReplyKeyboardRemove())
        Rulanguare = bot.send_message(message.chat.id, text01['national2'])  # Напишите свое имя
        bot.register_next_step_handler(Rulanguare, uzlan)


def Rulan(message):
    kn = ReplyKeyboardMarkup(resize_keyboard=True)  # принимает имя
    kn.add(text_btn['btn3'])
    user_info['name'] = message.text
    bot.send_message(message.chat.id, text01['name'])  # Напишите свой номер
    nomer = bot.send_message(message.chat.id, text01['name2'], reply_markup=kn)
    bot.register_next_step_handler(nomer, runomer)


def runomer(message):
    if message.content_type == 'contact':
        user_info['number'] = int(message.contact.phone_number)  # принимает номер
        bot.send_message(message.chat.id, text01['phone'])
        email = bot.send_message(message.chat.id, text01['phone2'])  # отправьте свой емаил
        bot.register_next_step_handler(email, ruemail)
    elif len(message.text) == 12 and re.match(r'^(998)[\d]{9}$', message.text):
        user_info['number'] = message.text  # принимает номер
        bot.send_message(message.chat.id, text01['phone'])
        email = bot.send_message(message.chat.id, text01['phone2'])  # отправьте свой емаил
        bot.register_next_step_handler(email, ruemail)
    else:
        bot.send_message(message.chat.id, text01['name3'])


def ruemail(message):
    user_info['gmail'] = message.text  # принимает емаил
    bot.send_message(message.chat.id, text01['email'])
    photo = bot.send_message(message.chat.id, text01['email2'])  # отправьте свое фото
    bot.register_next_step_handler(photo, ruphoto)


def ruphoto(message):
    bot.send_message(message.chat.id, 'Успешно👍')  # конец
    collection.insert_one(user_info)


def uzlan(message):
    kn = ReplyKeyboardMarkup(resize_keyboard=True)
    kn.add(text_btn['btn4'])
    user_info['name'] = message.text
    bot.send_message(message.chat.id, text01['name'])  # Напишите свой номер
    nomer = bot.send_message(message.chat.id, text01['name2'], reply_markup=kn)
    bot.register_next_step_handler(nomer, uznomer)


def uznomer(message):
    if message.content_type == 'contact':
        user_info['number'] = int(message.contact.phone_number)
        bot.send_message(message.chat.id, text01['phone'])
        email = bot.send_message(message.chat.id, text01['phone2'])  # отправьте свой емаил
        bot.register_next_step_handler(email, uzemail)
    elif len(message.text) == 12 and re.match(r'^(998)[\d]{9}$', message.text):
        user_info['number'] = message.text
        bot.send_message(message.chat.id, text01['phone'])
        email = bot.send_message(message.chat.id, text01['phone2'])  # отправьте свой емаил
        bot.register_next_step_handler(email, uzemail)
    else:
        bot.send_message(message.chat.id, text01['name3'])


def uzemail(message):
    user_info['gmail'] = message.text
    bot.send_message(message.chat.id, text01['email'])
    photo = bot.send_message(message.chat.id, text01['email2'])  # отправьте свое фото
    bot.register_next_step_handler(photo, uzphoto)


def uzphoto(message):
    bot.send_message(message.chat.id, 'Успешно👍')
    collection.insert_one(user_info)


bot.infinity_polling()
