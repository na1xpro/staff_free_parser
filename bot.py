from telebot import types
from main_parser import parse_diskounts, parse_tracksuits_man
from cfg_main_constants import name_file_json, name_file_txt
import config
import telebot

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('ЗНИЖКИ', callback_data='free_price')
    item2 = types.InlineKeyboardButton('СПОРТИВНІ КОСТЮМИ', callback_data='sportivni_kostyumi')
    item3 = types.InlineKeyboardButton('Вітровки', callback_data='vitrovki')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, ' Выберите категорию для парсинга ', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data)
def chek_callback_data(callback):
    data = callback.data

    def send_file_bot(name_file, type_file) -> str:
        bot.send_message(callback.message.chat.id,
                         f'Отлично сейчас отправим вам  {type_file} файл', )
        file = open(name_file, 'rb')
        bot.send_document(callback.message.chat.id, file)

    def send_main_file(name):
        bot.send_message(callback.message.chat.id, 'Подождите немного, парсинг начался.')
        name_func = name
        markup = types.InlineKeyboardMarkup(row_width=1)
        json_file_send = types.InlineKeyboardButton('JSon', callback_data='json_fle')
        txt_file_send = types.InlineKeyboardButton('TXT', callback_data='txt_fle')
        markup.add(json_file_send, txt_file_send)
        bot.send_message(callback.message.chat.id,
                         'Готово, в каком разширении вам отправить файл?', reply_markup=markup)

    if data == "json_fle":
        send_file_bot(name_file_json['free_price_js'], 'json')
    if data == 'txt_fle':
        send_file_bot(name_file_txt['free_price_txt'], 'txt')

    if callback.data == 'free_price':
        send_main_file(parse_diskounts())


bot.polling(none_stop=True)
