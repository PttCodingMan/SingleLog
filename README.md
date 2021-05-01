# logger
[![Package Version](https://img.shields.io/pypi/v/SingleLog.svg)](https://pypi.python.org/pypi/SingleLog)
![PyPI - Downloads](https://img.shields.io/pypi/dm/SingleLog)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/SingleLog)

### A python logger, super easy to use and thread safe.

## Install
```
pip install SingleLog
```

## Tutorials
### Init
```python
prefix = 'example'
log_level = Logger.INFO
logger = Logger(prefix, log_level)
```
### Display
```
prefix = 'example'
log_level = Logger.INFO
logger = Logger(prefix, Logger.INFO)

logger.info(1)
logger.debug(2)
logger.trace(3)
```
It will display
```
[20210501 11:19:48][example] 1
```
Also, I provide an interface that takes the log level as a parameter.  
You can change the log level programmably.
```
logger = Logger('example', Logger.INFO)

logger.log(Logger.INFO, 'Hi')
logger.log(Logger.DEBUG, 'Hi')
```
It will display
```
[20210501 11:59:52][example] Hi
```
### handler
Sometimes, you want to catch the log message at higher level.  
Use log handler
```
def log_to_file(msg):
    with open('single_log.txt', 'a', encoding='utf8') as f:
        f.write(f'{msg}\n')


logger = Logger('INFO', Logger.INFO, handler=log_to_file)

logger.info('1')
logger.info(2)
logger.info('show value', 456)
```
In this example, the log message will display on the screen.  
Algo you can find it in local file.
