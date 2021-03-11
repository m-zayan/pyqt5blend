from typing import Union, Callable

import sys
import os

import subprocess as process
from pathlib import Path

import json
import csv

import pandas as pd

import cv2

from datetime import datetime
import time

import traceback

from .handlers.exceptions import InvalidConfigurations

__all__ = ['Logger', 'OS', 'Sys', 'Reader', 'Writer', 'Time', 'ResManger']

OS_ROOT_DIR = str(Path.home()) + '/../../'


def invalid_arguments(func: Callable):

    def inner(*args, **kwargs):

        try:

            return func(*args, **kwargs)

        except TypeError as err:

            Logger.fail('invalid_arguments::', func.__name__, ', arguments : ')
            Logger.error(err)

    return inner


class Logger:

    @staticmethod
    def write_messages_json(content, log_file='logs.json', indent_level=3, sort_keys=False, separators=(',', ':')):

        json_record = dict()

        json_record['update_time'] = datetime.now().strftime("%I.%M:%S %p")
        json_record[json_record['update_time']] = content

        if OS.file_exists(log_file):

            Writer.dict_to_json(json_filename=log_file, content=json_record, overwrite=True,
                                indent_level=indent_level, separators=separators, sort_keys=sort_keys)

        else:

            Writer.dict_to_json(json_filename=log_file, content=json_record, overwrite=False,
                                indent_level=indent_level, separators=separators, sort_keys=sort_keys)

    @staticmethod
    def info(message, *args, end='\n'):

        print(Formatter.GREEN + str(message) + Formatter.END + Logger.__format_args__(*args), end=end)

    @staticmethod
    def info_r(message, *args):

        sys.stdout.write('\r ' + Formatter.GREEN + str(message) + Formatter.END + Logger.__format_args__(*args))
        sys.stdout.flush()

    @staticmethod
    def fail(message, *args, end='\n'):

        print(Formatter.FAIL + str(message) + Formatter.END + Logger.__format_args__(*args), end=end)

    @staticmethod
    def error(err, end='\n'):

        err_traceback = traceback.format_exc()

        Logger.fail(str(err))
        Logger.fail(str(err_traceback), end=end)

    @staticmethod
    def warning(message, *args, end='\n'):

        print(Formatter.WARNING + str(message) + Formatter.END + Logger.__format_args__(*args), end=end)

    @staticmethod
    def set_line(length: int = 100):

        Logger.info(Formatter.BLUE + '=' * length + Formatter.END)

    @staticmethod
    def __format_args__(*args):

        _format = '{}, {}' * (len(args) // 2)

        if len(args) % 2:

            _format += '{}'

        return _format.format(*args)


class OS:

    TYPE = sys.platform

    @staticmethod
    def file_exists(path):

        return Path(path).is_file()

    @staticmethod
    def dir_exists(path):

        return Path(path).is_dir()

    @staticmethod
    def make_dirs(path):

        os.makedirs(path)

    @property
    def cwd(self):

        return os.getcwd()

    @staticmethod
    def join(p1, p2):

        return os.path.join(p1, p2)

    @staticmethod
    def file_at(filename, dirs_list):

        for i in range(len(dirs_list)):

            if filename in os.listdir(dirs_list[i]):

                return dirs_list[i]

        raise ValueError(f'file : {filename}, is not found')

    @staticmethod
    def locate_file(pattern, params: str = '', updatedb=False):

        if updatedb:

            OS.run_commands('nice -n 19 ionice -c 3 updatedb')

        file_dirs = OS.run_commands(f'locate {params} {pattern}', multi_outputs=True, multi_output_sep='\n')

        if len(file_dirs) > 1:

            file_dirs.pop()

        return file_dirs

    @staticmethod
    def run_commands(command, multi_outputs=True, multi_output_sep='\n'):

        output: Union[bytes, str, list]

        try:

            if OS.TYPE == 'linux':

                output = process.check_output(command, shell=True)

            elif OS.TYPE == 'windows' or OS.TYPE == 'win':

                bash_dir = os.environ.get('bash')

                if bash_dir is None:

                    raise InvalidConfigurations('bash environmental variable doesn\'t exist')

                output = process.check_output([bash_dir, '-c', command], shell=True)

            else:

                raise InvalidConfigurations(f'Invalid OS Type : {OS.TYPE}')

        except process.CalledProcessError as error:

            content = {f'CalledProcessError': 'OS::run_commands(...), ' + str(error)}
            Logger.write_messages_json(content)

            return None

        else:

            output = output.decode()

        if multi_outputs:

            output = output.split(multi_output_sep)

        return output

    def kill_gpu_processes(self, process_keyword='python'):

        command = f"nvidia-smi | grep '{process_keyword}'"

        output = self.run_commands(command=command, multi_outputs=True)
        output = list(map(lambda l: l.split(), output))
        output = list(map(lambda l: l[4] if len(l) > 4 and l[4].isnumeric() else None, output))

        for pid in output:

            if pid is not None:

                Logger.info(f'kill : {pid}')
                self.run_commands(command=f'kill -9 {pid}')

        Logger.info('kill_gpu_processes::', output)


class Sys:

    @staticmethod
    def insert_path(index, path):

        sys.path.insert(index, path)


class Reader:

    @staticmethod
    def json_to_dict(json_filename):

        if not OS.file_exists(json_filename):

            Logger.warning(f'File: {json_filename} Doesn\'t Exist')

            return None

        content: dict

        with open(json_filename, "r") as buffer:

            content = json.load(buffer)

        return content


class Writer:

    @staticmethod
    def dict_to_json(json_filename, content, overwrite=False, indent_level=3, sort_keys=False, separators=(',', ':')):

        is_file_exist = OS.file_exists(json_filename)

        if not is_file_exist and overwrite:

            Logger.warning(f'overwrite=True, File: {json_filename} is Not Exists')

        elif is_file_exist and not overwrite:

            Logger.warning(f'File: {json_filename} Already Exists')

            ok = input('Do you want to continue - [y/n]: ')

            if ok.lower() == 'n':

                return None

            elif ok.lower() != 'y':

                Logger.error(f'Abort')

                return None

        if not is_file_exist:

            with open(json_filename, 'w+') as buffer_writer:

                json.dump(content, buffer_writer, indent=indent_level, separators=separators, sort_keys=sort_keys)
        else:

            new_content: dict

            with open(json_filename, 'r+') as buffer:

                new_content = json.load(buffer)
                new_content.update(content)

                buffer.seek(0)
                json.dump(new_content, buffer, indent=indent_level, separators=separators, sort_keys=sort_keys)
                buffer.truncate()

    @staticmethod
    def dict_to_csv(csv_filename, content, overwrite=False, use_pandas=True):

        is_file_exist = OS.file_exists(csv_filename)

        if not is_file_exist and overwrite:

            Logger.warning(f'overwrite=True, File: {csv_filename} is Not Exists')

        elif is_file_exist and not overwrite:

            Logger.warning(f'File: {csv_filename} Already Exists')

            ok = input('Do you want to continue - [y/n]: ')

            if ok.lower() == 'n':

                return None

            elif ok.lower() != 'y':

                Logger.error(f'Abort')

                return None

        if not use_pandas:

            if not is_file_exist:

                with open(csv_filename, 'w+') as buffer_writer:

                    csv_writer = csv.writer(buffer_writer)
                    csv_writer.writerow(content.keys())
                    csv_writer.writerow(content.values())

            else:

                new_content: dict

                with open(csv_filename, 'a') as buffer_writer:

                    csv_writer = csv.writer(buffer_writer)
                    csv_writer.writerow(content.values())
        else:

            dataframe = pd.DataFrame(content)
            dataframe.to_csv(csv_filename, index=False, encoding='utf-8')

    @staticmethod
    def write_image(to_path, filename, image):

        path = os.path.join(to_path, filename)

        cv2.imwrite(path, image)


class Formatter:

    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Time:

    @staticmethod
    def now(sep=':'):

        return datetime.now().strftime(f'%I{sep}%M{sep}%S')

    @staticmethod
    def sleep(seconds):

        time.sleep(seconds)


class ResManger:

    @staticmethod
    def get_intersect_path(dirname, current):

        idx = current.find(dirname)

        return current[:idx + len(dirname)]

    @staticmethod
    def get_vars_name(cls, instance):

        """
        Parameters
        ----------
        cls: class
        instance: class instance
        Return
        ------
        """
        vars_name = {}

        for key, value in vars(cls).items():

            if isinstance(value, instance):

                vars_name[value] = key

        return vars_name
