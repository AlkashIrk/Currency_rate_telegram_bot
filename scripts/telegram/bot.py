import scripts.globals as global_var
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from scripts.telegram.func import *
from scripts.telegram.menu.menu_main import *
from scripts.telegram.menu.menu_settings import *

token = global_var.telegram_token

if token is None:
    exit()

'''
############################### Bot ############################################
'''


def start(bot, update):
    global updater
    global menu_message

    user_id = bot.message.chat.id
    user_name = bot.effective_chat.full_name
    menu_message_id = bot.message.message_id

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

    bot.message.reply_text(
        text=user_info[user_id]['text'],
        reply_markup=user_info[user_id]['keyboard']
    )

    updater.bot.delete_message(
        chat_id=user_id,
        message_id=menu_message_id
    )


def error(update, context):
    print(f'Update {update} caused error {context.error}')


'''
############################# Handlers #########################################
'''


def start_bot():
    global updater
    updater = Updater(token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(info_menu, pattern='info'))
    updater.dispatcher.add_handler(CallbackQueryHandler(cancel_menu, pattern='cancel'))
    updater.dispatcher.add_handler(CallbackQueryHandler(settings_menu, pattern='settings'))
    updater.dispatcher.add_handler(CallbackQueryHandler(do_redraw_menu, pattern='redraw_menu'))

    updater.dispatcher.add_handler(CallbackQueryHandler(user_currency_menu, pattern='toggle_currency'))
    updater.dispatcher.add_handler(CallbackQueryHandler(toggle_user_currency, pattern='toggle_user_currency!'))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, parse_mess))
    updater.dispatcher.add_error_handler(error)

    updater.start_polling()
