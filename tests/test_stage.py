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

    logger.info('do something')
    logger.stage('bug')
    logger.info('do something')
    logger.stage('success')

    logger.info('start')
    for i in range(1, 8):
        logger.info('start', i)
        for ii in range(i):
            logger.stage(ii)


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


def test_stage_4():
    loglevels = [
        LogLevel.INFO,
        LogLevel.DEBUG,
    ]

    for loglevel in loglevels:
        logger = Logger('demo', loglevel)

        logger.info('do something')
        logger.stage(1)
        logger.debug(1.1)
        logger.stage(2)
        logger.debug(2.5)
        logger.stage(3)
        logger.debug(3.6)
        logger.stage(4)

        logger.info('===================')


if __name__ == '__main__':
    # test_stage()
    # test_stage_2()
    # test_stage_3()
    test_stage_4()
