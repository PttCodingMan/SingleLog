from SingleLog.log import Logger
from SingleLog.log import LoggerLevel

if __name__ == '__main__':
    logger = Logger('demo')

    logger.info('data', {'1': 'value1', '2': 'value2'})
    logger.info(1)
    logger.info(1, 2, 3, 4, 5)
    logger.info('show int', 100)
    logger.info('show str', 'this is a string')
    logger.info('show int list', [101, 102, 103])
    logger.info('show string list', ['101', '102', '103'])
    logger.info('show tuple', ('12', '14', '16'))

    logger.info('des', 'value0', 'value1', 'value2')

    print('=' * 20)

    logger = Logger('TRACE', Logger.TRACE)

    logger.info('This should be 3 to print')
    logger.debug('This should be 3 to print')
    logger.trace('This should be 3 to print')

    print('=' * 20)

    logger = Logger('DEBUG', Logger.DEBUG)

    logger.info('This should be 2 to print')
    logger.debug('This should be 2 to print')
    logger.trace('This should NOT be print')

    print('=' * 20)

    logger = Logger('INFO')

    logger.info('This should be 1 to print')
    logger.debug('This should NOT be print')
    logger.trace('This should NOT be print')

    print('=' * 20)

    logger = Logger('SILENT', Logger.SILENT)

    logger.info('This should NOT be print')
    logger.debug('This should NOT be print')
    logger.trace('This should NOT be print')

    print('=' * 20)

    logger = Logger('skip', Logger.INFO, skip_repeat=True)
    logger.info('This should only print once')
    logger.info('This should only print once')
    logger.info('This should only print once')

    print('=' * 20)

    logger = Logger('custom timestamp', Logger.INFO, timestamp="%H:%M:%S")
    logger.info('This should show custom timestamp')

    logger = Logger('no timestamp', Logger.INFO, timestamp=None)
    logger.info('This should show no timestamp')

    print('=' * 20)

    logger = Logger(None)
    logger.info('This should no prefix')

    print('=' * 20)

    enable_handler_test = False
    if enable_handler_test:
        def log_to_file(msg):
            with open('single_log.txt', 'a', encoding='utf8') as f:
                f.write(f'{msg}\n')

        def log_to_file2(msg):
            with open('single_log_2.txt', 'a', encoding='utf8') as f:
                f.write(f'{msg}\n')


        logger = Logger('INFO', Logger.INFO, handler=[log_to_file, log_to_file2])

        logger.info('1')
        logger.info(2)
        logger.info('show value', 456)

    enable_threading_test = False
    if enable_threading_test:

        import threading


        def thread_log(thread_id):
            current_logger = Logger(f'logger-{thread_id}')
            for i in range(1000):
                current_logger.info('show', i)


        thread_list = list()
        for i in range(100):
            t = threading.Thread(target=thread_log, args=(i,))
            thread_list.append(t)
            t.start()

        for t in thread_list:
            t.join()
