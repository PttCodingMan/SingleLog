import sys

sys.path.insert(0, '../')

from SingleLog import Logger

if __name__ == '__main__':
    logger = Logger('test')

    logger.info('hi this is a normal info')
    logger.warn('hi this is a normal warn')
    logger.error('hi this is a normal error')

    logger.warn('hi this is a msg', 'warn msg')
    logger.warn('hi this is a msg', 'warn msg', '1', '2')
    logger.warn('hi this is a msg', 'warn msg', '1', '2', '3')

    logger.error('hi this is a msg', 'error msg')
    logger.error('hi this is a msg', 'error msg', '1', '2')
    logger.error('hi this is a msg', 'error msg', '1', '2', '3')
