
# Проект AssistantIMAP

---------------------------------------------------------

## Description

Перемещение писем между папок IMAP.
Damn mail.Yandex

Проблема:
Если нужно переместить письма за определённый период в другую папку и если писем много (десятки тысяч), то перемещение превращается в задротство.

### Через web-интерфейс yandex

Выставляем отображение писем по 100 на странице (это максимум). Выбираем период внизу списка писем. Жмём N раз "ещё письма", каждый раз перемещаясь вниз страницы. Всё это дико тупит и жрёт оперативку лопатами.

- Быстро переносится max 500 шт.
- Если выбирать до 1000 - приемлимо, хоть и долго. И нужно ОБЯЗАТЕЛЬНО ждать второго обновления страницы!
- От 1000 до 2000 - то же, только гораздо медленней.
- Если больше 2000 - велика вероятность зависания.

Для 60000 писем, нужно спустится вниз страницы и нажать подгрузку суммарно 600 раз.

При отборе по периоду через поиск, письма подгружаются ещё медленней в найденные и главный косяк - выбираются так же, максимум по 100.

### Outlook

Наш любимый Outlook отбирает легче. Но тоже это лучше делать кусками по N писем иначе оутлук любит зависать намертво. Плюсом к этому можно поймать сбой в копировании, но не удалении писем! Из-за этого не разберёшь, что уже скопировало, а что нет. Привет тысячи дублей писем!

А теперь представьте, что это нужно делать время от времени у 60 человек. Вот так и родился этот скрипт.


## Requirements

![Python version](https://img.shields.io/badge/python-3.9%2B-blue)
> Требуется Python 3.9.7+

Установка зависимостей:
```sh
pip3 install -r requirements.txt
```
Depends on:
- loguru
- progress


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
ONLY_COPY = True
```
- ``MAIL_LOGIN`` : Replace with mailbox username
- ``MAIL_PASSW`` : Replace with mailbox user password
- ``FROM_FOLDER, TARGET_FOLDER`` : Select source and target folder
- ``DATE_START, DATE_END`` : Choose a period
- ``ONLY_COPY`` : Copy or Move emails


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

