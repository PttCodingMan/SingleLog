import sys
import threading

sys.path.insert(0, '../')

from SingleLog import Logger


def test_do():
    def thread_log(thread_id):
        current_logger = Logger(f'logger-{thread_id}')
        for i in range(1000):
            current_logger.info('show', i)

    thread_list = list()
    for i in range(100):
        t = threading.Thread(target=thread_log, args=(i,))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()
