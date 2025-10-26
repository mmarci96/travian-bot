from threading import Lock
from typing import List, Optional
from app.Bot import Bot
from app.data.Construction import Construction


class BotService:
    def __init__(self):
        self.bot: Optional[Bot] = None
        self.lock = Lock()

    def init_bot(self, url: str, username: str, password: str) -> dict:
        with self.lock:
            if self.bot:
                return {"status": "success", "message": "Already logged in"}

            self.bot = Bot(url, username, password)
            self.bot.login()
            if self.bot.is_logged():
                self.bot.setup()
                return {"status": "success", "message": "Logged in"}
            else:
                self.bot = None
                return {"status": "error", "message": "Login failed"}

    def refresh_builds(self, constructions):
        with self.lock:
            if self.bot:
                return self.bot.refresh_builds(constructions)

    def get_status(self) -> dict:
        with self.lock:
            if not self.bot:
                return {"status": "error", "message": "Bot not initialized"}
            return {"status": "success", "message": self.bot.get_status()}

    def update(self):
        with self.lock:
            if not self.bot:
                raise RuntimeError("Bot not initialized")
            self.bot.update()

    def test_build(self):
        with self.lock:
            if not self.bot:
                raise RuntimeError("Bot not initialized")
            self.bot.test_build()

    def send_farmlist(self, farm_list: list):
        with self.lock:
            if not self.bot:
                raise RuntimeError("Bot not initialized")
            self.bot.send_list(farm_list)

    def get_villages(self):
        with self.lock:
            if not self.bot:
                raise RuntimeError("Bot not initialized")
            return self.bot.get_villages()

    def add_resource_task(
        self, village_id: str, resource_type: str, target_level: int
    ):
        with self.lock:
            if not self.bot:
                raise RuntimeError("Bot not initialized")
            return self.bot.build_resource(
                village_id, resource_type, target_level
            )

    def get_tasks(self, village_id: str):
        with self.lock:
            if not self.bot:
                raise RuntimeError("Bot not initialized")
            return self.bot.get_tasks_by_village_id(village_id)

    def get_constructions_by_village_id(
        self, id: str
    ) -> Optional[List[Construction]]:
        with self.lock:
            if not self.bot:
                raise RuntimeError("Bot not initialized")
            return self.bot.get_constructions_by_village_id(id)

    def get_constructions(self):
        with self.lock:
            if self.bot:
                return self.bot.get_constructions()
        return None


# Singleton instance
bot_service = BotService()
