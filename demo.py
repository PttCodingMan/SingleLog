from SingleLog.log import Logger

if __name__ == '__main__':
    logger = Logger('INFO', Logger.INFO)

    logger.show('1', 2, 3, 4, 5)
    logger.show(Logger.INFO, 'show int', 100)
    logger.show(Logger.INFO, 'show str', 'this is a string')
    logger.show(Logger.INFO, 'show int list', [101, 102, 103])
    logger.show(Logger.INFO, 'show string list', ['101', '102', '103'])
    logger.show(Logger.INFO, 'show tuple', ('12', '14', '16'))

    logger.show(Logger.INFO, 'des', 'value0', 'value1', 'value2')

    print('=' * 20)

    logger = Logger('TRACE', Logger.TRACE)

    logger.show(Logger.INFO, 'It should be print')
    logger.show(Logger.DEBUG, 'It should be print')
    logger.show(Logger.TRACE, 'It should be print')

    print('=' * 20)

    logger = Logger('DEBUG', Logger.DEBUG)

    logger.show(Logger.INFO, 'It should be print')
    logger.show(Logger.DEBUG, 'It should be print')
    logger.show(Logger.TRACE, 'It should NOT be print')

    print('=' * 20)

    logger = Logger('INFO', Logger.INFO)

    logger.show(Logger.INFO, 'It should be print')
    logger.show(Logger.DEBUG, 'It should NOT be print')
    logger.show(Logger.TRACE, 'It should NOT be print')

    print('=' * 20)

    logger = Logger('SILENT', Logger.SILENT)

    logger.show(Logger.INFO, 'It should NOT be print')
    logger.show(Logger.DEBUG, 'It should NOT be print')
    logger.show(Logger.TRACE, 'It should NOT be print')

    print('=' * 20)


    def log_to_file(msg):
        with open('single_log.txt', 'a', encoding='utf8') as f:
            f.write(f'{msg}\n')


    logger = Logger('INFO', Logger.INFO, handler=log_to_file)

    logger.show(Logger.INFO, '1')
    logger.show(Logger.INFO, 2)
    logger.show(Logger.INFO, 'show value', 456)

    import threading


    def thread_log(thread_id):
        current_logger = Logger(f'logger-{thread_id}', Logger.INFO)
        for i in range(1000):
            current_logger.show(Logger.INFO, 'show', i)


    thread_list = list()
    for i in range(100):
        t = threading.Thread(target=thread_log, args=(i,))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()
