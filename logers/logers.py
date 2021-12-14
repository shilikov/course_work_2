from datetime import datetime
from time import time
import logging
from logging.handlers import RotatingFileHandler
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
            f"date: {date}\n"
              f"time: {times}\n"
              f"name: {func_name}\n"
              f"args: {args, kwargs}\n"
              f"result: {result}\n"
              f'функция работала {elapsed} секунд(ы)'
              )


        return result
    return loger



def log(message, sep='\n'):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
    if type(message) in [list, dict, tuple, set]:
        message = [f'{now} - {x}' for x in message]
        print(*message, sep=sep)
    else:
        print(f'{now} - {message}', sep=sep)



