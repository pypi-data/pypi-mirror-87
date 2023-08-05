import json
from json.decoder import JSONDecodeError
from pathlib import Path
from re import search
from typing import Any

import toml
import yaml

DIR = Path.cwd()
ENV = DIR.joinpath('.env')


class MyConfig():
    def __init__(self, filenames: list = None) -> None:
        self.config = parser(filenames)

    def __getattr__(self, key) -> Any:
        return self.config.get(key, None)


def parser(files: list = None) -> dict:
    '''This is a function that parses files.

    Args:
        files (list): Path to the files.

    Raises:
        Exception: Unknown format.
        Exception: Specify the correct path to the files.

    Returns:
        dict: Parsed data.
    '''
    data = dict()
    if ENV.exists():
        env_data = env_parse(ENV)
        data.update(env_data)
    if files:
        for i, file in enumerate(files):
            files[i] = str(DIR.joinpath(file))
        for file in files:
            file_data = dict()
            try:
                with open(file, encoding='utf-8') as f:
                    format = file.split('.')[-1]
                    if format == 'json':
                        try:
                            file_data = json.load(f)
                        except JSONDecodeError:
                            pass
                    elif format == 'toml':
                        file_data = toml.load(f)
                    elif format == 'yaml':
                        file_data = yaml.safe_load(f)
                    data.update(file_data)
            except FileNotFoundError:
                print(
                    'File not found. ' +
                    'Specify the correct path to the file: {}'.format(
                        file.split('\\')[-1]))
    _ = [dict(), list()]
    for key in data:
        if '-' in key:
            _[1].append(key)
            _[0].update({key.replace('-', '_'): data[key]})
    data.update(_[0])
    for item in _[1]:
        data.pop(item)
    return data


def env_parse(file: str) -> dict:
    '''Parses the .env file.

    Args:
        file (str): File path

    Returns:
        dict: .env file data
    '''

    data = dict()
    with open(file, encoding='utf-8') as f:
        for line in f:
            re_data = search(r'([a-zA-Z0-9_]+)\=(.*\n(?=[A-Z])|.*$)', line)
            var = re_data.group(1)
            value = re_data.group(2).strip('{}{}'.format('"', "'"))
            if value.isdigit():
                data.update({var: int(value)})
            elif value.lower() in ['true', 'false']:
                if value.lower() == 'true':
                    data.update({var: True})
                else:
                    data.update({var: False})
            else:
                data.update({var: value})
    return(data)
