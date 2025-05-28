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
    # targets = sys.argv[4].split(",")
    # min = sys.argv[5]
    # max = sys.argv[6]

    bot = Bot(url, username, password)
    bot.login()

    if not bot.is_logged():
        print("Incorrect username and password")
        return

    bot.go_home()
    bot.setup()
    sleep(1)
    bot.go_home()
    # bot.go_village()
    # bot.test_store()
    # bot.test_builder()


if __name__ == "__main__":
    main()
    sleep(5)
