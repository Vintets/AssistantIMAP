import os
import sys


def clear_consol() -> None:  # очищаем консоль
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')
