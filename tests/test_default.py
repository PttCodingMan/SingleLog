import sys

sys.path.insert(0, '../')

from SingleLog import DefaultLogger, LogLevel


def test_default():
    logger = DefaultLogger('test', LogLevel.DEBUG)

    logger.info('123', '456')
    logger.info('123', '456', '789')
    logger.info('test', [1, 3, 4, 5, 6, 7, 8, 9, 0])
    logger.info('dict', {'1': 'value1', '2': 'value2'})

    logger.debug('123', '456')
    logger.debug('123', '456', '789')

    logger.error('123', '456')

if __name__ == '__main__':
    test_default()
