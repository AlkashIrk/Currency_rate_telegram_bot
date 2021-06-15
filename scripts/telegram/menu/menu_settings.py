from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import scripts.base_sqlite as base_sqlite
from scripts.telegram.func import get_user_currency
from scripts.telegram.menu.menu_main import main_menu_keyboard

menu_message = {}
last_message_id = 0


def redraw_menu(bot, redraw_force=False):
    global last_message_id

    user_id = bot.effective_chat.id

    menu_message_id = menu_message[user_id]['id']
    if last_message_id > menu_message_id or redraw_force:
        bot.callback_query.message.delete()
        menu_message_id = bot.callback_query.message.reply_text(
            text=menu_message[user_id]['text'],
            reply_markup=menu_message[user_id]['keyboard']
        )
        menu_message['id'] = menu_message_id.message_id
    last_message_id = menu_message['id']


def do_redraw_menu(bot, update):
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

    redraw_menu(bot, redraw_force=True)


def settings_menu(bot, update):
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
                'keyboard': settings_menu_keyboard()
            }
    }
    menu_message.update(user_info)

    bot.callback_query.message.edit_text(
        text=user_info[user_id]['text'],
        reply_markup=user_info[user_id]['keyboard']
    )


def user_currency_menu(bot, update):
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
                'keyboard': user_currency_keyboard()
            }
    }
    menu_message.update(user_info)

    bot.callback_query.message.edit_text(
        text=user_info[user_id]['text'],
        reply_markup=user_info[user_id]['keyboard']
    )


def toggle_user_currency(bot, update):
    global last_message_id

    response = bot.callback_query.data
    user_id = bot.effective_chat.id
    user_name = bot.effective_chat.full_name

    user_currency = response.split('!')[1]

    data_update = [
        [
            user_id,
            user_name,
            user_currency
        ]
    ]

    base_sqlite.replace_data(
        table='users(tg_id, name, last_currency)',
        data=tuple(data_update)
    )

    data = base_sqlite.select(
        what='nominal, value, name',
        table='currency',
        expression='code="%s"' % user_currency
    )[0]

    message_head = 'Валюта для конвертации изменена:\n\n'
    message_body = 'Код валюты: %s\nКурс:\n%s %s = %s руб' % (user_currency, data[0], data[2], data[1])

    full_message = message_head + message_body

    message = bot.callback_query.message.reply_text(
        text=full_message,
        parse_mode='markdown',
        disable_web_page_preview=True
    )

    user_currency = get_user_currency(
        user_id=user_id,
        user_name=user_name
    )

    last_message_id = message.message_id
    menu_message_id = bot.effective_message.message_id

    user_info = {
        user_id:
            {
                'id': menu_message_id,
                'text': 'Текущая валюта %s' % user_currency,
                'keyboard': settings_menu_keyboard()
            }
    }
    menu_message.update(user_info)

    redraw_menu(bot, redraw_force=True)


'''
############################ Keyboards #########################################
'''


def settings_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Сменить валюту', callback_data='toggle_currency')],
                [InlineKeyboardButton('Перерисовать меню', callback_data='redraw_menu')],
                [InlineKeyboardButton('Назад', callback_data='main')],
                [InlineKeyboardButton('Выйти', callback_data='cancel')]
                ]
    return InlineKeyboardMarkup(keyboard)


def user_currency_keyboard():
    currencies = base_sqlite.select(
        what='code, name, nominal, value',
        table='currency',
        expression=''
    )

    keyboard = []
    for currency in currencies:
        keyboard.append(
            [InlineKeyboardButton(
                '%s\n%s' % (currency[0], currency[1]),
                callback_data='toggle_user_currency!%s'
                              % (currency[0]))]
        )

    keyboard.append([InlineKeyboardButton('Назад', callback_data='main')])
    return InlineKeyboardMarkup(keyboard)
