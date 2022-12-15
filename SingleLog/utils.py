import builtins
import json
from typing import List, Callable

old_print = builtins.print


def merge_msg(msg, frame: bool = True) -> str:
    if msg is None:
        return 'null'

    if not isinstance(msg, str):

        is_bool = isinstance(msg, bool)
        if is_bool:
            return 'true' if msg else 'false'

        is_tuple = isinstance(msg, tuple)
        is_set = isinstance(msg, set)
        if is_tuple or is_set:
            msg = list(msg)

        try:
            msg = f'{json.dumps(msg, indent=2, ensure_ascii=False)}'
            dump_msg = True
        except:
            dump_msg = False

        if not dump_msg:
            msg = f'{msg}'

        if is_tuple or is_set:
            msg = msg[1:-1]
            if frame:
                if is_tuple:
                    msg = f'({msg})'
                elif is_set:
                    msg = f'{{{msg}}}'

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
