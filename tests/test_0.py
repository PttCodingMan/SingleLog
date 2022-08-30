import time
import sys

sys.path.insert(0, '../')

from SingleLog import LogLevel
from SingleLog import Logger


def test_func():
    logger = Logger('test_func')

    logger.info('')

    logger.info('type', type(''))
    print('===')
    logger.info('ok', '123 ', ' 456')
    print('===')
    logger.info([101, 102, 103])

    logger.info('data', {'1': 'value1', '2': 'value2'})
    logger.info(1)
    logger.info(1, 2, 3, 4, 5)
    logger.info('show int', 100)
    logger.info('show str', 'this is a string')
    logger.info('show int list', [101, 102, 103])
    logger.info('show string list', ['101', '102', '103'])
    logger.info('show tuple', ('12', '14', '16'))

    logger.info('des', 'value0', 'value1', 'value2')

    try:
        raise ValueError('ValueError')
    except Exception as e:
        logger.info('got exception', str(e))

    print('=' * 20)

    logger = Logger('TRACE', LogLevel.TRACE)

    logger.info('This should be 3 to print')
    logger.debug('This should be 3 to print')
    logger.trace('This should be 3 to print')

    print('=' * 20)

    logger = Logger('DEBUG', LogLevel.DEBUG)

    logger.info('This should be 2 to print')
    logger.debug('This should be 2 to print')
    logger.trace('This should NOT be print')

    print('=' * 20)

    logger = Logger('INFO')

    logger.info('This should be 1 to print')
    logger.debug('This should NOT be print')
    logger.trace('This should NOT be print')

    print('=' * 20)

    logger = Logger('SILENT', LogLevel.SILENT)

    logger.info('This should NOT be print')
    logger.debug('This should NOT be print')
    logger.trace('This should NOT be print')

    print('=' * 20)

    logger = Logger('test', skip_repeat=True)
    logger.info('This should only print once', 'and its a silent msg on top')
    logger.info('This should only print once', 'and its a silent msg on top')
    logger.info('This should only print once', 'and its a silent msg on top')

    print('=' * 20)

    logger = Logger('custom timestamp', LogLevel.INFO, timestamp="%H:%M:%S")
    logger.info('This should show custom timestamp')

    logger = Logger('no timestamp', LogLevel.INFO, timestamp=None)
    logger.info('This should show', 'no timestamp')

    print('=' * 20)

    logger = Logger(None)
    logger.info('This should no prefix')

    print('=' * 20)

    logger = Logger()
    logger.info('default logger print')


if __name__ == '__main__':
    test_func()
