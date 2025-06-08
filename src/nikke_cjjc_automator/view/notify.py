from pathlib import Path
import ctypes
import time
import logging

def notify(msg: str, title: str = "Operation Completed"):
    MB_OK = 0x00000000
    MB_ICONINFORMATION = 0x00000040
    MB_SETFOREGROUND = 0x00010000
    MB_TOPMOST = 0x00040000
    time.sleep(0.5)
    try:
        ctypes.windll.user32.MessageBoxW(None, msg, title, MB_OK | MB_ICONINFORMATION | MB_SETFOREGROUND | MB_TOPMOST)
    except Exception as e:
        logging.error(f"Failed to show notification: {e}")


def notify_image(img_path: str, title: str = "Operation Completed"):
    if Path(img_path).exists():
        notify(f"Done!\n\nSaved: {Path(img_path).resolve()}", title)
    else:
        logging.error(f"Notification image does not exist: {Path(img_path).resolve(strict=False)}")
        notify("Notification image does not exist.", "Operation Error")
