import sys
import threading
import time

sys.path.insert(0, '../')

from SingleLog import Logger


def test_threading():
    def thread_log(thread_id):
        current_logger = Logger(f'logger-{thread_id}')
        for i in range(100):
            current_logger.info('show', i)

    thread_list = list()
    for i in range(50):
        t = threading.Thread(target=thread_log, args=(i,))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()


def test_threading_with_print():
    def thread_log(thread_id):
        current_logger = Logger(f'logger-{thread_id}')
        for i in range(50):
            current_logger.info('show', i)
            print(f'logger-{thread_id} print {i}')

    thread_list = list()
    for i in range(10):
        t = threading.Thread(target=thread_log, args=(i,))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()


if __name__ == '__main__':
    import SingleLog

    # print(len(SingleLog.SingleLog.enable_loggers))
    test_threading()
    # print(len(SingleLog.SingleLog.enable_loggers))
