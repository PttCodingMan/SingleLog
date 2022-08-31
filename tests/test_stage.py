import sys
import time

sys.path.insert(0, '../')

from SingleLog import Logger


def test_do():
    logger = Logger('rocket')

    logger.info('Init rocket launch proces')
    time.sleep(1.5)
    logger.stage('complete!')

    logger.info('Start the countdown')
    time.sleep(1)
    logger.stage('3')
    time.sleep(1)
    logger.stage('2')
    time.sleep(1)
    logger.stage('1')
    time.sleep(1)
    logger.stage('fire!')
    logger.info('Launch complete')

    logger.info('Init rocket launch proces, again')
    logger.stage('complete!')
    print('someone walk in!')
    print('aaaaaa')

    logger.info("Don't worry, logger will be fine.")


if __name__ == '__main__':
    test_do()
