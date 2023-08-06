# -*- coding: utf-8 -*-
# @File : windows.py
# @Author : mocobk
# @Email : mailmzb@qq.com
# @Time : 2020/11/29 3:13 下午
import os
from ctypes import windll, create_unicode_buffer, c_void_p, c_uint, c_wchar_p
from typing import List
from plyer import notification

def get_clipboard_file_paths() -> List[str]:
    """
    windows 平台获取剪贴板复制的文件路径列表
    """
    kernel32 = windll.kernel32
    global_lock = kernel32.GlobalLock
    global_lock.argtypes = [c_void_p]
    global_lock.restype = c_void_p
    global_unlock = kernel32.GlobalUnlock
    global_unlock.argtypes = [c_void_p]

    user32 = windll.user32
    get_clipboard_data = user32.GetClipboardData
    get_clipboard_data.restype = c_void_p

    drag_query_file = windll.shell32.DragQueryFileW
    drag_query_file.argtypes = [c_void_p, c_uint, c_wchar_p, c_uint]

    cf_hdrop = 15
    paths_list = []

    if user32.OpenClipboard(None):
        h_global = user32.GetClipboardData(cf_hdrop)
        if h_global:
            h_drop = global_lock(h_global)
            if h_drop:
                count = drag_query_file(h_drop, 0xFFFFFFFF, None, 0)
                for i in range(count):
                    length = drag_query_file(h_drop, i, None, 0)
                    buffer = create_unicode_buffer(length)
                    drag_query_file(h_drop, i, buffer, length + 1)
                    paths_list.append(buffer.value)

                global_unlock(h_global)

        user32.CloseClipboard()

    return paths_list

def notify(title='UpImg', message=''):
    """发送系统通知"""
    icon_path = os.path.join(os.path.dirname(__file__), 'notification.ico')
    notification.notify(title, message, app_icon=icon_path,  timeout=0)
    return True
