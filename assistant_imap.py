#!/usr/bin/env python

"""
Проект AssistantIMAP
Перемещение писем между папок IMAP
/*******************************************************
 * Written by Vintets <programmer@vintets.ru>, April 2023
 * This file is part of AssistantIMAP project.
*******************************************************/

# for python 3.9.7 and over
"""

import sys
import os
import time
import json
from datetime import datetime, date, timedelta, time as dt_time
from imaplib import IMAP4_SSL
import email
from progress.bar import IncrementalBar
from configs import config
import errors as err
from accessory import (authorship, clear_console, cprint,
                       check_version, create_dirs, exit_from_program,
                       logger, imap_utf7)


__version_info__ = ('4', '0', '1')
__version__ = '.'.join(__version_info__)
__author__ = 'master by Vint'
__title__ = '--- AssistantIMAP ---'
__copyright__ = 'Copyright 2023 (c)  bitbucket.org/Vintets'


def title_operation():
    if config.ONLY_COPY:
        title = ('Копирование', 'копирования', 'скопированы')
    else:
        title = ('Перемещение', 'переноса', 'перемещены')
    return title


def create_progressbar():
    bar = IncrementalBar(title_operation()[0], max=len(mylist), suffix='%(index)d/%(max)d [%(percent)d%%]')
    bar.hide_cursor = False
    bar._hidden_cursor = False
    bar.width = 50
    bar.empty_fill = '·'
    return bar


def chunks(L, n):
    """ Yield successive n-sized chunks from L."""

    for i in range(0, len(L), n):
        yield L[i:i+n]


def move_msg_uids(imap, mail_uids, target_folder, count=500):
    """ Faster ~10 times than move by one."""

    bar = create_progressbar()
    mail_uids = [x.decode() for x in mail_uids]
    for uids_part in chunks(mail_uids, count):
        uids_part_str = ','.join(uids_part)
        uids_part_str = uids_part_str.encode()
        copy_res = imap.uid('copy', uids_part_str, f'"{target_folder}"')
        if (not config.ONLY_COPY) and copy_res[0] == 'OK':
            imap.uid('store', uids_part_str, '+FLAGS', '\\Deleted')
        bar.next(len(uids_part))
    bar.finish()
    if not config.ONLY_COPY:
        status, expunge = imap.expunge()


def move_msg_uids_by_one(imap, mail_uids, target_folder):
    for mail_uid in mail_uids:
        copy_res = imap.uid('copy', mail_uid, f'"{target_folder}"')
        if (not config.ONLY_COPY) and copy_res[0] == 'OK':
            imap.uid('store', mail_uid, '+FLAGS', '\\Deleted')
    if not config.ONLY_COPY:
        imap.expunge()


def get_ids(imap, criterion='ALL'):
    """Получение строки с ID всех писем.
    Если criterion='UNSEEN' - непросмотренные"""

    status, ids = imap.search(None, criterion)
    # print(ids[0])
    return ids[0].split()


def get_uids(imap, criterion='ALL'):
    """Выполняет поиск и возвращает UID писем.
    Если criterion='UNSEEN' - непросмотренные"""

    status, uids = imap.uid('search', None, criterion)
    # print(ids[0])
    return uids[0].split()


def show_info_msg(imap, uid):
    status, msg = imap.uid('fetch', uid, '(RFC822)')
    msg = email.message_from_bytes(msg[0][1])

    # print(msg['Date'])  # Thu, 30 Mar 2023 14:24:38 +0300  (2023, 3, 30, 14, 24, 38, 0, 1, -1, 10800)
    try:
        msg_date = datetime.strptime(msg['Date'], '%a, %d %b %Y %H:%M:%S %z')
    except ValueError:
        msg_date = datetime.strptime(msg['Date'], '%a, %d %b %Y %H:%M:%S %z (%Z)')
    letter_id = msg['Message-ID']  # айди письма
    letter_from = msg['Return-path']  # e-mail отправителя
    print(f'\nMessage {int(uid)}')
    print(msg_date, letter_id, letter_from)


def init_from_folder():
    name = config.FROM_FOLDER
    if name.lower() in ('inbox', 'входящие'):
        name = 'Входящие'
    return name


def parse_strdates():
    try:
        d_start = datetime.strptime(config.DATE_START, '%d.%m.%Y')
    except ValueError as e:
        raise err.ParseStrDateError('Неправильная дата начала периода') from None
    try:
        d_end = datetime.strptime(config.DATE_END, '%d.%m.%Y')
    except ValueError as e:
        raise err.ParseStrDateError('Неправильная дата конца периода') from None
    return d_start, d_end


def connect_imap(imap):
    try:
        status_login = imap.login(config.MAIL_LOGIN, config.MAIL_PASSW)
        logger.success(f'Подключились к почтовому ящику {config.MAIL_LOGIN}')
        # cprint(f'2Подключились к почтовому ящику {config.MAIL_LOGIN}')
        # print(status_login)
    except imap.error:
        raise err.AuthenticationError('Неверные учетные данные или IMAP отключен') from None


def get_list_folders(imap):
    folders = {}
    status, raw_folders = imap.list()
    cprint('8\nПапки на сервере:')
    for raw_folder in raw_folders:
        # print(raw_folder.decode())
        folder_sep = raw_folder.decode().split(' "|" ')
        service_info = folder_sep[0]
        raw_name = folder_sep[-1].replace('"', '')
        name = imap_utf7.decode(raw_name.encode())
        if name == 'INBOX':
            name = 'Входящие'
        folders[name] = (raw_name, service_info)
        print(f'{name:<24}', service_info)
    print()
    return folders


def select_folder_on_server(imap, folders, from_folder):
    try:
        status, inbox = imap.select(f'"{folders[from_folder][0]}"')
    except (UnicodeEncodeError, KeyError):
        raise err.InvalidFolderNameError(f'Папка "{config.FROM_FOLDER}" не найдена') from None
    inbox_count = inbox[0].decode()
    print(f'Всего писем в папке "{from_folder}": {inbox_count}')


def check_target_folder(folders, target_folder):
    try:
        target_folder = folders[target_folder][0]
    except KeyError:
        raise err.InvalidFolderNameError(f'Папка "{target_folder}" не найдена') from None


def imap_search_uids(imap, period):
    date_start_dt, date_end_dt = period
    date_start = date_start_dt.strftime('%d-%b-%Y')
    date_end = date_end_dt.strftime('%d-%b-%Y')
    uids = get_uids(imap, criterion=f'SINCE {date_start} BEFORE {date_end}')
    return uids


def waiting_for_confirmation(msg=''):
    cprint(msg, end='')
    command = input('')
    if command.lower() != 'y':
        raise err.RefusalToMoveError(f'Отмена! {title_operation()[0]} не подтверждено') from None


def show_first_last_mail_info(imap, uids):
    if uids:
        show_info_msg(imap, uid=uids[0])
        show_info_msg(imap, uid=uids[-1])


def show_all_mail_info(imap, uids):
    for uid in uids:
        show_info_msg(imap, uid=uid)


def move_emails(imap, uids, folders=None, from_folder=None, target_folder=None):
    # run_uids = (uids[-1], uids[-2])  # for test. Only first and last
    run_uids = uids
    logger.info(f'Запуск {title_operation()[1]} {len(run_uids)} писем из {from_folder} в {target_folder}')
    try:
        start_time = time.monotonic()
        move_msg_uids(imap, run_uids, folders[target_folder][0])
        end_time = time.monotonic()
        delta = timedelta(seconds=end_time - start_time)
    except imap.error as e:
        raise err.MoveEmailsError(f'Ошибка {title_operation()[1]} {e}') from None
    else:
        logger.success(f'Письма успешно {title_operation()[2]} за время {delta}')


def imap_session(imap,
                 from_folder=None, target_folder=None,
                 period=None):

    connect_imap(imap)
    folders = get_list_folders(imap)
    # print(json.dumps(folders, indent=4, ensure_ascii=False))

    select_folder_on_server(imap, folders, from_folder)
    check_target_folder(folders, target_folder)

    # ids = get_all_ids(imap)
    # uids = get_uids(imap)  # All uids
    # uids = get_uids(imap, criterion='UNSEEN')  # только непрочитанные
    uids = imap_search_uids(imap, period)
    cprint(f'8Найдено писем ^14_{len(uids)}')
    # print(uids)
    if not uids:
        logger.info('Не найдено писем по критериям')
        return

    waiting_for_confirmation(msg=f'5Для {title_operation()[1]} писем введите ^9_Y : ')

    # show_first_last_mail_info(imap, uids)
    # show_all_mail_info(imap, uids)

    move_emails(imap, uids, folders=folders, from_folder=from_folder, target_folder=target_folder)


def main():
    from_folder = init_from_folder()
    target_folder = config.TARGET_FOLDER
    date_start, date_end = parse_strdates()
    cprint(f'5Выбран почтовый ящик ^15_{config.MAIL_LOGIN}')
    cprint(f'1Режим: ^14_{title_operation()[0]}')
    cprint(f'1Откуда, куда: ^14_{config.FROM_FOLDER} ^8_-->> ^14_{target_folder}')
    cprint(f'1Период с      ^14_{date_start.date()} ^8_по ^14_{date_end.date()}')
    with IMAP4_SSL(config.IMAP_SERVER) as imap:
        imap_session(imap,
                     from_folder=from_folder, target_folder=target_folder,
                     period=(date_start, date_end))


if __name__ == '__main__':
    _width = 130
    _hight = 54
    if sys.platform == 'win32':
        os.system('color 71')
        # os.system('mode con cols=%d lines=%d' % (_width, _hight))
    else:
        os.system('setterm -background white -foreground white -store')
        # ubuntu terminal
        os.system('setterm -term linux -back $blue -fore white -clear')
    PATH_SCRIPT = os.path.abspath(os.path.dirname(__file__))
    os.chdir(PATH_SCRIPT)
    clear_console()
    check_version()

    authorship(__author__, __title__, __version__, __copyright__)  # width=_width

    try:
        main()
    except (err.ParseStrDateError, err.InvalidFolderNameError, err.AuthenticationError) as e:
        logger.critical(e)
        exit_from_program(code=1, close=config.CLOSECONSOLE)
    except (err.RefusalToMoveError, err.MoveEmailsError) as e:
        logger.log('FAIL', e)
        exit_from_program(code=0, close=config.CLOSECONSOLE)
    except KeyboardInterrupt:
        logger.info('Отмена. Скрипт остановлен.')
        exit_from_program(code=0, close=config.CLOSECONSOLE)
    except Exception as e:
        logger.critical(e)  # __str__()
        if config.EXCEPTION_TRACE:
            raise e
        exit_from_program(code=1, close=config.CLOSECONSOLE)
