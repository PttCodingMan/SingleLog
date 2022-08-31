from .SingleLog import Logger, LogLevel


# old way of calling
class Logger(Logger):
    TRACE = LogLevel.TRACE
    DEBUG = LogLevel.DEBUG
    INFO = LogLevel.INFO
    SILENT = LogLevel.SILENT
