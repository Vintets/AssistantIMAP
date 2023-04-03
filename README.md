
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
TARGET_FOLDER = 'Archive'
```
``USR`` : Replace with MySQL/MariaDB user name
``PWD`` : Replace with MySQL/MariaDB user password


## Usage

```bash
python3 assistant_imap.py
```

## License
____

:copyright: 2023 by Vint

![License](https://img.shields.io/badge/license-Apache--2.0-blue)
:license:  [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0)

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

____


> Примичание: ...
