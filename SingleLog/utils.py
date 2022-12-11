import atexit
import builtins
import json
from typing import List, Callable

old_print = builtins.print


def merge_msg(msg, frame: bool = True) -> str:
    if not isinstance(msg, str):

        is_tuple = isinstance(msg, tuple)
        try:
            msg = f'{json.dumps(msg, indent=2, ensure_ascii=False)}'
            dump_msg = True
        except:
            dump_msg = False

        if not dump_msg:
            msg = f'{msg}'

        if is_tuple:
            msg = msg[1:-1]
            if frame:
                msg = f'({msg})'

    elif frame:
        msg = f'[{msg}]'

    return msg


def output_screen(total_message: str) -> None:
    for i in range(2):
        try:
            old_print(total_message, end='')
            break
        except UnicodeEncodeError:
            if i == 1:
                old_print('sorry, logger can not print the message')
                break
            total_message = total_message.encode("utf-16", 'surrogatepass').decode("utf-16", "surrogatepass")


def callback(handlers: List[Callable], total_message: str) -> None:
    for i in range(2):
        try:
            for handler in handlers:
                handler(total_message)
            break
        except UnicodeEncodeError:
            if i == 1:
                old_print('sorry, logger can not print the message')
                break
            total_message = total_message.encode("utf-16", 'surrogatepass').decode("utf-16", "surrogatepass")
