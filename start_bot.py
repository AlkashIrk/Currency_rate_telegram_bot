import scripts.base_sqlite
from scripts.telegram.bot import start_bot
from scripts.xml_parse import update_data

if __name__ == "__main__":
    update_data()
    start_bot()
