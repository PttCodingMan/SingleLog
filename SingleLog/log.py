import inspect
import json
import os
import threading
from time import strftime

global_lock = threading.Lock()


def _merge(msg, frame: bool = True) -> str:
    if isinstance(msg, dict):
        msg = f'\n{json.dumps(msg, indent=2)}'
    elif isinstance(msg, tuple):
        msg = " ".join([str(x).strip() for x in msg])
        if frame:
            msg = f'({msg})'
    else:
        if isinstance(msg, str):
            pass
        elif hasattr(msg, '__iter__'):
            msg = " ".join([str(x).strip() for x in msg])
        else:
            msg = str(msg)
        if frame:
            msg = f'[{msg}]'

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


def get_call_location_info(func):
    def wrapper(*args, **kwargs):
        cf = inspect.currentframe()

        line_no = cf.f_back.f_lineno
        file_name = cf.f_back.f_code.co_filename
        file_name = os.path.basename(file_name)
        kwargs.update({
            'line_no': line_no,
            'file_name': file_name})
        return func(*args, **kwargs)

    return wrapper


class Logger:
    TRACE = LoggerLevel(LoggerLevel.TRACE)
    DEBUG = LoggerLevel(LoggerLevel.DEBUG)
    INFO = LoggerLevel(LoggerLevel.INFO)
    SILENT = LoggerLevel(LoggerLevel.SILENT)

    log_level_list = [TRACE, DEBUG, INFO, SILENT]

    def __init__(self, prefix, level: LoggerLevel = INFO, handler=None, skip_repeat: bool = False,
                 timestamp: str = "%Y%m%d %H:%M:%S"):
        self.prefix = prefix
        if not self.prefix:
            self.prefix = ''
        else:
            self.prefix = f'[{self.prefix}]'

        if not isinstance(level, LoggerLevel):
            raise TypeError(f'Error log level type: {type(level)}')
        if level not in self.log_level_list:
            raise ValueError('Log level error')

        self.level = level

        if handler is not None:
            if not isinstance(handler, list):
                handler = [handler]
            for h in handler:
                if not callable(h):
                    raise TypeError('Handler must be callable!!')
        self.handler = handler
        self.skip_repeat = skip_repeat
        self.last_msg = None
        self.timestamp = timestamp

    def info(self, *msg):
        self.log(Logger.INFO, *msg)

    @get_call_location_info
    def debug(self, *msg, **kwargs):
        self.log(Logger.DEBUG, *msg, **kwargs)

    @get_call_location_info
    def trace(self, *msg, **kwargs):
        self.log(Logger.TRACE, *msg, **kwargs)

    def log(self, log_level: LoggerLevel, *msg, line_no=None, file_name=None):
        if self.skip_repeat:
            if self.last_msg == msg:
                return
            self.last_msg = msg

        if len(msg) == 0:
            return

        if log_level not in self.log_level_list:
            raise ValueError('Log level error')

        if self.level > log_level:
            return

        if len(msg) == 0:
            return

        des = _merge(msg[0], frame=False)

        msg = [f' {_merge(x)}' for x in msg[1:]]
        msg.insert(0, des)

        timestamp = f'[{strftime(self.timestamp)}]' if self.timestamp else ''
        location = f'[{file_name} {line_no}]' if line_no is not None else ''

        total_message = f'{timestamp}{self.prefix}{location} {"".join(msg)}'.strip()

        with global_lock:
            if self.handler:
                for handler in self.handler:
                    handler(total_message)
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
