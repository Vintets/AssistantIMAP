#!/usr/bin/env python3

import sys

try:
    from configs.config import PATH_LOGS, LOGGER_NAME_MODULE, LOGGER_PREFIX
except ModuleNotFoundError:
    from pathlib import Path

    PATH_LOGS = Path('.')
    LOGGER_PREFIX = 'test'
    LOGGER_NAME_MODULE = True
from loguru import logger


FILENAME_LOG_MAIN = PATH_LOGS / f'{LOGGER_PREFIX}_{{time:YYYY-MM-DD}}.log'
FILENAME_LOG_ERR = PATH_LOGS / f'{LOGGER_PREFIX}_error_{{time:YYYY-MM-DD}}.log'


# исправление цвета INFO на windows с серой консолью
logger.level('INFO', color='<light-white><bold>')
logger.level('CRITICAL', color='<RED><white><bold>')

# добавляем свои уровни 'FAIL'
logger.level('FAIL', no=27, color='<light-magenta>', icon='@')

# удаляем начальный логгер и создаём свой базовый логгер с уровнем default LOGURU_LEVEL 'DEBUG'
logger.remove()
name_module = '{name}-' if LOGGER_NAME_MODULE else ''
new_format = '<light-blue>{time:YYYY-MM-DD HH:mm:ss.SSS}</light-blue> | <lvl>{level: <8}</lvl> | <cyan>%s{line}</cyan>- <lvl>{message}</lvl>' % name_module
logger.add(sys.stdout, format=new_format)

# добавляем логгеры с дефолтным форматированием для вывода в файлы
logger.add(FILENAME_LOG_MAIN,
           filter=lambda record: record['level'].no <= 30,
           rotation='00:00',
           compression='zip',
           delay=True)
logger.add(FILENAME_LOG_ERR,
           filter=lambda record: record['level'].no >= 30,
           rotation='00:00',
           compression='zip',
           delay=True)


def exemples() -> None:
    logger.trace('Hello, World (trace)!')
    logger.debug('Hello, World (debug)!')
    logger.info('Hello, World (info)!')
    logger.success('Hello, World (success)!')
    logger.warning('Hello, World (warning)!')
    logger.error('Hello, World (error)!')
    logger.critical('Hello, World (critical)!')
    logger.log('FAIL', 'No data recorded!')
    print()


def create_dir_log() -> None:
    if not (PATH_LOGS.exists() and PATH_LOGS.is_dir()):
        PATH_LOGS.mkdir()


create_dir_log()

if __name__ == '__main__':
    import os
    width = 120
    hight = 50
    # os.system('color 71')
    os.system('mode con cols=%d lines=%d' % (width, hight))
    os.system('powershell -command "&{$H=get-host;$W=$H.ui.rawui;$B=$W.buffersize;$B.width=%d;$B.height=%d;$W.buffersize=$B;}"' % (width, 4000))
    exemples()
