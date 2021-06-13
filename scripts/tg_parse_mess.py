import scripts.base_sqlite as base_sqlite


def parse_mess(bot, update):
    user_id = bot.effective_chat.id
    user_name = bot.effective_chat.full_name
    text_data = bot.effective_message.text

    data_update = []
    data_update.append([
        user_id,
        user_name
    ])
    base_sqlite.replace_data(
        table='users(tg_id, name)',
        data=tuple(data_update)
    )

    user_currency = base_sqlite.select(
        what='last_currency',
        table='users',
        expression='tg_id=%s' % user_id
    )[0][0]

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
        full_message = "Произошла ошибка при вводе данных. Введите сумму для конвертации валюты."
        bot.message.reply_text(
            text=full_message,
            disable_web_page_preview=True
        )
