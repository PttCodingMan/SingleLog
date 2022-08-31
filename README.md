# SingleLog
[![Package Version](https://img.shields.io/pypi/v/SingleLog.svg)](https://pypi.python.org/pypi/SingleLog)
[![test](https://github.com/PttCodingMan/SingleLog/actions/workflows/test.yml/badge.svg)](https://github.com/PttCodingMan/SingleLog/actions/workflows/test.yml)
![PyPI - Downloads](https://img.shields.io/pypi/dm/SingleLog)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/SingleLog)


### A single python logger, super easy to use and thread safe.

## Install
```
pip install SingleLog -U
```

## Basic Usage
```python
from SingleLog import Logger

logger = Logger('demo')

logger.info('hello world')
```

### Log Levels
You can set the [LogLevel](https://github.com/PttCodingMan/SingleLog/blob/master/SingleLog/log.py) of the logger.

- `info`: Confirmation that things are working as expected.
- `debug`: Detailed information, usually of interest only when diagnosing problems.
- `trace`: Detailed information on the flow through the system.


```python
from SingleLog import Logger
from SingleLog import LogLevel

logger = Logger('demo', log_level=LogLevel.DEBUG)

logger.info('you can see it, when log_level is set to INFO, DEBUG and TRACE')
logger.debug('you can see it, when log_level is set to DEBUG and TRACE')
logger.trace('you can see it, when log_level is set to TRACE')
```

## Data automatically format
SingleLog Supports some common types to display in format. Such as list, dict and tuple etc.

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

### Stage method
You can use stage method to display the log.

```python
import time
from SingleLog import Logger

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
```

![](https://imgur.com/rKs6N2I.jpeg)

### Logger Handler
You can use logger handler to handle the log.
```python
from SingleLog import Logger

def log_to_file(msg):
    with open('single_log.txt', 'a', encoding='utf8') as f:
        f.write(f'{msg}\n')


logger = Logger('Handle', handler=log_to_file)

logger.info('1')
logger.info(2)
logger.info('show value', 456)
```
Handler also supports list.
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
Also you can find it in single_log.txt and single_log_2.txt.

## License
MIT License