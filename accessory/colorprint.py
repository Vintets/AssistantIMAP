#!/home/admin/venv_flask3/bin/python3
# -*- coding: utf-8 -*-

# from __future__ import print_function
import os
import re
import sys
PLATFORM = sys.platform
if PLATFORM == 'win32':
    from ctypes import windll
    _stdout_handle = windll.kernel32.GetStdHandle(-11)
    _SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
else:
    pass


def _pr(cstr, force_linux=False):
    clst = cstr.split('^')
    color = 0x0001
    for cstr in clst:
        dglen = re.search(r'\D', cstr).start()
        if dglen:
            color = int(cstr[:dglen])
        text = cstr[dglen:]
        text = text.replace('\u0456', u'i')
        if text[:1] == '_':
            text = text[1:]
        text = _set_color(color, force_linux) + text
        # sys.stdout.write(text)
        print(text, end='')
        sys.stdout.flush()


def _restore_colors(end=''):
    # sys.stdout.write(_set_color(20) + '')
    print(_set_color(20) + '', end=end)
    sys.stdout.flush()


def cprint(cstr, end='\n', force_linux=False):
    _pr(cstr, force_linux=force_linux)
    _restore_colors(e=end)


# def cprint2(cstr, force_linux=False):
    # _pr(cstr, force_linux=force_linux)
    # _restore_colors()


def colors_win():
    return {
            0 : 'чёрный',  # noqa: E203
            1 : 'синий',  # noqa: E203
            2 : 'зелёный',  # noqa: E203
            3 : 'голубой',  # noqa: E203
            4 : 'красный',  # noqa: E203
            5 : 'фиолетовый',  # noqa: E203
            6 : 'жёлтый',  # noqa: E203
            7 : 'серый',  # noqa: E203

            8 : 'тёмно-серый',  # noqa: E203
            9 : 'светло-синий',  # noqa: E203
            10: 'светло-зелёный',
            11: 'светло-голубой',
            12: 'светло-красный',
            13: 'светло-фиолетовый (пурпурный)',
            14: 'светло-жёлтый',
            15: 'белый',
            }


def colors_win2linux():
    return {
            0 : 30,  # noqa: E203
            1 : 34,  # noqa: E203
            2 : 32,  # noqa: E203
            3 : 36,  # noqa: E203
            4 : 31,  # noqa: E203
            5 : 35,  # noqa: E203
            6 : 33,  # noqa: E203
            7 : 37,  # noqa: E203

            8 : 90,  # noqa: E203
            9 : 94,  # noqa: E203
            10: 92,
            11: 96,
            12: 91,
            13: 95,
            14: 93,
            15: 97,
            }


def _dafault_color(force_linux):
    # цвет по умолчанию: 20
    # для windows это 1, для linux - сброс
    def_color = 1
    if ('linux' in PLATFORM) or force_linux:
        def_color = 15
    elif PLATFORM == 'win32':
        def_color = 1
    return def_color


def _set_color(color, force_linux=False):
    if color == 20:
        color = _dafault_color(force_linux)
    prefix_color = ''
    if ('linux' in PLATFORM) or force_linux:
        prefix_color = '\033[%(col_linux)sm' % {'col_linux': colors_win2linux()[color]}
    elif PLATFORM == 'win32':
        _SetConsoleTextAttribute(_stdout_handle, color | 0x0070)  # 78
    return prefix_color


# --------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    os.system('color 71')
    for col in range(16):
        color_win = {
                'color': col,
                'name': colors_win()[col]
                }
        cprint('%(color)dЦвет %(color)d\t %(name)s' % color_win)

    print('\nПримеры')
    cprint('20######### Идем к другу ^14_%s ^8_%d/%d ^20_на ^3_%s ^20_#########' % (12345, 5, 3000, 'main'))
    cprint('13Завершили обход всех ^12_НОВЫХ ^13_друзей')

    cprint('Обрабатываем файл ^5_XXX ^13_YYY')
    cprint('Обрабатываем файл ^5_XXX ^13_YYY ^14_ZZZ', end='')
    cprint('4 конец')

    # input('\n---------------   END   ---------------')

# ==================================================================================================
