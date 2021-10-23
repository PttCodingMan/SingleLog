# SingleLog
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
# log_level = Logger.DEBUG
# log_level = Logger.TRACE
logger = Logger(prefix, log_level)
```
### Display
```python
prefix = 'example'
log_level = Logger.INFO
logger = Logger(prefix, Logger.INFO)

logger.info(1)
logger.debug(2)
logger.trace(3)
```
It will display
```python
[20210501 11:19:48][example] 1
```
Also, I provide an interface that takes the log level as a parameter.  
You can change the log level programmably.
```python
logger = Logger('example', Logger.INFO)

logger.log(Logger.INFO, 'Hi')
logger.log(Logger.DEBUG, 'Hi')
```
It will display
```python
[20210501 11:59:52][example] Hi
```
Single logger supports args as parameter.  
It helps you to format your log message
```python
logger = Logger('example', Logger.INFO)
logger.log(Logger.INFO, 'This is the description', 'value 0', 'value 1', 99)
```
It will display
```python
[20210501 12:10:01][example] This is the description [value 0] [value 1] [99]
```

Single logger supports many types to display.  
For example: list, dict and tuple
```python
logger = Logger('example', Logger.INFO)
logger.info('show int list', [101, 102, 103])
logger.info('show tuple', ('12', '14', '16'))
logger.info('data', {'1': 'value1', '2': 'value2'})
```
It will display
```python
[20210501 12:14:48][example] show int list [101 102 103]
[20210501 12:14:48][example] show tuple (12 14 16)
[20210501 12:14:48][example] data 
{
  "1": "value1",
  "2": "value2"
}
```
### handler
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
In this example, the log message will display on the screen.  
Also you can find it in local file.
