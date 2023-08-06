# -*- coding: utf-8 -*-
# @File : mac.py
# @Author : mocobk
# @Email : mailmzb@qq.com
# @Time : 2020/11/29 3:14 下午
from typing import List

from AppKit import NSPasteboard, NSFilenamesPboardType
from notifypy import Notify


def get_clipboard_file_paths() -> List[str]:
    """
    获取剪贴板复制的文件路径列表
    """
    pb = NSPasteboard.generalPasteboard()
    if NSFilenamesPboardType in pb.types():
        paths = pb.propertyListForType_(NSFilenamesPboardType)
        return list(paths)
    else:
        return []

def notify(title='UpImg', message='') -> bool:
    """发送系统通知"""
    notify = Notify()
    notify.application_name = 'UpImg'
    notify.title = title
    notify.message = message
    return notify.send(block=False)
