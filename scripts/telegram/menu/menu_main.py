import scripts.globals as global_var
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from scripts.telegram.func import *

menu_message = {}
last_message_id = 0


def main_menu(bot, update):
    global menu_message

    user_id = bot.effective_chat.id
    user_name = bot.effective_chat.full_name
    menu_message_id = bot.effective_message.message_id

    user_currency = get_user_currency(
        user_id=user_id,
        user_name=user_name
    )

    user_info = {
        user_id:
            {
                'id': menu_message_id,
                'text': 'Текущая валюта %s' % user_currency,
                'keyboard': main_menu_keyboard()
            }
    }
    menu_message.update(user_info)

    bot.callback_query.message.edit_text(
        text=user_info[user_id]['text'],
        reply_markup=user_info[user_id]['keyboard']
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
