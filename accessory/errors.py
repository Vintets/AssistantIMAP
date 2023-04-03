import os
from accessory import cprint
from typing import Optional


class ParseStrDateError(Exception):
    """Error parsing str date. Incorrect format"""

    def __init__(self, msg: Optional[str] = None) -> None:
        self.msg = msg if msg is not None else '<<ParseStrDateError>>'

    def __str__(self) -> None:
        return self.msg


class InvalidFolderNameError(Exception):
    """ Invalid Name Folder FROM_FOLDER or TARGET_FOLDER"""

    pass


def process_critical_exception(message: Optional[str] = None) -> None:
    """Prints message, describing critical situation, and exit"""

    if message is not None:
        print(message)
    cprint('14{dash}   ^12_ERROR   ^14_{dash}'.format(dash='-' * 20))
    os._exit(1)
