from threading import Thread
from time import sleep
from app.service.BotService import bot_service
from app.Logger import LogType, msg


def loop_check_queue():
    """Background loop that updates bot tasks continuously."""
    while True:
        try:
            if bot_service.bot is None:
                sleep(5)  # wait until bot is initialized
                continue

            bot_service.update()
            constructions = bot_service.get_constructions()
            msg(f"constructions: {constructions}")
            bot_service.refresh_builds(constructions)
        except Exception as e:
            msg(f"[!] Error in build queue loop: {e}", log_type=LogType.ERROR)
        sleep(10)


def start_background_tasks():
    """Start background thread for build queue loop."""
    t = Thread(target=loop_check_queue, daemon=True)
    t.start()
    msg("[✓] Background build queue thread started.")


def start_bot(url: str, username: str, password: str):
    """Initialize bot in a separate thread."""

    def run():
        msg("init bot")
        bot = bot_service.init_bot(url, username, password)
        msg(f"[i] Bot initialized: {bot}")

    t = Thread(target=run, daemon=True)
    t.start()
