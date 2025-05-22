import os
import sys
import time
from enum import Enum


def check_version() -> None:
    if sys.version_info < (3, 9, 7):
        print(u'Для работы требуется версия Python 3.9.7 и выше')
        time.sleep(4)
        exit()
        raise Exception(u'Для работы требуется версия Python 3.9.7 и выше')


def create_dirs(path_graphlog) -> None:
    if not (path_graphlog.exists() and path_graphlog.is_dir()):
        path_graphlog.mkdir()


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
