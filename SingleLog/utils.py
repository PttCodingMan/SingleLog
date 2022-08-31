import json


def _merge(msg, frame: bool = True) -> str:
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