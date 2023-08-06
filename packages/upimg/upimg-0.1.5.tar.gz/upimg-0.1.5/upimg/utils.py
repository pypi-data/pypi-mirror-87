#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : mocobk
# @Email  : mailmzb@qq.com
# @Time   : 2020/11/26 19:14
import os
import pickle
import platform
from collections import namedtuple
from io import BytesIO

from PIL import Image, ImageGrab

SYSTEM = platform.system()
if SYSTEM == 'Windows':
    from upimg.sys_platform.windows import get_clipboard_file_paths, notify, set_global_hot_key

if SYSTEM == 'Darwin':
    from upimg.sys_platform.mac import get_clipboard_file_paths, notify


class ClipbordFile:
    @property
    def clipboard_file_paths(self):
        return get_clipboard_file_paths()

    @property
    def file_objects(self):
        """
        获取图片优先级： 剪贴板图片 > 已复制到剪贴板的文件列表 > 已选择的文件
        """

        image = ImageGrab.grabclipboard()

        if isinstance(image, Image.Image):
            with BytesIO() as image_bytes_io:
                image.save(image_bytes_io, format='PNG')
                image_bytes_io.seek(0)
                yield image_bytes_io, '.png'
            return

        file_paths = self.clipboard_file_paths
        if file_paths:
            for path in file_paths:
                with open(path, 'rb') as fp:
                    ext = os.path.splitext(fp.name)[1].lower()
                    yield fp, ext


def send_notify(title='UpImg', message=''):
    return notify(title=title, message=message)


CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.pkl')
CONFIG_FIELDS = ['service', 'username', 'password', 'upload_path', 'url_base']
CONFIG_DEFAULTS = ['', '', '', '/', 'https://test.upimg.com']
CONFIG = namedtuple('CONFIG', CONFIG_FIELDS)


def set_config():
    args = {}
    for field, default in zip(CONFIG_FIELDS, CONFIG_DEFAULTS):
        value = input('{}{}: '.format(field.replace('_', ' '), f'[{default}]' if default else ''))
        args[field] = value or default

    with open(CONFIG_PATH, 'wb') as fp:
        pickle.dump(CONFIG(**args), fp)

    set_global_hot_key()


def get_config() -> CONFIG:
    with open(CONFIG_PATH, 'rb') as fp:
        return pickle.load(fp)


if __name__ == '__main__':
    pass
