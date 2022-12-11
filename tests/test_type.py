from SingleLog import Logger

if __name__ == '__main__':
    logger = Logger('test')

    logger.info('str', 'str')
    logger.info('int', 1)
    logger.info('float', 1.1)
    logger.info('list', [1, 2, 3])
    logger.info('dict', {'a': 1, 'b': 2})
    logger.info('tuple', (1, 2, 3))
    logger.info('set', {1, 2, 3})
    logger.info('bool', True)
    logger.info('None', None)
    logger.info('function', print)
    logger.info('class', Logger)
    logger.info('object', logger)

