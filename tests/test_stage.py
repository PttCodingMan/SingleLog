import sys
import time

sys.path.insert(0, '../')

from SingleLog import Logger, LogLevel


def test_stage():
    logger = Logger('rocket')

    logger.info('Init rocket launch proces')
    time.sleep(0.5)
    logger.stage('complete!')

    logger.info('Start the countdown')
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


def test_stage_2():
    logger = Logger('demo')

    logger.info('start')
    for i in range(10):
        logger.stage(i)


def test_stage_3():

    loglevels = [
        LogLevel.INFO,
        LogLevel.DEBUG,
    ]

    for loglevel in loglevels:
        logger = Logger(f'demo-{loglevel}', loglevel)

        logger.debug('start')
        for i in range(10):
            logger.stage(i)
            if i == 5:
                print('someone walk in!')

        logger.debug('end')


if __name__ == '__main__':
    test_stage()