import sys
from itertools import permutations

sys.path.insert(0, '../')

from SingleLog import LogLevel
from SingleLog import Logger


def test_func():
    logger = Logger('test_func')

    logger.debug('start')
    logger.info('hi')

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

    print('=' * 20)
    logger.info('Twitter already post today')


def test_first_test():
    from SingleLog import SingleLog

    api_list = [
        'print',
        'info',
        'stage'
    ]

    for i, api_test in enumerate(permutations(api_list)):
        SingleLog.last_logger = None
        logger = Logger(f'test-{i}')
        for api in api_test:
            if api == 'print':
                print(f'test-{i} print')
                print(f'test-{i} print')
            if api == 'info':
                logger.info('info')
                logger.info('info')
            if api == 'stage':
                logger.stage(f'test-{i} stage')
                logger.stage(f'test-{i} stage')

        print('=' * 20)


def test_error_new_line():
    logger = Logger('test_error_new_line')
    Logger('1').info('hi')
    Logger('2').info('hi')
    Logger('3').info('hi')


if __name__ == '__main__':
    test_first_test()
    # test_func()
    # test_error_new_line()

    # logger = Logger('test')
    # logger.info('hi')

    # print('hi')
