
from .SingleLog import Logger, LogLevel


class Logger(Logger):
    # the old logger
    TRACE = LogLevel.TRACE
    DEBUG = LogLevel.DEBUG
    INFO = LogLevel.INFO
    SILENT = LogLevel.SILENT
