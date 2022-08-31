import time

from SingleLog import Logger

if __name__ == '__main__':
    logger = Logger('test')

    logger.info('start')
    start = time.time()
    for i in range(100000):
        logger.info(i)

    end = time.time()

    logger.info(f'{end - start} seconds')

    # 1.9021880626678467 seconds (100000) 2022-08-31

