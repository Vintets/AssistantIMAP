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
from configs import config
import errors as err
from accessory import (authorship, clear_console, cprint,
                       check_version, create_dirs, exit_from_program,
                       logger, imap_utf7)


__version_info__ = ('0', '6', '2')
__version__ = '.'.join(__version_info__)
__author__ = 'master by Vint'
__title__ = '--- AssistantIMAP ---'
__copyright__ = 'Copyright 2023 (c)  bitbucket.org/Vintets'


def move_msg(imap, mail_ids, target_folder):
    for mail_id in mail_ids:
        copy_res = imap.copy(mail_id, target_folder)
        if copy_res[0] == 'OK':
            imap.store(mail_id, '+FLAGS', '\\Deleted')
    imap.expunge()


def move_msg_uid(imap, mail_uids, target_folder):
    for mail_uid in mail_uids:
        copy_res = imap.uid('copy', mail_uid, target_folder)
        if copy_res[0] == 'OK':
            imap.uid('store', mail_uid, '+FLAGS', '\\Deleted')
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


def imap_search_uids(imap, period):
    date_start_dt, date_end_dt = period
    date_start = date_start_dt.strftime('%d-%b-%Y')
    date_end = date_end_dt.strftime('%d-%b-%Y')
    uids = get_uids(imap, criterion=f'SINCE {date_start} BEFORE {date_end}')
    return uids


def waiting_for_confirmation(msg=''):
    cprint(msg, end='')
    command = input('')
    if command != 'Y':
        raise err.RefusalToMoveError(f'Отмена! Перемещение не подтверждено') from None


def show_first_last_mail_info(imap, uids):
    if uids:
        show_info_msg(imap, uid=uids[0])
        show_info_msg(imap, uid=uids[-1])


def show_all_mail_info(imap, uids):
    for uid in uids:
        show_info_msg(imap, uid=uid)


def imap_session(imap,
                 from_folder=None, target_folder=None,
                 period=None):

    connect_imap(imap)
    folders = get_list_folders(imap)
    # print(json.dumps(folders, indent=4, ensure_ascii=False))

    try:
        status, inbox = imap.select(folders[from_folder][0])
    except UnicodeEncodeError:
        raise err.InvalidFolderNameError(f'Папка "{config.FROM_FOLDER}" не найдена') from None
    inbox_count = inbox[0].decode()
    print(f'Всего писем в папке "{from_folder}": {inbox_count}')

    # ids = get_all_ids(imap)
    # uids = get_uids(imap)  # All uids
    # uids = get_uids(imap, criterion='UNSEEN')  # только непрочитанные
    uids = imap_search_uids(imap, period)
    cprint(f'0Найдено писем ^14_{len(uids)} ^1_{uids}')

    waiting_for_confirmation(msg='5Для переноса писем введите ^9_Y : ')

    show_first_last_mail_info(imap, uids)
    # show_all_mail_info(imap, uids)

    # move_msg(imap, (ids[-1], ids[-2]), target_folder)
    # move_msg_uid(imap, (uids[-1], uids[-2]), target_folder)

def main():
    from_folder = init_from_folder()
    target_folder = imap_utf7.encode(config.TARGET_FOLDER)
    date_start, date_end = parse_strdates()
    cprint(f'5Выбран почтовый ящик ^15_{config.MAIL_LOGIN}')
    cprint(f'1Период: ^14_{date_start.date()} ^0_-->> ^14_{date_end.date()}')
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
    except err.RefusalToMoveError as e:
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
