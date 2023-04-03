
# Проект AssistantIMAP

---------------------------------------------------------

## Description

Перемещение писем между папок IMAP.
Damn mail.Yandex


## Зависимости

![Python version](https://img.shields.io/badge/python-3.9%2B-blue)
> Требуется Python 3.9.7+

Установка зависимостей:
```sh
pip3 install -r requirements.txt
```
Depends on:
- loguru

## Configuration

`configs/config.py`

```python
# CONFIGURATION
IMAP_SERVER = 'imap.yandex.ru'
MAIL_LOGIN = 'login'
MAIL_PASSW = 'password'

FROM_FOLDER = 'Входящие'
TARGET_FOLDER = 'Archive_2022'
DATE_START = '01.02.2023'
DATE_END = '01.03.2023'
```
``MAIL_LOGIN`` : Replace with mailbox username
``MAIL_PASSW`` : Replace with mailbox user password
``FROM_FOLDER, TARGET_FOLDER`` : Select source and target folder
``DATE_START, DATE_END`` : Choose a period


## Usage

```bash
python3 assistant_imap.py
```

## License

![License](https://img.shields.io/badge/license-Apache--2.0-blue)
:license:  [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0)

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

____

:copyright: 2023 by Vint
____

