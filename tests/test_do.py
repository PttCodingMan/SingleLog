import sys
import time

sys.path.insert(0, '../')

from SingleLog import Logger, LogLevel


def test_do():
    logger = Logger('test_do')

    logger.do_info('do something success')
    time.sleep(0.5)
    logger.done('ok')

    logger.do_info('do something fails')
    time.sleep(0.5)
    logger.done('fails')

    print('=' * 20)

    logger = Logger(log_level=LogLevel.INFO)

    logger.do_debug('do something success')
    time.sleep(0.5)
    logger.done('DEBUG')
