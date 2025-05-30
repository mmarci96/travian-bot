from datetime import datetime


class Construction:
    """Stores the name, level its building to and the timestamp on the finish date"""

    def __init__(
        self,
        name: str,
        level: int,
        finish_at: datetime,
    ):
        super(Construction, self).__init__()
        self.name = name
        self.level = level
        self.finish_at = finish_at

    def is_complete(self) -> bool:
        now = datetime.now()
        if now > self.finish_at:
            return True
        return False

    def duration(self):
        return datetime.now() - self.finish_at

    def to_dict(self):
        date_str = self.finish_at.strftime("%Y-%m-%d %H:%M:%S")
        return {
            "name": self.name,
            "level": self.level,
            "finish_at": self.finish_at.strftime(date_str)
        }

    def __repr__(self):
        date_str = self.finish_at.strftime("%Y-%m-%d %H:%M:%S")
        return f"<Construction (Name: {self.name}) | Level: {self.level} | Finish at: {date_str}>"
