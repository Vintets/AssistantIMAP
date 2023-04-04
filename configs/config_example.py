from pathlib import Path


IMAP_SERVER = 'imap.yandex.ru'
MAIL_LOGIN = 'login'
MAIL_PASSW = 'password'

FROM_FOLDER = 'Входящие'
TARGET_FOLDER = 'Archive_2022'
DATE_START = '01.02.2023'
DATE_END = '01.03.2023'
ONLY_COPY = True

CLOSECONSOLE = True
LOGGER_NAME_MODULE = True
EXCEPTION_TRACE = False

PATH_LOGS = Path('logs')
