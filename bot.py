import telebot

import configparser

from classes import *

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг

TOKEN = config["Telegram"]["token"] # Токен телеграм

bot = telebot.TeleBot(TOKEN)

values = {
    'рубль': 'RUB',
    'евро': 'EUR',
    'доллар': 'USD'
}


@bot.message_handler(commands=['start', 'help', 'values'])
def start(message: telebot.types.Message):
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Привет,  {message.chat.username}! Дотупные команды бота - "/start", '
                                          f'"/help", "/values"'
                                          f' \nВведите валюты для конвертации -> " евро рубль сумма "')
    if message.text == '/help':
        bot.send_message(message.chat.id,
                         'Нужно Отправить сообщение боту в виде <имя валюты цену которой нужно узнать> '
                         '<имя валюты в которой надо узнать цену первой '
                         'валюты> <количество первой валюты>.'
                         '\nВведите "доллар -> рубль -> Сумма"'
                         '\nПосмотреть список валют команда - "/values"')
    if message.text == '/values':
        bot.reply_to(message, f'{[i for i in values]}')


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    try:

        api = ApiResponse()

        data = message.text.split()

        if data[0] in values and data[1] in values:
            base = values[data[0]]
            quote = values[data[1]]
            amount = float(data[2])
        else:
            raise bot.reply_to(message, str(ValException("Введена не верная валюта")))

        bot.reply_to(message, f"{api.get_price(base, quote, amount)} {quote}")

    except TypeError:
        pass
    except Exception as e:
        bot.reply_to(message, str(e))


bot.polling(none_stop=True)  # Запуск бота
