from __future__ import annotations

import inspect
import json
import os
import threading
from enum import IntEnum, auto
from time import strftime
from typing import Callable

from AutoStrEnum import AutoStrEnum
from colorama import init, Fore

init(autoreset=True)

global_lock = threading.Lock()


def _merge(msg, frame: bool = True) -> str:
    if isinstance(msg, (list, dict)):
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


class LoggerStatus(AutoStrEnum):
    DOING = auto()
    DONE = auto()

    FINISH = auto()


default_key_word_success = ['success', 'ok', 'done', 'yes', 'y', 'okay', 'okey', 'true', 't', 'complete', 'pass']
default_key_word_fails = ['fail', 'false', 'f', 'error', 'e', 'no', 'n', 'bug']


class SingleLog:

    def __init__(self, log_name: [str | None] = 'logger', log_level: LogLevel = LogLevel.INFO,
                 skip_repeat: bool = False, handler: Callable = None, od_end: str = ' ... ',
                 timestamp: [str | None] = "%m.%d %H:%M:%S", key_word_success: [list | None] = None,
                 key_word_fails: [list | None] = None):
        """
        Init of SingleLog.
        :param log_name: the display name of current logger.
        :param log_level: (Optional) (Default: Logger.INFO)the log level of current logger.
        :param handler: (Optional) the handler of current logger. you can get the output msg from the handler.
        :param skip_repeat: (Optional) if True, the current logger will skip the repeat msg.
        :param timestamp: (Optional) the timestamp format of current logger.
        :param od_end: (Optional) the end of the output msg.
        :param key_word_success: (Optional) the key words of success.
        :param key_word_fails: (Optional) the key words of fails.
        """

        self.log_name = log_name
        if not self.log_name:
            self.log_name = ''
        else:
            self.log_name = f'[{self.log_name}]'

        if not isinstance(log_level, LogLevel):
            raise TypeError(f'Error log level type: {type(log_level)}')

        self.log_level = log_level

        if handler is not None:
            if not isinstance(handler, list):
                handler = [handler]
            for h in handler:
                if not callable(h):
                    raise TypeError('Handler must be callable!!')

        self.handler = handler
        self.skip_repeat = skip_repeat
        self.timestamp = timestamp

        self.do_end = od_end

        if key_word_success is None:
            key_word_success = default_key_word_success
        self.key_word_success = key_word_success

        if key_word_fails is None:
            key_word_fails = default_key_word_fails
        self.key_word_fails = key_word_fails

        self._log_status = LoggerStatus.FINISH
        self._last_msg = None

    def info(self, *msg):
        self._log(LogLevel.INFO, *msg)

    def debug(self, *msg):
        self._log(LogLevel.DEBUG, *msg)

    def trace(self, *msg):
        self._log(LogLevel.TRACE, *msg)

    def _do(self, log_level: LogLevel, *msg):
        if self._log_status == LoggerStatus.DOING:
            print()
        self._log_status = LoggerStatus.DOING
        self._log(log_level, *msg)
        self._do_level = log_level

    def do_info(self, *msg):
        self._do(LogLevel.INFO, *msg)

    def do_debug(self, *msg):
        self._do(LogLevel.DEBUG, *msg)

    def do_trace(self, *msg):
        self._do(LogLevel.TRACE, *msg)

    def done(self, *msg):
        # its log level is the same as the last do_level

        if self._log_status == LoggerStatus.FINISH:
            # works like normal logger
            self._log(LogLevel.INFO, *msg)
        else:
            self._log_status = LoggerStatus.DONE
            self._log(self._do_level, *msg)
            self._log_status = LoggerStatus.FINISH

    def _log(self, log_level: LogLevel, *msg):

        if self.log_level > log_level:
            return

        if 0 == (msg_size := len(msg)):
            msg = ' '

        if self.log_level <= LogLevel.DEBUG:
            cf = inspect.currentframe()
            line_no = cf.f_back.f_back.f_lineno
            file_name = cf.f_back.f_back.f_code.co_filename
            file_name = os.path.basename(file_name)
        else:
            line_no = None
            file_name = None

        message = ''
        for m in msg:
            if not message:
                message = f'{message}{_merge(m, frame=False)}'
            else:
                message = f'{message} {_merge(m)}'

        if self.skip_repeat:
            if self._last_msg == message:
                return
            self._last_msg = message

        if self._log_status == LoggerStatus.DONE:
            color = ''
            for s in self.key_word_success:
                if s in message.lower():
                    color = Fore.GREEN
                    break

            if not color:
                for s in self.key_word_fails:
                    if s in message.lower():
                        color = Fore.RED
                        break

            total_message = f'{color}{message}'
        else:
            timestamp = f'[{strftime(self.timestamp)}]' if self.timestamp else ''
            location = f'[{file_name} {line_no}]' if line_no is not None else ''

            total_message = f'{timestamp}{self.log_name}{location} {message}'.strip()

        cur_end = self.do_end if self._log_status == LoggerStatus.DOING else os.linesep

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
                print(total_message, end=cur_end)
            except UnicodeEncodeError:
                total_message = total_message.encode("utf-16", 'surrogatepass').decode("utf-16", "surrogatepass")
                try:
                    print(total_message, end=cur_end)
                except UnicodeEncodeError:
                    print('sorry, SingleLog can not print the message')


class Logger(SingleLog):
    # the old logger
    TRACE = LogLevel.TRACE
    DEBUG = LogLevel.DEBUG
    INFO = LogLevel.INFO
    SILENT = LogLevel.SILENT

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
