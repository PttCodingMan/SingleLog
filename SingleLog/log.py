from __future__ import annotations

import builtins
import inspect
import json
import os
import threading
from enum import IntEnum, auto
from time import strftime
from typing import Callable, List, Set

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
    TAIL = auto()
    STAGE = auto()

    FINISH = auto()


default_key_word_success = ['success', 'ok', 'done', 'yes', 'y', 'okay', 'true', 'complete', 'pass']
default_key_word_fails = ['fail', 'false', 'error', 'bug']
enable_loggers: Set[SingleLog] = set()
is_first_print = True
old_print = builtins.print


def set_other_logger_finish(current_logger: SingleLog = None):
    global enable_loggers
    for logger in enable_loggers:
        if logger is current_logger:
            continue
        logger.status = LoggerStatus.FINISH


def _if_do_new_line(current_logger: SingleLog = None):
    global enable_loggers

    # what situation we print a new line
    # 1. if next print is a default print
    # 2. the current logger.status is doing

    print_new_line = False
    for i, logger in enumerate(enable_loggers):
        if not print_new_line:
            if current_logger is not None:
                # if current logger is doing and there is some logger status is STAGE or TAIL or DOING
                # we print a new line
                # old_print('.', current_logger.status)
                if current_logger.status != LoggerStatus.DOING:
                    continue
                if logger.status in [LoggerStatus.STAGE, LoggerStatus.TAIL, LoggerStatus.DOING]:
                    old_print()
                    print_new_line = True
            else:
                # for default print
                # if there is some logger status is STAGE or TAIL
                # we print a new line
                if logger.status in [LoggerStatus.STAGE, LoggerStatus.TAIL, LoggerStatus.DOING]:
                    old_print()
                    print_new_line = True

        if logger is not current_logger:
            # we don't check this anymore
            logger.status = LoggerStatus.FINISH


def new_print(*args, **kwargs):
    _if_do_new_line()
    old_print(*args, **kwargs)
    if kwargs.get('end', '') == '\n':
        set_other_logger_finish()
    global is_first_print
    is_first_print = False


builtins.print = new_print


class SingleLog:

    def __init__(self, log_name: [str | None] = 'logger', log_level: LogLevel = LogLevel.INFO,
                 skip_repeat: bool = False, handler: [Callable | List[Callable]] = None, stage_sep: str = ' ... ',
                 timestamp: [str | None] = "%m.%d %H:%M:%S", key_word_success: [list | None] = None,
                 key_word_fails: [list | None] = None):
        """
        Init of SingleLog.
        :param log_name: the display name of current logger.
        :param log_level: (Optional) (Default: Logger.INFO)the log level of current logger.
        :param handler: (Optional) the handler of current logger. you can get the output msg from the handler.
        :param skip_repeat: (Optional) if True, the current logger will skip the repeat msg.
        :param timestamp: (Optional) the timestamp format of current logger.
        :param stage_sep: (Optional) the separator of stage.
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

        self.stage_sep = stage_sep

        if key_word_success is None:
            key_word_success = default_key_word_success
        self.key_word_success = key_word_success

        if key_word_fails is None:
            key_word_fails = default_key_word_fails
        self.key_word_fails = key_word_fails

        self._stage_count = 0
        self._color_list = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

        self.status = LoggerStatus.FINISH
        self._last_msg = None
        self._do_level = None
        self._add_new_line = False

        global enable_loggers
        enable_loggers.add(self)

    def info(self, *msg):
        self._do(LogLevel.INFO, *msg)

    def debug(self, *msg):
        self._do(LogLevel.DEBUG, *msg)

    def trace(self, *msg):
        self._do(LogLevel.TRACE, *msg)

    def _do(self, log_level: LogLevel, *msg):
        self.status = LoggerStatus.DOING
        if self._log(log_level, *msg):
            self.status = LoggerStatus.TAIL
            self._do_level = log_level

    def stage(self, *msg):
        # its log level is the same as the last do_level
        if self.status == LoggerStatus.DOING:
            # works like normal logger
            self._do(LogLevel.INFO, *msg)
        elif self.status == LoggerStatus.TAIL or self.status == LoggerStatus.STAGE:
            self.status = LoggerStatus.STAGE
            self._log(self._do_level, *msg)
        else:
            raise Exception('Unknown log status')

    def __del__(self):
        global enable_loggers
        enable_loggers.remove(self)

    def _log(self, log_level: LogLevel, *msg) -> bool:

        if self.log_level > log_level:
            return False

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
                return False
            self._last_msg = message

        if self.status == LoggerStatus.STAGE:
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

            if not color:
                color = self._color_list[self._stage_count]
                self._stage_count = (self._stage_count + 1) % len(self._color_list)

            total_message = f' {self.stage_sep} {color}{message}'
        else:
            global is_first_print
            if not is_first_print:
                if self.status == LoggerStatus.DOING:
                    old_print()
                else:
                    _if_do_new_line(self)
            is_first_print = False

            # _if_do_new_line(self)
            timestamp = f'[{strftime(self.timestamp)}]' if self.timestamp else ''
            location = f'[{file_name} {line_no}]' if line_no is not None else ''

            total_message = f'{timestamp}{self.log_name}{location} {message}'.strip()

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
                old_print(total_message, end='')
            except UnicodeEncodeError:
                total_message = total_message.encode("utf-16", 'surrogatepass').decode("utf-16", "surrogatepass")
                try:
                    old_print(total_message, end='')
                except UnicodeEncodeError:
                    old_print('sorry, SingleLog can not print the message')

        return True


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
