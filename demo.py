
from single_log.log import Logger

if __name__ == '__main__':
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