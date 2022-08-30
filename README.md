# SingleLog
[![Package Version](https://img.shields.io/pypi/v/SingleLog.svg)](https://pypi.python.org/pypi/SingleLog)
![PyPI - Downloads](https://img.shields.io/pypi/dm/SingleLog)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/SingleLog)
[![Python package](https://github.com/PttCodingMan/SingleLog/actions/workflows/python-package.yml/badge.svg)](https://github.com/PttCodingMan/SingleLog/actions/workflows/python-package.yml)

### A single python logger, super easy to use and thread safe.

## Install
```
pip install SingleLog -U
```

## Tutorials
### Init
```python
from SingleLog import Logger
from SingleLog import LogLevel

log_level = LogLevel.INFO # default
# log_level = LogLevel.DEBUG
# log_level = LogLevel.TRACE
logger = Logger('demo', log_level)
```
```
### Display
```python
from SingleLog import Logger

logger = Logger('demo')

logger.info(1)
logger.debug(2)
logger.trace(3)
```
Result
```Batchfile
[20210501 11:19:48][demo] 1
```

When the log level is set to ```LogLevel.DEBUG``` or ```LogLevel.TRACE```, the location will be displayed.

```python
from SingleLog import Logger
from SingleLog import LogLevel

logger = Logger('demo', LogLevel.TRACE)
logger.info('This is the description', 'demo')
logger.debug('This is the description', 'demo')
logger.trace('This is the description', 'demo')
```
Result
```Batchfile
[20211104 09:13:16][demo][demo.py 6] This is the description [demo]
[20211104 09:13:16][demo][demo.py 7] This is the description [demo]
[20211104 09:13:16][demo][demo.py 8] This is the description [demo]
```

SingleLog Supports some common types to display in format. Such as list, dict and tuple.
```python
from SingleLog import Logger

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

Supports the `do` method that you can call it, when you finish the work.

```python
import time
from SingleLog import Logger

logger = Logger('demo')
logger.do_info('do something')
time.sleep(1)
logger.done('ok')
```

Output
```Batchfile
[08.30 10:36:57][logger] do something ... ok
```

### Handler
Sometimes, you want to catch the log message at higher level.  
Use log handler.
```python
from SingleLog import Logger
from SingleLog import LogLevel

def log_to_file(msg):
    with open('single_log.txt', 'a', encoding='utf8') as f:
        f.write(f'{msg}\n')


logger = Logger('INFO', LogLevel.INFO, handler=log_to_file)

logger.info('1')
logger.info(2)
logger.info('show value', 456)
```
Handler can also be a list.
```python
from SingleLog import Logger
from SingleLog import LogLevel

def log_to_file(msg):
    with open('single_log.txt', 'a', encoding='utf8') as f:
        f.write(f'{msg}\n')

def log_to_file2(msg):
    with open('single_log_2.txt', 'a', encoding='utf8') as f:
        f.write(f'{msg}\n')


logger = Logger('INFO', LogLevel.INFO, handler=[log_to_file, log_to_file2])

logger.info('1')
logger.info(2)
logger.info('show value', 456)
```
In this demo, the log message will display on the screen.  
Also you can find it in local file.

You can check all the demo in [demo.py](https://github.com/PttCodingMan/SingleLog/blob/master/demo.py).

## License
MIT License