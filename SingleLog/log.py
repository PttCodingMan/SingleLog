import inspect
import json
import os
import sys
import threading
from enum import IntEnum, unique
from time import strftime

global_lock = threading.Lock()


def _merge(msg, frame: bool = True) -> str:
    if isinstance(msg, dict) or isinstance(msg, list):
        msg = f'\n{json.dumps(msg, indent=2, ensure_ascii=False)}'
    elif isinstance(msg, tuple):
        msg = " ".join([str(x).strip() for x in msg])
        if frame:
            msg = f'({msg})'
    else:
        if isinstance(msg, str):
            pass
        else:
            msg = str(msg)
        if frame:
            msg = f'[{msg}]'

    return msg


class LogLevel(IntEnum):
    TRACE = 1
    DEBUG = 2
    INFO = 3
    SILENT = 4


class Logger:
    TRACE = LogLevel.TRACE
    DEBUG = LogLevel.DEBUG
    INFO = LogLevel.INFO
    SILENT = LogLevel.SILENT

    def __init__(self, logger_name, log_level: LogLevel = INFO, handler=None, skip_repeat: bool = False,
                 timestamp: [str | None] = "%m.%d %H:%M:%S"):
        """
        Init of SingleLog.
        :param logger_name: the display name of current logger.
        :param log_level: (Optional) (Default: Logger.INFO)the log level of current logger.
        :param handler: (Optional) the handler of current logger. you can get the output msg from the handler.
        :param skip_repeat: (Optional) if True, the current logger will skip the repeat msg.
        :param timestamp: (Optional) the timestamp format of current logger.
        """

        self.logger_name = logger_name
        if not self.logger_name:
            self.logger_name = ''
        else:
            self.logger_name = f'[{self.logger_name}]'

        if not isinstance(log_level, LogLevel):
            raise TypeError(f'Error log level type: {type(log_level)}')

        self.logger_level = log_level

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
        self._log(Logger.INFO, *msg)

    def debug(self, *msg):
        self._log(Logger.DEBUG, *msg)

    def trace(self, *msg):
        self._log(Logger.TRACE, *msg)

    def _log(self, log_level: LogLevel, *msg):
        if self.skip_repeat:
            if self.last_msg == msg:
                return
            self.last_msg = msg

        if (msg_size := len(msg)) == 0:
            msg = ' '

        if not isinstance(log_level, LogLevel):
            raise ValueError('Log level error')

        if self.logger_level > log_level:
            return

        if self.logger_level <= self.DEBUG:
            cf = inspect.currentframe()
            line_no = cf.f_back.f_back.f_lineno
            file_name = cf.f_back.f_back.f_code.co_filename
            file_name = os.path.basename(file_name)
        else:
            line_no = None
            file_name = None

        des = _merge(msg[0], frame=False)

        msg = [f' {_merge(x)}' for x in msg[1:]]
        msg.insert(0, des)

        timestamp = f'[{strftime(self.timestamp)}]' if self.timestamp else ''
        location = f'[{file_name} {line_no}]' if line_no is not None else ''

        total_message = f'{timestamp}{self.logger_name}{location} {"".join(msg)}'.strip()

        with global_lock:

            try:
                if self.handler:
                    for handler in self.handler:
                        handler(total_message)
            except UnicodeEncodeError:
                total_message = total_message.encode("utf-16", 'surrogatepass').decode("utf-16", "surrogatepass")
                if self.handler:
                    for handler in self.handler:
                        handler(total_message)

            try:
                print(total_message)
            except UnicodeEncodeError:
                try:
                    print(total_message.encode(sys.stdin.encoding, 'replace').decode(sys.stdin.encoding))
                except:
                    try:
                        print(total_message.encode('utf-8', "replace").decode('utf-8'))
                    except:
                        pass

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
