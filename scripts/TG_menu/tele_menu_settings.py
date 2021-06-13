from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from scripts.TG_menu.tele_menu_message import *

menu_message = {}
last_message_id = 0


def redraw_menu(bot, redraw_force=False):
    global last_message_id
    menu_message_id = menu_message['id']
    if last_message_id > menu_message_id or redraw_force:
        bot.callback_query.message.delete()
        menu_message_id = bot.callback_query.message.reply_text(
            text=menu_message['text'],
            reply_markup=menu_message['keyboard']
        )
        menu_message['id'] = menu_message_id.message_id
    last_message_id = menu_message['id']


def do_redraw_menu(bot, update):
    from scripts.TG_menu.tele_menu_main import main_menu_keyboard

    menu_message_id = bot.effective_message.message_id
    menu_message['id'] = menu_message_id
    menu_message['text'] = main_menu_message()
    menu_message['keyboard'] = main_menu_keyboard()
    redraw_menu(bot, redraw_force=True)


def settings_menu(bot, update):
    global menu_message
    chat_id = bot.effective_chat.id
    menu_message_id = bot.effective_message.message_id
    menu_message['id'] = menu_message_id
    menu_message['text'] = settings_menu_message()
    menu_message['keyboard'] = settings_menu_keyboard(chat_id=chat_id)
    bot.callback_query.message.edit_text(settings_menu_message(),
                                         reply_markup=settings_menu_keyboard(chat_id=chat_id))


############################ Keyboards #########################################
def settings_menu_keyboard(chat_id):
    text = 'Текущая валюта'
    sell_edit = 'USD'

    keyboard = [[InlineKeyboardButton(text, callback_data='toggle_buy_sell!%s' % sell_edit)],
                [InlineKeyboardButton('Перерисовать меню', callback_data='redraw_menu')],
                [InlineKeyboardButton('Назад', callback_data='main')],
                [InlineKeyboardButton('Выйти', callback_data='cancel')]
                ]
    return InlineKeyboardMarkup(keyboard)
