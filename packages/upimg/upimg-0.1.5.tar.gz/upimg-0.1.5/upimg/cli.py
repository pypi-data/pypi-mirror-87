#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : mocobk
# @Email  : mailmzb@qq.com
# @Time   : 2020/11/30 16:24
import argparse
import os
from traceback import print_exc
from urllib.parse import urljoin

from pyperclip import copy as copy2clipboard

from upimg import utils
from upimg.upload import UpImage


def parse_args():
    parser = argparse.ArgumentParser(description='Upload image from clipboard and return Markdown link.')
    parser.add_argument('-c', '--config', action="store_true", help='file upload config')
    return parser.parse_args()


def main():
    args = parse_args()
    if args.config:
        try:
            utils.set_config()
            print('Config success! Now you can execute the command "upimg" or use global hot key "Ctrl + Alt + A"')
        except Exception:
            print_exc()

    else:
        if not os.path.exists(utils.CONFIG_PATH):
            message = 'Config file is not found, Please config it first.\nusage: upimg --config'
            utils.send_notify(*message.split('\n'))
            raise Exception(message)
        config = utils.get_config()
        try:
            up = UpImage(config.service, config.username, config.password, config.upload_path)
            utils.send_notify(title='UpImg', message='uploading ...')
            markdown_links = [f'![]({urljoin(config.url_base, path)})' for path in up.upload()]
            files_count = len(markdown_links)
            if files_count > 0:
                utils.send_notify(title=f'{files_count} upload success', message='You can paste it with Ctrl + V ')
            else:
                utils.send_notify(title=f'{files_count} upload success', message='Maybe you should copy it first')
            copy2clipboard('\n'.join(markdown_links))

        except Exception:
            with open('./upimg-error.log', 'w') as fp:
                print_exc(file=fp)
            utils.send_notify('Error!!!', message=f'{os.path.abspath("./upimg-error.log")}')


if __name__ == '__main__':
    main()
