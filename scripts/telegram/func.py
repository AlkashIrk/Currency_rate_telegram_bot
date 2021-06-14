import time
import scripts.base_sqlite as base_sqlite
from scripts.xml_parse import update_data

# периодичность проверки курсов валют на сайте (в секундах) - каждый час
check_period = 60 * 60 * 1
last_check = 0


def parse_mess(bot, update):
    check_updates()
    user_id = bot.effective_chat.id
    user_name = bot.effective_chat.full_name
    text_data = bot.effective_message.text

    user_currency = get_user_currency(user_id=user_id, user_name=user_name)

    value_str = text_data.replace(' ', '')
    value_str = value_str.replace(',', '.')
    try:
        value = float(value_str)

        data = base_sqlite.select(
            what='nominal, value, name',
            table='currency',
            expression='code="%s"' % user_currency
        )[0]

        rub_to_curr = round(value / data[1] * data[0], 2)
        curr_to_rub = round(value / data[0] * data[1], 2)

        message_head_1 = 'Валюта: %s\nКод валюты: %s\n' % (data[2], user_currency)
        message_head_2 = 'Курс ЦБ:\n%s %s = %s руб\n\n' % (data[0], user_currency, round(data[1], 2))

        message_head = message_head_1 + message_head_2

        message_body_1 = '   %s руб = %s %s\n' % (value, rub_to_curr, user_currency)
        message_body_2 = '   %s %s = %s руб' % (value, user_currency, curr_to_rub)

        full_message = message_head + message_body_1 + message_body_2

        full_message = '``` \n' + full_message + '\n```'

        bot.message.reply_text(
            text=full_message,
            parse_mode='markdown',
            disable_web_page_preview=True
        )

    except Exception as inst:
        print("\t%s" % inst)
        full_message = "Произошла ошибка при вводе данных. Введите число для конвертации валюты."
        bot.message.reply_text(
            text=full_message,
            disable_web_page_preview=True
        )


def get_user_currency(user_id, user_name):
    try:
        base_sqlite.select(
            what='name',
            table='users',
            expression='tg_id=%s' % user_id
        )[0][0]
    except:
        data_update = [
            [
                user_id,
                user_name
            ]
        ]
        base_sqlite.replace_data(
            table='users(tg_id, name)',
            data=tuple(data_update)
        )

    user_currency = base_sqlite.select(
        what='last_currency',
        table='users',
        expression='tg_id=%s' % user_id
    )[0][0]

    return user_currency


def get_base_info():
    try:
        last_update = base_sqlite.select(
            table='settings',
            what='value',
            expression='name="last_update"'
        )[0][0]
        text = 'Последнее обновление %s\n\nДля конвертации введите число в сообщении' % last_update
    except:
        return None

    return text


def check_updates():
    global last_check
    timestamp_now = round(time.time())

    if last_check == 0 or last_check + check_period <= timestamp_now:
        try:
            last_check = base_sqlite.select(
                table='settings',
                what='value',
                expression='name="last_check"'
            )[0][0]
        except:
            last_check = 0

    if last_check + check_period <= timestamp_now or last_check == 0:
        update_result = update_data()
        if update_result:
            data_update = [[
                'last_check',
                timestamp_now]
            ]
            base_sqlite.replace_data(
                table='settings(name, value)',
                data=tuple(data_update)
            )
