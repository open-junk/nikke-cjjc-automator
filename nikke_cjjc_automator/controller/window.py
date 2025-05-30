import logging
import time
import win32gui
import win32con
import pygetwindow
from ..config import settings
from .hotkey import HotkeyManager

class WindowManager:
    def __init__(self, hotkey_mgr: HotkeyManager):
        self.hotkey_mgr = hotkey_mgr
        self.window_title: str = getattr(settings, "WINDOW_TITLE", "NIKKE")

    def find_and_activate(self):
        self.hotkey_mgr.check()
        logging.info(f"Searching for window with title containing '{self.window_title}'...")
        delay = getattr(settings, "ACTION_DELAY", 1.2)
        hwnd = self._find_hwnd_by_title()
        if hwnd is None:
            logging.error(f"Error: No running window with title containing '{self.window_title}' found. Please make sure the game is running.")
            return None
        logging.info(f"Found target window HWND: {hwnd}, title: '{win32gui.GetWindowText(hwnd)}'")
        self.hotkey_mgr.check()
        try:
            # Restore window if minimized
            if win32gui.IsIconic(hwnd):
                logging.info("Window is minimized, restoring...")
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                time.sleep(delay)
            # Activate window
            logging.info("Activating window...")
            try:
                win32gui.SetForegroundWindow(hwnd)
            except Exception as e:
                logging.warning(f"SetForegroundWindow failed ({e}), trying ShowWindow as fallback...")
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                win32gui.SetForegroundWindow(hwnd)
            time.sleep(delay)
            foreground_hwnd = win32gui.GetForegroundWindow()
            if foreground_hwnd == hwnd:
                logging.info(f"Window HWND {hwnd} ('{win32gui.GetWindowText(hwnd)}') successfully activated and brought to foreground.")
            else:
                logging.warning(f"Tried to activate window HWND {hwnd} ('{win32gui.GetWindowText(hwnd)}'), but foreground is HWND {foreground_hwnd} ('{win32gui.GetWindowText(foreground_hwnd)}'). Script will continue, but may operate on the wrong window.")
            try:
                window = pygetwindow.Win32Window(hwnd)
                return window
            except Exception as e:
                logging.warning(f"Error creating pygetwindow object (does not affect activation): {e}")
                return None
        except Exception as e:
            logging.error(f"Unexpected error while activating window HWND {hwnd}: {e}")
            return None

    def _find_hwnd_by_title(self) -> int:
        hwnds = []
        win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), hwnds)
        for hwnd in hwnds:
            try:
                title = win32gui.GetWindowText(hwnd)
                if self.window_title.lower() in title.lower() and win32gui.IsWindowVisible(hwnd):
                    return hwnd
            except Exception:
                continue
        return None
