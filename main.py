import telebot
from config import token, keys, names
from extensions import ConvertException, CryptoConversion

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'приветствуем вас в нашем конвертируещем валюты боте.\n Для того что-бы начать работу, ' \
           'введите данные в формате\n <валюта которую хотим перевести> <в какую хотим перевести> ' \
           '<количество переводимой валюты>\n для того чтобы узнать список валют введите /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def helper(message: telebot.types.Message):
    text = 'Для того что-бы начать работу, ' \
           'введите данные в формате\n <валюта которую хотим перевести> <в какую хотим перевести> ' \
           '<количество переводимой валюты>\n для того чтобы узнать список валют введите /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты для конвертации:\n'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        val = message.text.split(' ')
        if len(val) != 3:
            raise ConvertException('Неверное количество вводимых данных. '
                                   'Для того чтобы посмотреть правила ввода данных введите команду /help')
        quote, base, amount = val
        final_price = CryptoConversion.convert(quote, base, amount)
    except ConvertException as e:
        bot.reply_to(message, f"ошибка пользователя\n\n{e}")
    except Exception as a:
        bot.reply_to(message, f'ошибка сервера\n\n{a}')
    else:
        bot.send_message(message.chat.id, f"{str(final_price)} {names[base]}")


bot.polling(none_stop=True)
