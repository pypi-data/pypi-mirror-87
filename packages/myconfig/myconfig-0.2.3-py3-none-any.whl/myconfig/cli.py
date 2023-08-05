import argparse
from pathlib import Path

FORMATS = ['json', 'toml', 'yaml']

DIR = Path.cwd()

gitignore = DIR.joinpath('.gitignore')
config_ignore = '\n\n# myconfig\n{}'

python_code = """from myconfig import MyConfig

config = MyConfig(['{}', '{}'])
"""

python_env_only = """from myconfig import MyConfig

config = MyConfig()
"""


def init(format: str = None) -> None:
    '''Creates the file myconfig.
    Adds the path to the .settings file in .gitignore.

    Args:
        format (str): File format.
        settings (str, optional): Default config file. Defaults to 'settings'.
        secrets (str, optional): Default secret config file.\
        Defaults to '.secrets'.

    Raises:
        Exception: Unknown format.
    '''
    if format:
        settings = 'settings'
        secrets = '.secrets'

        if format not in FORMATS:
            raise Exception('Unknown format.')

        for file in [settings, secrets]:
            f = open(DIR.joinpath(
                '{}.{}'.format(file, format)),
                'a',
                encoding='utf-8')
            f.close()

        with open(DIR.joinpath('settings.py'), 'w', encoding='utf-8') as f:
            f.write(
                python_code.format(
                    '{}.{}'.format(settings, format),
                    '{}.{}'.format(secrets, format)))

        if gitignore.exists():
            file = gitignore.read_text(encoding='utf-8')
            file += config_ignore.format(secrets + '.*')
            with open(gitignore, 'r+', encoding='utf-8') as f:
                text = f.read() + config_ignore.format(secrets + '.*')
                f.seek(0)
                f.write(text)
    else:
        with open(DIR.joinpath('settings.py'), 'w', encoding='utf-8') as f:
            f.write(python_env_only)


def main() -> None:
    '''CLI function'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--init', default=None, type=str, nargs='?')
    args = parser.parse_args()
    if args.init:
        return init(args.init)
    return init()


if __name__ == '__main__':
    main()
