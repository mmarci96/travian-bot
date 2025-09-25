import time
from threading import Thread
from app.service.BotService import bot_service


def loop_check_queue():
    while True:
        try:
            bot_service.get_build_queue()
        except Exception as e:
            print(f"[!] Error in build queue loop: {e}")
        time.sleep(10)


def start_background_tasks():
    t = Thread(target=loop_check_queue, daemon=True)
    t.start()
    print("[✓] Background build queue thread started.")
