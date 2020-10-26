import sys
from time import strftime
import threading

global_lock = threading.Lock()


class Logger:
    TRACE = 1
    DEBUG = 2
    INFO = 3
    SILENT = 4

    def __init__(self, prefix, level, handler=None):
        self.prefix = prefix
        self.level = level
        self.handler = handler

    def merge(self, msg) -> str:
        if isinstance(msg, list):
            msg = list(map(str, msg))
            for i in range(len(msg)):
                if len(msg[i]) == 0:
                    continue
                if msg[i][0].upper() != msg[i][0].lower() and i != 0:
                    msg[i] = ' ' + msg[i].lstrip()
                if (msg[i][-1].upper() != msg[i][-1].lower() and
                        i != len(msg) - 1):
                    msg[i] = msg[i].rstrip() + ' '

            msg = ' '.join(msg)
        msg = str(msg)
        msg = msg.replace('  ', ' ')

        return msg

    def _show(self, current_log_level, msg):

        if self.level > current_log_level:
            return
        if current_log_level == self.SILENT:
            return
        if not isinstance(msg, int) and len(msg) == 0:
            return

        msg = self.merge(msg)

        total_message = '[' + strftime('%m%d %H%M%S') + ']'

        if self.prefix is not None:
            total_message += '[' + self.prefix + ']'
        total_message += ' ' + msg

        try:
            global_lock.acquire()
            print(total_message.encode(
                sys.stdin.encoding,
                'replace'
            ).decode(
                sys.stdin.encoding
            ))
        except Exception:
            print(total_message.encode('utf-8', "replace").decode('utf-8'))
        finally:
            global_lock.release()

        if self.handler is not None:
            self.handler(total_message)

    def show(self, *msg):

        if len(msg) == 0:
            return

        if isinstance(msg[0], int):
            current_log_level = msg[0]
            msg = msg[1:]
        else:
            current_log_level = self.INFO

        if self.level > current_log_level:
            return

        for i in range(len(msg)):
            if isinstance(msg[i], list):
                msg = msg[i].copy()

        des = self.merge(msg[0])
        if len(msg) == 0:
            return
        msg = msg[1:]

        total_message = [f' [{self.merge(x)}]' for x in msg]
        total_message.insert(0, des)

        self._show(current_log_level, ''.join(total_message))


if __name__ == '__main__':

    test_log_level = [
        Logger.SILENT,
        Logger.INFO,
        Logger.DEBUG,
        Logger.TRACE
    ]

    for current_log_level in test_log_level:
        logger = Logger('test prefix', current_log_level)

        logger.show(Logger.SILENT, 'SILENT')
        logger.show(Logger.INFO, 'INFO')
        logger.show(Logger.DEBUG, 'DEBUG')
        logger.show(Logger.TRACE, 'TRACE')

        print('=================')

    logger = Logger('test prefix', Logger.INFO)
    logger.show(Logger.INFO, 'Test', 123)
    logger.show(Logger.INFO, 'Test', [1, 2])

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
