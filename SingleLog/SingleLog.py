from __future__ import annotations

import builtins
import inspect
import os
import threading
from enum import IntEnum, auto
from time import strftime
from typing import Callable, List

from AutoStrEnum import AutoStrEnum
from colorama import init, Fore

from SingleLog import utils
from SingleLog.utils import merge_msg, old_print

init(autoreset=True)

global_lock = threading.Lock()


class LogLevel(IntEnum):
    TRACE = 1
    DEBUG = 2
    INFO = 3
    SILENT = 4


class LoggerStatus(AutoStrEnum):
    PRINT = auto()
    START = auto()
    STAGE = auto()

    FINISH = auto()


default_key_word_success = ['success', 'ok', 'done', 'yes', 'okay', 'true', 'complete', 'pass']
default_key_word_fails = ['fail', 'false', 'error', 'bug', 'fire']
default_color_list = [Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX,
                      Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX]
last_logger: [Logger | None] = None


def new_print(*args, **kwargs):
    print_logger.print(*args, **kwargs)


builtins.print = new_print

BOLD = '\033[1m'


class Logger:

    def __init__(self, log_name: [str | None] = 'logger', log_level: LogLevel = LogLevel.INFO,
                 skip_repeat: bool = False, handler: [Callable | List[Callable]] = None, stage_sep: str = '..',
                 timestamp: [str | None] = "%m.%d %H:%M:%S", key_word_success: [list | None] = None,
                 key_word_fails: [list | None] = None, stage_color_list: [List[Fore] | None] = None):
        """
        :param log_name: the display name of current logger.
        :param log_level: (Optional) (Default: Logger.INFO)the log level of current logger.
        :param handler: (Optional) the handlers of current logger. you can get the output msg from the handlers.
        :param skip_repeat: (Optional) if True, the current logger will skip the repeat msg.
        :param timestamp: (Optional) the timestamp format of current logger.
        :param stage_sep: (Optional) the separator of stage.
        :param key_word_success: (Optional) the key words of success.
        :param key_word_fails: (Optional) the key words of fails.
        :param stage_color_list: (Optional) the color list of stage.
        """

        self.log_name = log_name
        if not self.log_name:
            self.log_name = ''
        else:
            self.log_name = f'[{self.log_name}]'

        if not isinstance(log_level, LogLevel):
            raise TypeError(f'Error log level type: {type(log_level)}')

        self.log_level = log_level

        self.handlers = []
        if handler is not None:
            if not isinstance(handler, list):
                handler = [handler]
            for h in handler:
                if not callable(h):
                    raise TypeError('Handler must be callable!!')
            self.handlers = handler

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

        if stage_color_list is None:
            self._stage_color_list = default_color_list
        else:
            self._stage_color_list = stage_color_list

        self.status = LoggerStatus.FINISH
        self._last_msg = None
        self._stage_level = None

    def info(self, *msg):
        self._start_check(LogLevel.INFO, *msg)

    def debug(self, *msg):
        self._start_check(LogLevel.DEBUG, *msg)

    def trace(self, *msg):
        self._start_check(LogLevel.TRACE, *msg)

    def _start_check(self, log_level: LogLevel, *msg):

        with global_lock:
            if self._start(log_level, *msg):
                self.status = LoggerStatus.STAGE
                self._stage_level = log_level

    def stage(self, *msg):
        # its log level is the same as the last do_level
        if self.status == LoggerStatus.FINISH:
            # works like normal logger
            self._start_check(LogLevel.INFO, *msg)
            return

        self._stage(self._stage_level, *msg)

    def _print(self, *args, **kwargs):
        with global_lock:
            self.status = LoggerStatus.PRINT
            self._add_newline()
            self._output(None, *args, **kwargs)
            self.status = LoggerStatus.FINISH

            global last_logger
            last_logger = self


    def _check_log_level(self, log_level: LogLevel) -> bool:
        # check the msg will be output or not

        if self.status == LoggerStatus.PRINT:
            return True

        if self.log_level > log_level:
            return False

        return True

    def _stage(self, log_level: LogLevel, msg):
        if not self._check_log_level(log_level):
            return

        if self.status not in [LoggerStatus.STAGE, LoggerStatus.START]:
            raise Exception(f'Unknown log status {self.status}')

        message = str(msg)
        if self.skip_repeat:
            self._last_msg = message

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
            color = self._stage_color_list[self._stage_count]
            self._stage_count = (self._stage_count + 1) % len(self._stage_color_list)

        total_message = f' {self.stage_sep} {color}{BOLD}{message}'

        utils.output_screen(total_message)
        utils.output_file(self.handlers, total_message)

        global last_logger
        last_logger = self

    def _start(self, log_level: LogLevel, *msg) -> bool:

        if not self._check_log_level(log_level):
            return False

        self.status = LoggerStatus.START

        if not msg:
            msg = ' '

        message = f'{merge_msg(msg[0], frame=False)}'
        for m in msg[1:]:
            message = f'{message} {merge_msg(m)}'

        if self.skip_repeat:
            if self._last_msg == message:
                return False
            self._last_msg = message

        location = ''
        if self.log_level <= LogLevel.DEBUG:
            cf = inspect.currentframe()
            line_no = cf.f_back.f_back.f_lineno
            file_name = cf.f_back.f_back.f_code.co_filename
            file_name = os.path.basename(file_name)
            location = f'[{file_name} {line_no}]'

        timestamp = f'[{strftime(self.timestamp)}]' if self.timestamp else ''
        total_message = f'{timestamp}{self.log_name}{location} {message}'.strip()

        self._add_newline()
        self._output(total_message)

        global last_logger
        last_logger = self

        return True

    def __add_newline(self) -> None:
        old_print()
        if last_logger is not self:
            last_logger.status = LoggerStatus.FINISH
        self._stage_count = 0

    def _add_newline(self):

        if self.status == LoggerStatus.STAGE:
            # if the last stage is stage, don't need to lock
            raise Exception('Cannot print in stage status')

        global last_logger
        if last_logger:
            if self.status == LoggerStatus.START:
                # if the status is start, it means we need to check the status of last logger
                # note: last logger could be self
                if last_logger.status != LoggerStatus.FINISH:
                    # if self or last logger is not finish, add newline
                    self.__add_newline()
            elif self.status == LoggerStatus.PRINT:
                # is the last print is not print, we need to add newline
                # adjust this to avoid the situation that the last print is print
                if last_logger.__class__.__name__ != 'PrintLogger':
                    # if self is not last logger, add newline
                    self.__add_newline()

    def _output(self, total_message: [str | None], *args, **kwargs) -> None:
        if self.status == LoggerStatus.PRINT:
            old_print(*args, **kwargs)
            return

        utils.output_screen(total_message)
        utils.output_file(self.handlers, total_message)



class PrintLogger(Logger):
    def print(self, *args, **kwargs):
        self._print(*args, **kwargs)


print_logger = PrintLogger(log_name='', timestamp=None)
