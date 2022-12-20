import logging
from sys import stdout

from SingleLog import Logger

logging.basicConfig(level=logging.INFO)
logging.debug('debug')


if __name__ == '__main__':
    logger = Logger('test')
    logger.info('hi this is a normal info')
    # logger.stage('info stage')
    #
    # logging.info('info')
