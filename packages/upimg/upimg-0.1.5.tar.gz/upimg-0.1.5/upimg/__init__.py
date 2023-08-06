import os
import pythoncom
from win32com.shell import shell
from win32com.shell import shellcon
import win32con

def set_shortcut():  # 如无需特别设置图标，则可去掉iconname参数
    try:
        filename = r"D:\Anaconda3\Scripts\upimg.exe"  # 要创建快捷方式的文件的完整路径
        iconname = ""
        lnkname = r"D:\Users\Desktop" + r"\timer.exe.lnk"  # 将要在此路径创建快捷方式

        shortcut = pythoncom.CoCreateInstance(
            shell.CLSID_ShellLink, None,
            pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
        shortcut.SetPath(filename)
        # key = (0x02 << 8) | (0x04 << 8) | 0x41
        key = (0x04 << 8) | 0x42
        t = shortcut.SetHotkey(key)
        print(t)
        shortcut.SetWorkingDirectory(r"D:\Anaconda3\Scripts") # 设置快捷方式的起始位置, 不然会出现找不到辅助文件的情况
        shortcut.SetIconLocation(iconname, 0)  # 可有可无，没有就默认使用文件本身的图标
        if os.path.splitext(lnkname)[-1] != '.lnk':
            lnkname += ".lnk"
        shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnkname, 0)

        return True
    except Exception as e:
        return False

if __name__ == '__main__':
    set_shortcut()
