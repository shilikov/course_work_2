from datetime import datetime
from time import time
from typing import Callable, Any
from pprint import pprint


def log_to_console(func) -> Callable:
    def loger(*args, **kwargs) -> Any:
        date = datetime.date(datetime.now())
        times = datetime.time(datetime.now())
        func_name = func.__name__
        started_at = time()
        result = func(*args, **kwargs)
        ended_at = time()
        elapsed = round(ended_at - started_at, 4)
        print()

        pprint(
            f"date: {date} time: {times} "
            f"name: {func_name} "
            f"args: {args, kwargs} "
            f"result: {result}"
            f"'функция работала {elapsed} секунд(ы)'")
        return result

    return loger


def log(message, sep='\n'):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
    if type(message) in [list, dict, tuple, set]:
        message = [f'{now} - {x}' for x in message]
        print(*message, sep=sep)
    else:
        print(f'{now} - {message}', sep=sep)
