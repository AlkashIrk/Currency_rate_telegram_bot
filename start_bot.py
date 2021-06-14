import scripts.base_sqlite
from scripts.telegram.bot import start_bot
from scripts.telegram.func import check_updates

if __name__ == "__main__":
    check_updates()
    start_bot()
