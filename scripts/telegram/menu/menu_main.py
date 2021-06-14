import scripts.globals as global_var
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from scripts.telegram.menu.menu_message import *
from scripts.telegram.func import *

menu_message = {}
last_message_id = 0


def main_menu(bot, update):
    global menu_message
    menu_message_id = bot.effective_message.message_id
    menu_message['id'] = menu_message_id
    menu_message['text'] = main_menu_message()
    menu_message['keyboard'] = main_menu_keyboard()
    bot.callback_query.message.edit_text(
        text=main_menu_message(),
        reply_markup=main_menu_keyboard()
    )


def cancel_menu(bot, update):
    bot.callback_query.message.delete()


def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Информация', callback_data='info')],
                [InlineKeyboardButton('Настройки', callback_data='settings')]
                ]
    return InlineKeyboardMarkup(keyboard)


def info_menu(bot, update):
    full_message = get_base_info()

    bot.callback_query.message.reply_text(
        text=full_message,
        disable_web_page_preview=True
    )
