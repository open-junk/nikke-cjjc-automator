from pathlib import Path
import ctypes
import time
import logging

def notify(msg: str, title: str = "操作完成"):
    MB_OK = 0x00000000
    MB_ICONINFORMATION = 0x00000040
    MB_SETFOREGROUND = 0x00010000
    MB_TOPMOST = 0x00040000
    time.sleep(0.5)
    try:
        ctypes.windll.user32.SetForegroundWindow(ctypes.windll.user32.GetDesktopWindow())
        ctypes.windll.user32.MessageBoxW(None, msg, title, MB_OK | MB_ICONINFORMATION | MB_SETFOREGROUND | MB_TOPMOST)
    except Exception as e:
        logging.error(f"顯示通知失敗: {e}")


def notify_image(img_path: str, title: str = "操作完成"):
    if Path(img_path).exists():
        notify(f"完成！\n\n已存檔: {Path(img_path).name}", title)
    else:
        logging.error(f"通知圖片不存在: {img_path}")
        notify("通知圖片不存在。", "操作錯誤")
