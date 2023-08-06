# -*- coding: utf-8 -*-
# @File : windows.py
# @Author : mocobk
# @Email : mailmzb@qq.com
# @Time : 2020/11/29 3:13 下午
import os
import sys
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
    notification.notify(title, message, app_icon=icon_path, timeout=0)
    return True


def get_desktop_path():
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, 'Desktop')[0]


def set_global_hot_key():
    """
    HOT KEY code
    https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-gethotkey
    Return              code/value	       Description
    HOTKEYF_ALT         0x04               ALT key
    HOTKEYF_CONTROL     0x02               CTRL key
    HOTKEYF_EXT         0x08               Extended key
    HOTKEYF_SHIFT       0x01               SHIFT key
    """
    import pythoncom
    from win32com.shell import shell

    # 要创建快捷方式的文件的完整路径
    exe_path = os.path.join(sys.base_prefix, 'Scripts', 'upimg.exe')
    exe_path = os.path.join(r'D:\Anaconda3', 'Scripts', 'upimg.exe')
    iconname = os.path.join(os.path.dirname(__file__), 'notification.ico')
    # 在桌面生成创建快捷方式（其他路径快捷键会失效）
    # lnk_path = os.path.join(os.getenv("APPDATA"), 'UpImg.lnk')
    lnk_path = os.path.join(get_desktop_path(), 'UpImg.lnk')

    shortcut = pythoncom.CoCreateInstance(
        shell.CLSID_ShellLink, None,
        pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
    shortcut.SetPath(exe_path)
    # Ctrl + Alt + A
    # hot_key = (0x02 << 8) | (0x04 << 8) | 0x41
    hot_key = (0x02 << 8) | 0x31
    shortcut.SetHotkey(hot_key)
    # 设置快捷方式的起始位置, 不然会出现找不到辅助文件的情况
    shortcut.SetWorkingDirectory(os.path.dirname(exe_path))
    # 可有可无，没有就默认使用文件本身的图标
    shortcut.SetIconLocation(iconname, 0)
    # https://docs.microsoft.com/en-us/windows/win32/api/shobjidl_core/nf-shobjidl_core-ishelllinka-setshowcmd
    # SW_SHOWNORMAL 1 | SW_SHOWMINIMIZED 2(无效) | SW_SHOWMINNOACTIVE 7 | SW_SHOWMAXIMIZED 3
    shortcut.SetShowCmd(7)
    shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnk_path, 0)

