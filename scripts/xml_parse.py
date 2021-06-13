import requests
import xmltodict
import scripts.base_sqlite as base_sqlite


url = "https://www.cbr-xml-daily.ru/daily_utf8.xml"


def update_data():
    data = get_data()
    data_insert = {}
    try:
        update_date = data['ValCurs']['@Date']
        currencies = data['ValCurs']['Valute']
        for currency in currencies:
            value_str = currency['Value']
            value = value_str.replace(',', '.')
            del value_str

            nominal_str = currency['Nominal']
            nominal = nominal_str.replace(',', '.')
            del nominal_str

            data_insert[currency['CharCode']] = {
                'name': currency['Name'],
                'value': float(value),
                'nominal': float(nominal)
            }
            del currency
            del value
            del nominal
        del currencies
    except:
        update_date = None
        pass
    del data


    try:
        last_update = base_sqlite.select(
            what='value',
            table='settings',
            expression='name="last_update"'
        )[0][0]
    except:
        last_update = None

    if last_update != update_date:
        data_update = []
        data_update.append ([
            'last_update',
            update_date
        ])
        base_sqlite.replace_data(
            table='settings(name, value)',
            data=tuple(data_update)
        )

        data_update = []
        for data in data_insert:
            data_update.append([
                data,
                data_insert[data]['name'],
                data_insert[data]['nominal'],
                data_insert[data]['value']
            ]
            )

        data_update = tuple(data_update)
        base_sqlite.replace_data(
            table='currency(code, name, nominal, value)',
            data=data_update
        )


def get_data():
    global url
    response = requests.get(url)
    data = xmltodict.parse(response.content)
    return data
