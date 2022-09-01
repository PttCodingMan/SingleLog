# SingleLog
[![Package Version](https://img.shields.io/pypi/v/SingleLog.svg)](https://pypi.python.org/pypi/SingleLog)
[![test](https://github.com/PttCodingMan/SingleLog/actions/workflows/test.yml/badge.svg)](https://github.com/PttCodingMan/SingleLog/actions/workflows/test.yml)
![PyPI - Downloads](https://img.shields.io/pypi/dm/SingleLog)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/SingleLog)

### SingleLog is a simple library for logging. It is designed to make logging easier.
### It can format your data and output it to the console or file.
### It can also log your event status step by step.

## Quick View

### Stage Method
You can use stage method to display the log step by step.  
And don't need to worry about the default print function will print the log in the same line.

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

![](https://imgur.com/0nYvBcd.gif)

### Automatic Data Format
SingleLog Supports some common types to display in format. Such as list, dict and tuple etc.

```python
from SingleLog import Logger

logger = Logger('demo')
logger.info('show int list', [101, 102, 103])
logger.info('show tuple', ('12', '14', '16'))
logger.info('data', {'1': 'value1', '2': 'value2'})
```

![](https://imgur.com/EVudUBb.jpg)

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

## Advanced Usage
You can use logger to display the log in different ways.

### Skip Repeated Message
You can skip repeated message.  
The following logger will display only one message.

```python
from SingleLog import Logger

logger = Logger('demo', skip_repeat=True)

logger.info('hello world')
logger.info('hello world')
logger.info('hello world')
```

### Stage Separator

You can change stage separator to display the log.

```python
import time
from SingleLog import Logger

logger = Logger('demo', stage_sep='-')

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
```

![](https://imgur.com/6FZoLYD.jpeg)

### Stage Color
You can change stage color.  
You can find the more color information from [Colorama](https://github.com/tartley/colorama).

```python
from colorama import Fore
from SingleLog import Logger

logger = Logger('demo', stage_color_list = [Fore.GREEN, Fore.YELLOW])

logger.info('start')
for i in range(10):
    logger.stage(i)
```

![](https://imgur.com/B06f3iM.jpeg)

### Timestamp
You can change timestamp format.

```python
from SingleLog import Logger

logger = Logger('demo')
logger.info('default timestamp')

logger = Logger('demo', timestamp='%Y-%m-%d %H:%M:%S')
logger.info('custom timestamp')
```

![](https://imgur.com/P0NGMf6.jpeg)

### Keyword of success and failure
You can use keyword of success and failure to display the log.  

The keywords in `key_word_success`, will be displayed in green color.  
The keywords in `key_word_failure`, will be displayed in red color.  

```python
from SingleLog import Logger

logger = Logger('demo', key_word_success=['custom_success'], key_word_fails=['custom_fail'])

logger.info('do something')
logger.stage('custom_success')
logger.stage('custom_fail')
```

![](https://imgur.com/fjymmFq.jpeg)

## License
MIT License