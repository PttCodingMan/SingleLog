# SingleLog
[![Package Version](https://img.shields.io/pypi/v/SingleLog.svg)](https://pypi.python.org/pypi/SingleLog)
![PyPI - Downloads](https://img.shields.io/pypi/dm/SingleLog)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/SingleLog)
[![Python package](https://github.com/PttCodingMan/SingleLog/actions/workflows/python-package.yml/badge.svg)](https://github.com/PttCodingMan/SingleLog/actions/workflows/python-package.yml)

### A python logger, super easy to use and thread safe.

## Install
```
pip install SingleLog
```

## Tutorials
### Init
```python
log_level = Logger.INFO # default
# log_level = Logger.DEBUG
# log_level = Logger.TRACE
logger = Logger('demo', log_level)
```
### Display
```python
logger = Logger('demo')

logger.info(1)
logger.debug(2)
logger.trace(3)
```
Result
```Batchfile
[20210501 11:19:48][demo] 1
```

When the log level is set to ```Logger.DEBUG``` or ```Logger.TRACE```, the location will be displayed.

```python
logger = Logger('demo', Logger.TRACE)
logger.info('This is the description', 'demo')
logger.debug('This is the description', 'demo')
logger.trace('This is the description', 'demo')
```
Result
```Batchfile
[20211104 09:13:16][demo] This is the description [demo]
[20211104 09:13:16][demo][demo.py 7] This is the description [demo]
[20211104 09:13:16][demo][demo.py 8] This is the description [demo]
```

SingleLog Supports some common types to display. Such as list, dict and tuple.
```python
logger = Logger('demo')
logger.info('show int list', [101, 102, 103])
logger.info('show tuple', ('12', '14', '16'))
logger.info('data', {'1': 'value1', '2': 'value2'})
```
Result
```Batchfile
[20210501 12:14:48][demo] show int list [101 102 103]
[20210501 12:14:48][demo] show tuple (12 14 16)
[20210501 12:14:48][demo] data 
{
  "1": "value1",
  "2": "value2"
}

```

SingleLog supports args as parameter.  
It helps you to format your log message
```python
logger = Logger('demo')
logger.info('This is the description', 'value 0', 'value 1', 99)
```
Result
```Batchfile
[20210501 12:10:01][demo] This is the description [value 0] [value 1] [99]
```

### Handler
Sometimes, you want to catch the log message at higher level.  
Use log handler.
```python
def log_to_file(msg):
    with open('single_log.txt', 'a', encoding='utf8') as f:
        f.write(f'{msg}\n')


logger = Logger('INFO', Logger.INFO, handler=log_to_file)

logger.info('1')
logger.info(2)
logger.info('show value', 456)
```
Handler can also be a list.
```python
def log_to_file(msg):
    with open('single_log.txt', 'a', encoding='utf8') as f:
        f.write(f'{msg}\n')

def log_to_file2(msg):
    with open('single_log_2.txt', 'a', encoding='utf8') as f:
        f.write(f'{msg}\n')


logger = Logger('INFO', Logger.INFO, handler=[log_to_file, log_to_file2])

logger.info('1')
logger.info(2)
logger.info('show value', 456)
```
In this demo, the log message will display on the screen.  
Also you can find it in local file.
