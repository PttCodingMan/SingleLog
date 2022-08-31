import builtins
import json
from typing import List, Callable

old_print = builtins.print


def merge_msg(msg, frame: bool = True) -> str:
    if isinstance(msg, (list, dict)):
        msg = f'{json.dumps(msg, indent=2, ensure_ascii=False)}'
    elif isinstance(msg, tuple):
        msg = f'{json.dumps(msg, indent=2, ensure_ascii=False)}'
        msg = msg[1:-1]
        if frame:
            msg = f'({msg})'
    else:
        if isinstance(msg, str):
            pass
        else:
            msg = str(msg)
        if frame:
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


def output_file(handlers: List[Callable], total_message: str) -> None:
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
