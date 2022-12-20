import sys
import time

sys.path.insert(0, '../')

from SingleLog import Logger

if __name__ == '__main__':
    logger = Logger('test')

    logger.info('start')
    start = time.time()
    for i in range(100000):
        logger.info(i)

    end = time.time()

    logger.info(f'{end - start} seconds')

    # 1.5678861141204834 seconds (100000) 2022-08-31
