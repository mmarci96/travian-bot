from enum import Enum
from datetime import datetime
import sys


class LogType(Enum):
    ERROR = "[ERROR]"
    WARN = "[WARN]"
    INFO = "[INFO]"
    RUN = "[RUN]"


def msg(msg: str, log_type=LogType.INFO):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f" [{timestamp}] {log_type.value} {msg}")
    sys.stdout.flush()
