import os
import sys
import time
import ctypes
from enum import Enum


MOUSEEVENTF_LEFTDOWN = 2
MOUSEEVENTF_LEFTUP = 4


def check_version() -> None:
    if sys.version_info < (3, 9, 7):
        print(u'Для работы требуется версия Python 3.9.7 и выше')
        time.sleep(4)
        exit()
        raise Exception(u'Для работы требуется версия Python 3.9.7 и выше')


def create_dirs(path_graphlog) -> None:
    if not (path_graphlog.exists() and path_graphlog.is_dir()):
        path_graphlog.mkdir()


def limit(value: int, low: int = 0, high: int = 255) -> int:
    """Лимиты для переданного значения"""
    return min(max(value, low), high)


def lclick(x: int, y: int) -> None:
    win32api = ctypes.windll.user32
    win32api.SetCursorPos(x, y)
    win32api.mouse_event(MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.3)
    win32api.mouse_event(MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def exit_from_program(code: int = 0, close: bool = False) -> None:
    if not close:
        input('\n---------------   END   ---------------')
    else:
        time.sleep(1)
    try:
        sys.exit(code)
    except SystemExit:
        os._exit(code)


class ResultType(Enum):
    SUCCESS = 'успешно'
    PARTIAL_SUCCESS = 'успешно случайно'
    WRONG = 'неправильно'
