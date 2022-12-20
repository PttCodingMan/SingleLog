import sys

sys.path.insert(0, '../')

from SingleLog import DefaultLogger


def test_default():
    logger = DefaultLogger('test')

    logger.info('123', '456')

    logger.info('123', '456', '789')

    logger.info('test', [1, 3, 4, 5, 6, 7, 8, 9, 0])


if __name__ == '__main__':
    test_default()
