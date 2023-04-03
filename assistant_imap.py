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
import time
from datetime import datetime, date, timedelta, time as dt_time
from imaplib import IMAP4_SSL
import email
# import shlex
from utf7 import imaputf7decode, imaputf7encode
from imap_tools import imap_utf7
# import accessory.errors as err
from accessory import authorship, clear_consol, cprint, check_version, create_dirs, exit_from_program, logger


__version_info__ = ('0', '3', '0')
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

    msg_date = datetime.strptime(msg['Date'], '%a, %d %b %Y %H:%M:%S %z')
    # print(msg['Date'])  # Thu, 30 Mar 2023 14:24:38 +0300  (2023, 3, 30, 14, 24, 38, 0, 1, -1, 10800)
    letter_id = msg['Message-ID']  # айди письма
    letter_from = msg['Return-path']  # e-mail отправителя
    print(f'\nMessage {int(uid)}')
    print(msg_date, letter_id, letter_from)


def filter_messages_by_date(imap, uids):
    for uid in uids:
        status, msg = imap.uid('fetch', uid, '(RFC822)')
        # if status == 
        msg = email.message_from_bytes(msg[0][1])

        msg_date = datetime.strptime(msg['Date'], '%a, %d %b %Y %H:%M:%S %z')



def main(imap_server, username, mail_pass, target_folder):
    with IMAP4_SSL(imap_server) as imap:
        status_login = imap.login(username, mail_pass)
        print(status_login)
        status, folders = imap.list()
        for folder in folders:
            # print(folder.decode())
            # folder_utf8 = imaputf7decode(folder.decode())
            folder_utf8 = imap_utf7.decode(folder)
            # folder_list = shlex.split(folder_utf8)
            folder_list = folder_utf8.split(' "|" ')
            name = folder_list[-1].replace('"', '')
            print(f'{name:<24}', folder_list[0])
        status, inbox = imap.select('INBOX')
        inbox_count = inbox[0].decode()
        print(f'Входящие {inbox_count}')

        # ids = get_all_ids(imap)
        # uids = get_uids(imap, criterion='UNSEEN')  # только непрочитанные
        uids = get_uids(imap, criterion='(SINCE "16-03-2023")')
        # uids = get_uids(imap)
        print(uids)

        show_info_msg(imap, uid=uids[-1])

        # selected_msg = filter_messages_by_date(imap, uids)


        # move_msg(imap, (ids[-1], ids[-2]), target_folder)
        # move_msg_uid(imap, (uids[-1], uids[-2]), target_folder)

        # imap.fetch(b'19', "(BODY[HEADER.FIELDS (Subject)])")


def exit_from_program(code: int = 0) -> None:
    time.sleep(1)
    try:
        sys.exit(code)
    except SystemExit:
        os._exit(code)


if __name__ == '__main__':
    imap_server = 'imap.yandex.ru'
    username = 'login'
    mail_pass = 'password'
    target_folder = imap_utf7.encode('Входящие_2022')

    try:
        main(imap_server, username, mail_pass, target_folder)
    except Exception as e:
        # logger.critical(e)  # __str__()
        raise e
        exit_from_program(code=1)
    except KeyboardInterrupt:
        # logger.info('Отмена. Скрипт остановлен.')
        exit_from_program(code=0)
