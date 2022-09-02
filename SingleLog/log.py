from warnings import warn

from .SingleLog import Logger, LogLevel


# old way of calling
class Logger(Logger):
    TRACE = LogLevel.TRACE
    DEBUG = LogLevel.DEBUG
    INFO = LogLevel.INFO
    SILENT = LogLevel.SILENT

    def __init__(self, *args, **kwargs):

        warn(f'"from SingleLog.log import Logger" is deprecated, use "from SingleLog import Logger"',
             DeprecationWarning, stacklevel=2)

        handler = kwargs.pop('handler', None)
        if handler is not None:
            # DeprecationWarning('handler is deprecated, use callback instead')
            callback = kwargs.pop('callback', None)
            if callback is not None:
                raise ValueError('callback and handler cannot be set at the same time')

            kwargs['callback'] = handler

        super().__init__(*args, **kwargs)
