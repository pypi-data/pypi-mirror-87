# -*- coding: utf-8 -*-
# @File : upload.py
# @Author : mocobk
# @Email : mailmzb@qq.com
# @Time : 2020/11/25 10:54 下午

from datetime import datetime
from typing import List

import upyun

from upimg.utils import ClipbordFile


class UpImage:
    def __init__(self, service, username, password, upload_path='/'):
        self.upyun = upyun.UpYun(service, username, password)
        self.upload_path = upload_path

    def upload(self) -> List[str]:
        """
        return {'content-length': '1916', 'content-type': 'image/jpeg', 'etag': '"ad38e734e48cd6134e02bc60f91c55b5"',
        'file-type': 'JPEG', 'width': '132', 'height': '23', 'frames': '1'}
        """
        path_list = []
        clipbord_file = ClipbordFile()
        for file, ext in clipbord_file.file_objects:
            full_path = self.upload_path + datetime.now().strftime('%Y%m%d%H%M%S%f') + ext
            self.upyun.put(full_path, file)
            path_list.append(full_path)
        return path_list
