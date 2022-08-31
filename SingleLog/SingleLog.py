from __future__ import annotations

import builtins
import inspect
import os
import threading
from enum import IntEnum, auto
from time import strftime
from typing import Callable, List, Set

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
default_key_word_fails = ['fail', 'false', 'error', 'bug']
default_color_list = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
enable_loggers: Set[Logger] = set()
is_first_print = True


def set_other_logger_finish(current_logger: Logger = None):
    global enable_loggers
    for logger in enable_loggers:
        if logger is current_logger:
            continue
        logger.status = LoggerStatus.FINISH


def new_print(*args, **kwargs):
    print_logger.print(*args, **kwargs)


builtins.print = new_print


class Logger:

    def __init__(self, log_name: [str | None] = 'logger', log_level: LogLevel = LogLevel.INFO,
                 skip_repeat: bool = False, handler: [Callable | List[Callable]] = None, stage_sep: str = '...',
                 timestamp: [str | None] = "%m.%d %H:%M:%S", key_word_success: [list | None] = None,
                 key_word_fails: [list | None] = None, stage_color_list: [List[Fore] | None] = None):
        """
        Init of Logger.
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
        self._do_level = None
        self.check_add_new_line = False

        with global_lock:
            global enable_loggers
            enable_loggers.add(self)

    def info(self, *msg):
        self._do(LogLevel.INFO, *msg)

    def debug(self, *msg):
        self._do(LogLevel.DEBUG, *msg)

    def trace(self, *msg):
        self._do(LogLevel.TRACE, *msg)

    def _do(self, log_level: LogLevel, *msg):
        if self.status != LoggerStatus.FINISH:
            self.check_add_new_line = True
        self.status = LoggerStatus.START
        if self._start(log_level, *msg):
            self.status = LoggerStatus.STAGE
            self._do_level = log_level
        elif not self.check_add_new_line:
            self.status = LoggerStatus.FINISH

    def stage(self, *msg):
        # its log level is the same as the last do_level
        if self.status == LoggerStatus.FINISH:
            # works like normal logger
            self._do(LogLevel.INFO, *msg)
        elif self.status == LoggerStatus.STAGE:
            self._stage(self._do_level, *msg)
        else:
            raise Exception(f'Unknown log status {self.status}')

    def __del__(self):
        with global_lock:
            global enable_loggers
            enable_loggers.remove(self)

    def _check_log_level(self, log_level: LogLevel) -> bool:
        # check the msg will be output or not

        if self.status == LoggerStatus.PRINT:
            return True

        if self.log_level > log_level:
            return False

        return True

    def _stage(self, log_level: LogLevel, msg):
        if not self._check_log_level(log_level):
            return False

        if self.status != LoggerStatus.STAGE:
            raise Exception(f'Unknown log status {self.status}')

        message = str(msg)

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

        total_message = f' {self.stage_sep} {color}{message}'

        utils.output_screen(total_message)
        utils.output_file(self.handlers, total_message)

    def _start(self, log_level: LogLevel, *msg, **kwargs) -> bool:

        if not self._check_log_level(log_level):
            return False

        total_message = None
        if self.status != LoggerStatus.PRINT:

            if not msg:
                msg = ' '

            message = f'{merge_msg(msg[0], frame=False)}'
            for m in msg[1:]:
                message = f'{message} {merge_msg(m)}'

            if self.skip_repeat:
                if self._last_msg == message:
                    return False
                self._last_msg = message

            line_no = None
            file_name = None
            if self.log_level <= LogLevel.DEBUG:
                cf = inspect.currentframe()
                line_no = cf.f_back.f_back.f_lineno
                file_name = cf.f_back.f_back.f_code.co_filename
                file_name = os.path.basename(file_name)

            if self.status != LoggerStatus.PRINT:
                timestamp = f'[{strftime(self.timestamp)}]' if self.timestamp else ''
                location = f'[{file_name} {line_no}]' if line_no is not None else ''

                total_message = f'{timestamp}{self.log_name}{location} {message}'.strip()

        with global_lock:

            if self.status != LoggerStatus.STAGE:
                global is_first_print
                if not is_first_print:
                    if self.check_add_new_line:
                        self.check_add_new_line = False
                        old_print()
                        set_other_logger_finish(self)
                    elif self.status == LoggerStatus.START:

                        add_new_line = False
                        for logger in enable_loggers:
                            if logger != self and logger.status != LoggerStatus.FINISH:
                                add_new_line = True
                            logger.status = LoggerStatus.FINISH

                        if add_new_line:
                            old_print()
                    else:
                        old_print()
                is_first_print = False

            kwargs['end'] = ''

            if self.status == LoggerStatus.PRINT:
                old_print(*msg, **kwargs)
                return True

            utils.output_screen(total_message)
            utils.output_file(self.handlers, total_message)

            return True


class PrintLogger(Logger):
    def print(self, *args, **kwargs):
        self.status = LoggerStatus.PRINT
        self._start(LogLevel.INFO, *args, **kwargs)


print_logger = PrintLogger(log_name='', timestamp=None)
enable_loggers.add(print_logger)