import sys
import time

sys.path.insert(0, '../')

from SingleLog import Logger, LogLevel


def test_do():

    def log_to_file(msg):
        with open('./single_log_1.txt', 'a', encoding='utf-8') as f:
            f.write(f'{msg}\n')

    def log_to_file2(msg):
        with open('./single_log_2.txt', 'a', encoding='utf-8') as f:
            f.write(f'{msg}\n')

    logger = Logger('INFO', handler=[log_to_file, log_to_file2])

    logger.info('1')
    logger.info(2)
    logger.info('show value', 456)
