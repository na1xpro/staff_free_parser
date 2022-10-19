from telebot import types
from main_parser import main_proces
import config
import telebot
from cfg_main_constants import name_file

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('Парсинг', callback_data='parse_data')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data)
def chek_callback_data(callback):
    if callback.data == 'parse_data':
        bot.send_message(callback.message.chat.id, 'Подождите немного, парсинг начался.')
        main_proces()
        markup = types.InlineKeyboardMarkup(row_width=1)
        json_file_send = types.InlineKeyboardButton('JSon', callback_data='json_fle')
        txt_file_send = types.InlineKeyboardButton('TXT', callback_data='txt_fle')
        markup.add(json_file_send, txt_file_send)
        bot.send_message(callback.message.chat.id,
                         'Готово, в каком разширении вам отправить файл?', reply_markup=markup)
    if callback.data == "json_fle":
        bot.send_message(callback.message.chat.id,
                         'Отлично сейчас отправим вам json  файл', )
        file = open(name_file['file1'], 'rb')
        bot.send_document(callback.message.chat.id, file)
    if callback.data == 'txt_fle':
        bot.send_message(callback.message.chat.id,
                         'Отлично сейчас отправим вам txd  файл', )
        file = open(name_file['file2'], 'rb')
        bot.send_document(callback.message.chat.id, file)


bot.polling(none_stop=True)
