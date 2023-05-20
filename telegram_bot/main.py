"""Основной файл для запуска Телеграм бота
Содержит:
Основную логику программы;
Размещение кнопок в Телеграм боте(удобный интерфейс взаимодействия);
Выполнение операций конвертации."""

import telebot
from telebot import types
from config import *
from extensions import Converter, APIException

# Размещение кнопок в Телеграм боте
conv_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
buttons = []
for val in exchanges.keys():
    buttons.append(types.KeyboardButton(val.capitalize()))

conv_markup.add(*buttons)

bot = telebot.TeleBot(TOKEN)


# Вводная инструкция
@bot.message_handler(commands=["start", "help"])
def start(message):
    text = "Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<колличество переводимой валюты>\nУвидеть список всех доступных валют: /values \
 Выполнить операцию конвертации: /convert"

    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in exchanges.keys():
        text = "\n".join((text, key))
    bot.send_message(message.chat.id, text)


# Исполнение операций для конвертации
@bot.message_handler(commands=["convert"])
def convert(message: telebot.types.Message):
    text = "Выберите валюту, из которой ковертировать:"
    bot.send_message(message.chat.id, text, reply_markup=conv_markup)
    bot.register_next_step_handler(message, base_handler)


def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = "Выберите валюту, в которой ковертировать:"
    bot.send_message(message.chat.id, text, reply_markup=conv_markup)
    bot.register_next_step_handler(message, sym_handler, base)


def sym_handler(message: telebot.types.Message, base):
    sym = message.text.strip()
    text = "Выберите  колличество конвертируемой валюты:"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, sym)


def amount_handler(message: telebot.types.Message, base, sym):
    amount = message.text.strip()
    try:
        new_price = Converter.get_price(base, sym, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации: \n{e}")
    else:
        text = f"Цена {amount} {base} в {sym} : {new_price}"
        bot.send_message(message.chat.id, text)


bot.polling()
