import time

from SingleLog import Logger
from SingleLog.log import Logger as old_logger

if __name__ == '__main__':
    logger = Logger('test')

    logger.info('start')
    start = time.time()
    for i in range(1000):
        logger.info(i)

    end = time.time()

    logger.info(f'{end - start} seconds')

