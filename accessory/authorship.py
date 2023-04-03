import shutil


# __author__ = 'master by Vint'
# __title__ = '--- TeplonetNew ---'
# __version__ = '0.0.1'
# __build__ = 0x000000
# __copyright__ = 'Copyright 2017 ©  bitbucket.org/Vintets'
# __license__ = ''
# authorship.authorship(__author__, __title__, __version__, __copyright__)

def authorship(author, title: str, version: str, copyright_: str, width: int = 0) -> None:
    if not width:
        width = shutil.get_terminal_size().columns
    copyright_ = copyright_.center(width, ' ')
    version = f'version {version} {author}'.center(width, ' ')
    name_product = title.center(width, ' ')
    print('{0}{1}{2}{0}'.format('*' * width, copyright_, version))
    print('{0}\n'.format(name_product))
