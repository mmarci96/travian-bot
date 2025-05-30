from random import randrange
from app.Bot import Bot
from time import sleep
import sys


def main():
    if len(sys.argv) > 8:
        print("You did not write the correct system variables")
        return

    url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    bot = Bot(url, username, password)
    bot.login()

    if not bot.is_logged():
        print("Incorrect username and password")
        return

    bot.setup()
    # bot.test_build()
    sleep(randrange(3, 4))
    # bot.update()


if __name__ == "__main__":
    main()
    sleep(5)
