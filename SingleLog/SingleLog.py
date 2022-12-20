from __future__ import annotations

import atexit
import builtins
import inspect
import logging
import os
import threading
import uuid
from enum import auto, IntEnum
from time import strftime
from typing import Callable, List, Optional

from AutoStrEnum import AutoStrEnum
from colorama import init, Fore

from SingleLog import utils
from SingleLog.utils import merge_msg, old_print

init(autoreset=True)

global_lock = threading.Lock()


class LogLevel(IntEnum):
    # more log
    TRACE = logging.DEBUG - 1
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    SILENT = logging.CRITICAL + 1

    # less log


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


@atexit.register
def process_exit():
    old_print(' ')


BOLD = '\033[1m'


class Logger:

    def __init__(self, log_name: [str | None] = 'logger', log_level: LogLevel = LogLevel.INFO,
                 skip_repeat: bool = False, stage_sep: str = '..', timestamp: [str | None] = "%m.%d %H:%M:%S",
                 callback: [Callable | List[Callable]] = None, stage_color_list: [List[Fore] | None] = None,
                 key_word_success: [list | None] = None, key_word_fails: [list | None] = None):

        """
        :param log_name: the display name of current logger.
        :param log_level: (Optional) (Default: Logger.INFO)the log level of current logger.
        :param callback: (Optional) the _callback_list of current logger. you can get the output msg from the _callback_list.
        :param skip_repeat: (Optional) if True, the current logger will skip the repeat msg.
        :param timestamp: (Optional) the _timestamp format of current logger.
        :param stage_sep: (Optional) the separator of stage.
        :param key_word_success: (Optional) the key words of success.
        :param key_word_fails: (Optional) the key words of fails.
        :param stage_color_list: (Optional) the color list of stage.
        """

        self._log_name = log_name
        if not self._log_name:
            self._log_name = ''
        else:
            self._log_name = f'[{self._log_name}]'

        if not isinstance(log_level, LogLevel):
            raise TypeError(f'Error log level type: {type(log_level)}')

        self._log_level = log_level

        self._callback_list = []
        if callback is not None:
            if not isinstance(callback, list):
                callback = [callback]
            for h in callback:
                if not callable(h):
                    raise TypeError('callback must be callable!!')
            self._callback_list = callback

        self._skip_repeat = skip_repeat
        self._timestamp = timestamp

        self._stage_sep = stage_sep

        if key_word_success is None:
            key_word_success = default_key_word_success
        self._key_word_success = key_word_success

        if key_word_fails is None:
            key_word_fails = default_key_word_fails
        self._key_word_fails = key_word_fails

        self._stage_count = 0

        if stage_color_list is None:
            self._stage_color_list = default_color_list
        else:
            self._stage_color_list = stage_color_list

        self._logger_status = LoggerStatus.FINISH
        self._last_msg = None

    def error(self, *msg):
        self._start(LogLevel.ERROR, *msg)

    def warn(self, *msg):
        self._start(LogLevel.WARN, *msg)

    def info(self, *msg):
        self._start(LogLevel.INFO, *msg)

    def debug(self, *msg):
        self._start(LogLevel.DEBUG, *msg)

    def trace(self, *msg):
        self._start(LogLevel.TRACE, *msg)

    def stage(self, *msg):
        # the stage msg will be output in the same line
        # the stage effect works on LogLevel.INFO and the last logger is not FINISH

        if self._log_level != LogLevel.INFO:
            self._start(self._log_level, *msg)
            return

        if last_logger and last_logger._logger_status == LoggerStatus.FINISH:
            # works like normal logger
            self._start(LogLevel.INFO, *msg)
            return

        if self._logger_status == LoggerStatus.FINISH:
            self._start(LogLevel.INFO, *msg)
            return

        self._stage(LogLevel.INFO, *msg)

    def _print(self, *args, **kwargs):
        with global_lock:
            self._logger_status = LoggerStatus.PRINT
            self._add_newline()
            self._output(None, *args, **kwargs)
            self._logger_status = LoggerStatus.FINISH

            global last_logger
            last_logger = self

    def _check_log_level(self, log_level: LogLevel) -> bool:
        # check the msg will be output or not

        if self._logger_status == LoggerStatus.PRINT:
            return True

        if not log_level:
            raise ValueError('log_level must be set!!')

        if self._log_level > log_level:
            return False

        return True

    def _stage(self, log_level: LogLevel, msg):
        if not self._check_log_level(log_level):
            return

        if self._logger_status not in [LoggerStatus.STAGE, LoggerStatus.START]:
            raise Exception(f'Unknown log logger_status {self._logger_status}')

        message = str(msg)
        if self._skip_repeat:
            self._last_msg = message

        color = ''
        for s in self._key_word_success:
            if s in message.lower():
                color = Fore.GREEN
                break

        if not color:
            for s in self._key_word_fails:
                if s in message.lower():
                    color = Fore.RED
                    break

        if not color:
            color = self._stage_color_list[self._stage_count]
            self._stage_count = (self._stage_count + 1) % len(self._stage_color_list)

        total_message = f' {self._stage_sep} {color}{BOLD}{message}'

        utils.output_screen(total_message)
        utils.callback(self._callback_list, total_message)

        global last_logger
        last_logger = self

    def _start(self, log_level: LogLevel, *msg):

        with global_lock:
            if not self._check_log_level(log_level):
                return

            self._logger_status = LoggerStatus.START

            if not msg:
                msg = ' '

            message = f'{merge_msg(msg[0], frame=False)}'

            color = ''
            if log_level == LogLevel.WARN:
                color = Fore.YELLOW
            elif log_level == LogLevel.ERROR:
                color = Fore.RED

            bold = BOLD if color != '' else ''

            for m in msg[1:]:
                message = f'{color}{bold}{message} {merge_msg(m)}'
            else:
                message = f'{color}{bold}{message}'

            if self._skip_repeat:
                if self._last_msg == message:
                    return
                self._last_msg = message

            location = ''
            if self._log_level <= LogLevel.DEBUG:
                cf = inspect.currentframe()
                line_no = cf.f_back.f_back.f_lineno
                file_name = cf.f_back.f_back.f_code.co_filename
                file_name = os.path.basename(file_name)
                location = f'[{file_name} {line_no}]'

            timestamp = f'[{strftime(self._timestamp)}]' if self._timestamp else ''
            total_message = f'{timestamp}{self._log_name}{location} {message}'.strip()

            self._add_newline()
            self._output(total_message)

            global last_logger
            last_logger = self

            self._logger_status = LoggerStatus.STAGE

            return

    def __add_newline(self) -> None:
        old_print()
        if last_logger is not self:
            last_logger._logger_status = LoggerStatus.FINISH
        self._stage_count = 0

    def _add_newline(self):

        if self._logger_status == LoggerStatus.STAGE:
            # if the last stage is stage, don't need to lock
            raise Exception('Cannot print in stage logger_status')

        global last_logger
        if last_logger:
            if self._logger_status == LoggerStatus.START:
                # if the logger_status is start, it means we need to check the logger_status of last logger
                # note: last logger could be self
                if last_logger._logger_status != LoggerStatus.FINISH:
                    # if self or last logger is not finish, add newline
                    self.__add_newline()
            elif self._logger_status == LoggerStatus.PRINT:
                # is the last print is not print, we need to add newline
                # adjust this to avoid the situation that the last print is print
                if last_logger.__class__.__name__ != 'PrintLogger':
                    # if self is not last logger, add newline
                    self.__add_newline()

    def _output(self, total_message: [str | None], *args, **kwargs) -> None:
        if self._logger_status == LoggerStatus.PRINT:
            old_print(*args, **kwargs)
            return

        utils.output_screen(total_message)
        utils.callback(self._callback_list, total_message)


class PrintLogger(Logger):
    def print(self, *args, **kwargs):
        self._print(*args, **kwargs)


print_logger = PrintLogger(log_name='', timestamp='')


########################################################################################################################

class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = "\x1b[0;37m"
    white = '\x1b[2m'
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, name):
        super().__init__()
        # self.fmt = '[%(asctime)s][%(levelname)s] %(message)s'
        self.fmt = f'[%(asctime)s][{name}] %(message)s'
        self.datefmt = '%m.%d %H:%M:%S'
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.white + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)

        # global current_color
        # log_fmt = f"\x1b[{current_color}m" + self.fmt + self.reset

        formatter = logging.Formatter(log_fmt, self.datefmt)
        return formatter.format(record)


uuid_pool = set()


def get_uuid():
    while True:
        new_id = str(uuid.uuid4())
        if new_id not in uuid_pool:
            uuid_pool.add(new_id)
            return new_id


class DefaultLogger:
    def __init__(self, name, level=LogLevel.INFO, handler: Optional[list] = []):
        self.logger = logging.getLogger(get_uuid())
        self.logger.setLevel(level)

        # Create stdout handler for logging to the console (logs all five levels)
        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(level)
        stdout_handler.setFormatter(CustomFormatter(name))

        # Add handlers to the logger
        self.logger.addHandler(stdout_handler)

        self.handlers = []
        if handler is not None:
            if not isinstance(handler, list):
                handler = [handler]
            self.handlers = handler

    def _convert(self, msg):
        message = f'{merge_msg(msg[0], frame=False)}'

        for m in msg[1:]:
            message = f'{message} {merge_msg(m)}'

        return message

    def _output(self, logger_func, msg):
        message = self._convert(msg)
        logger_func(message)
        for handler in self.handlers:
            handler(message)

    def info(self, *msg):
        self._output(self.logger.info, msg)

    def debug(self, *msg):
        self._output(self.logger.debug, msg)

    def trace(self, *msg):
        self._output(self.logger.debug, msg)

    def warning(self, *msg):
        self._output(self.logger.warning, msg)

    def error(self, *msg):
        self._output(self.logger.error, msg)

    def critical(self, *msg):
        self._output(self.logger.critical, msg)
