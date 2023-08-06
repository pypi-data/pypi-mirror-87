import os
import time
from datetime import datetime, timedelta
from functools import wraps

from colorama import Fore, Style


class Timer:

    try:
        WIDTH, _ = os.get_terminal_size(0)
    except:
        WIDTH = 76

    DATETIME_FMT = f'{Fore.LIGHTCYAN_EX}%Y-%m-%d %H:%M:%S{Fore.RESET}'
    TIMER_COLOR = Fore.LIGHTGREEN_EX

    INFO = f'[{Fore.LIGHTBLUE_EX}{"INFO":8}{Fore.RESET}]| '
    ERROR = f'[{Fore.LIGHTRED_EX}{Style.BRIGHT}{"ERROR":8}{Style.RESET_ALL}]| '
    WARNING = f'[{Fore.LIGHTRED_EX}{"WARNING":8}{Fore.RESET}]| '

    def __init__(self, interval, start=None, is_error=False, exception=None, **kwargs):
        self.interval = interval
        self.start = start
        self.extra = kwargs
        self.is_error = is_error
        self.exception = exception
        if is_error:
            self._run_error_timer()
        else:
            self._run_default_timer()

    @staticmethod
    def interval(**kwargs):
        def decorator(method):
            seconds = timedelta(**kwargs).total_seconds()
            @wraps(method)
            def wrapper(*args, **kwargs):
                return method(*args, **kwargs, interval=seconds)
            return wrapper
        return decorator

    @classmethod
    def _format_seconds(cls, seconds):
        if seconds >= 60*60*24:
            return f'{cls.TIMER_COLOR}{round(seconds / (60*60*24), 2)}{Fore.RESET} days.'
        if seconds >= 60*60:
            return f'{cls.TIMER_COLOR}{round(seconds / (60*60), 2)}{Fore.RESET} hours.'
        if seconds >= 60:
            return f'{cls.TIMER_COLOR}{round(seconds / 60, 2)}{Fore.RESET} minutes.'
        return f'{cls.TIMER_COLOR}{round(seconds, 2)}{Fore.RESET} seconds.'

    def _divide(self, symbol, style=''):
        print(f'{style}{"":{symbol}<{self.WIDTH}}{Style.RESET_ALL}')

    def _sleep(self):
        now = datetime.now()
        interval = self.interval
        interval_format = self._format_seconds(seconds=interval)
        next_round = (now + timedelta(seconds=interval)).strftime(self.DATETIME_FMT)
        print(f'{self.INFO}sleep : {interval_format}')
        print(f'{self.INFO}next round : {next_round}')
        self._divide('=')
        time.sleep(interval)

    def _error_snap(self):
        now = datetime.now()
        interval = self.interval
        interval_format = self._format_seconds(seconds=interval)
        next_round = (now + timedelta(seconds=interval)).strftime(self.DATETIME_FMT)
        exception = self.exception or 'Caught an exception!'
        print(f'{self.ERROR}{exception}')
        print(f'{self.WARNING}restart at: {next_round}')
        self._divide('=')
        time.sleep(interval)

    def _display_consume(self):
        if self.start is None:
            return None
        consume = round(time.time() - self.start, 2)
        consume_format = self._format_seconds(seconds=consume)
        print(f'{self.INFO}consume: {consume_format}')

    def _display_extra(self):
        if not self.extra:
            return None
        for k, v in self.extra.items():
            if len(k) <= 8:
                print(f'[{Fore.LIGHTYELLOW_EX}{k.upper():8}{Fore.RESET}]| {Fore.CYAN}{v}{Fore.RESET}')
                continue
            print(f'{self.INFO}{Fore.CYAN}{k} - {v}{Fore.RESET}')
        self._divide('-', style=Style.DIM)

    def _run_error_timer(self):
        self._divide('=')
        self._display_extra()
        self._error_snap()

    def _run_default_timer(self):
        self._divide('=')
        self._display_extra()
        self._display_consume()
        self._sleep()

