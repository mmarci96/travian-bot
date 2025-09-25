import time
from threading import Thread
from app.service.BotService import bot_service
from app.Logger import LogType, msg


def loop_check_queue():
    while True:
        try:
            bot_service.update()
            constructions = bot_service.get_constructions()
            msg(f"constructions: {constructions}")
            bot_service.refresh_builds(constructions)
        except Exception as e:
            msg(f"[!] Error in build queue loop: {e}", log_type=LogType.ERROR)
        time.sleep(10)


def start_background_tasks():
    t = Thread(target=loop_check_queue, daemon=True)
    t.start()
    msg("[✓] Background build queue thread started.")
