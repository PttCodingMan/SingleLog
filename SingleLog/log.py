import json
import threading
from time import strftime

global_lock = threading.Lock()


def _merge(msg) -> str:
    if isinstance(msg, list):
        msg = f'[{" ".join([str(x).strip() for x in msg])}]'
    elif isinstance(msg, tuple):
        msg = f'({" ".join([str(x).strip() for x in msg])})'
    elif isinstance(msg, dict):
        msg = f'\n{json.dumps(msg, indent=2)}'
    else:
        msg = f'[{str(msg)}]'

    return msg


class LoggerLevel:
    TRACE = 1
    DEBUG = 2
    INFO = 3
    SILENT = 4

    group = [TRACE, DEBUG, INFO, SILENT]

    def __init__(self, level):
        if level not in self.group:
            raise ValueError(f'log level error: {level}')
        self.value = level

    def __lt__(self, other):
        if not isinstance(other, LoggerLevel):
            return False
        return self.value < other.value

    def __le__(self, other):
        if not isinstance(other, LoggerLevel):
            return False
        return self.value <= other.value

    def __eq__(self, other):
        if not isinstance(other, LoggerLevel):
            return False
        return self.value == other.value

    def __ne__(self, other):
        if not isinstance(other, LoggerLevel):
            return False
        return self.value != other.value

    def __gt__(self, other):
        if not isinstance(other, LoggerLevel):
            return False
        return self.value > other.value

    def __ge__(self, other):
        if not isinstance(other, LoggerLevel):
            return False
        return self.value >= other.value


class Logger:
    TRACE = LoggerLevel(LoggerLevel.TRACE)
    DEBUG = LoggerLevel(LoggerLevel.DEBUG)
    INFO = LoggerLevel(LoggerLevel.INFO)
    SILENT = LoggerLevel(LoggerLevel.SILENT)

    group = [TRACE, DEBUG, INFO, SILENT]

    def __init__(self, prefix, level, handler=None, skip_repeat: bool = False, need_timestamp: bool = True):
        self.prefix = prefix
        if not self.prefix:
            self.prefix = ''
        else:
            self.prefix = f'[{self.prefix}]'

        if not isinstance(level, LoggerLevel):
            raise TypeError(f'Error log level type: {type(level)}')
        if level not in self.group:
            raise ValueError('Log level error')

        self.level = level
        if handler is not None and not callable(handler):
            raise TypeError('Handler must is callable!!')
        self.handler = handler
        self.skip_repeat = skip_repeat
        self.last_msg = None
        self.need_timestamp = need_timestamp

    def info(self, *msg):
        self.log(Logger.INFO, *msg)

    def debug(self, *msg):
        self.log(Logger.DEBUG, *msg)

    def trace(self, *msg):
        self.log(Logger.TRACE, *msg)

    def log(self, log_level: LoggerLevel, *msg):

        if self.skip_repeat:
            if self.last_msg == msg:
                return
            self.last_msg = msg

        if len(msg) == 0:
            return

        if log_level not in self.group:
            raise ValueError('Log level error')

        if self.level > log_level:
            return

        if len(msg) == 0:
            return

        des = str(msg[0])
        msg = msg[1:]

        msg = [f' {_merge(x)}' for x in msg]
        msg.insert(0, des)

        timestamp = ''
        if self.need_timestamp:
            timestamp = f'[{strftime("%Y%m%d %H:%M:%S")}]'

        total_message = f'{timestamp}{self.prefix} {"".join(msg)}'.strip()

        if self.handler is not None:
            self.handler(total_message)

        with global_lock:
            print(total_message)

#                        ____________
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#  _____________________|            |_____________________
# |                                                        |
# |                                                        |
# |                                                        |
# |_____________________              _____________________|
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |____________|


# 耶和華是我的牧者，我必不致缺乏。
# 他使我躺臥在青草地上，領我在可安歇的水邊。
# 他使我的靈魂甦醒，為自己的名引導我走義路。
# 我雖然行過死蔭的幽谷，也不怕遭害，因為你與我同在；你的杖，你的竿，都安慰我。
# 在我敵人面前，你為我擺設筵席；你用油膏了我的頭，使我的福杯滿溢。
# 我一生一世必有恩惠慈愛隨著我；我且要住在耶和華的殿中，直到永遠。
# - 詩篇 23篇
