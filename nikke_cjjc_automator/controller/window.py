import logging
import time
import psutil
import win32gui
import win32process
import win32con
import pygetwindow
from ..config import settings
from .hotkey import HotkeyManager

class WindowManager:
    def __init__(self, hotkey_mgr: HotkeyManager):
        self.hotkey_mgr = hotkey_mgr
        self.process_name: str = getattr(settings, "PROCESS_NAME", "nikke.exe")
        self.window_title: str = getattr(settings, "WINDOW_TITLE", "NIKKE")

    def find_and_activate(self):
        self.hotkey_mgr.check()
        logging.info(f"Searching for process '{self.process_name}' and window with title '{self.window_title}'...")
        delay = getattr(settings, "ACTION_DELAY", 1.2)
        # 1. Find process PID(s)
        found_pids = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == self.process_name.lower():
                    found_pids.append(proc.info['pid'])
                    logging.debug(f"Found matching process: PID={proc.info['pid']}, Name={proc.info['name']}")
            except Exception as e:
                logging.warning(f"Error while iterating processes: {e}")
                continue
        if not found_pids:
            logging.error(f"Error: No running process named '{self.process_name}' found. Please make sure the game is running.")
            return None
        if len(found_pids) > 1:
            logging.warning(f"Warning: Found multiple '{self.process_name}' processes (PIDs: {found_pids}). Using the first one: {found_pids[0]}")
        target_pid = found_pids[0]
        logging.info(f"Found target process PID: {target_pid}")
        self.hotkey_mgr.check()
        # 2. Find HWND by PID and window title
        hwnds = []
        win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), hwnds)
        target_title = self.window_title.lower().strip()
        target_hwnd = None
        for hwnd in hwnds:
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                title = win32gui.GetWindowText(hwnd).lower().strip()
                if pid == target_pid and title == target_title and win32gui.IsWindowVisible(hwnd):
                    logging.info(f"Found window: HWND={hwnd}, Title='{win32gui.GetWindowText(hwnd)}'")
                    target_hwnd = hwnd
                    break
            except Exception:
                continue
        if target_hwnd is None:
            logging.error(f"Error: Found process PID {target_pid}, but no visible main window with title '{self.window_title}'.")
            return None
        self.hotkey_mgr.check()
        # 3. Activate window
        try:
            if win32gui.IsIconic(target_hwnd):
                logging.info("Window is minimized, restoring...")
                win32gui.ShowWindow(target_hwnd, win32con.SW_RESTORE)
                time.sleep(delay)
            logging.info("Activating window...")
            try:
                win32gui.SetForegroundWindow(target_hwnd)
            except Exception as e:
                logging.warning(f"SetForegroundWindow failed ({e}), trying ShowWindow as fallback...")
                win32gui.ShowWindow(target_hwnd, win32con.SW_SHOW)
                win32gui.SetForegroundWindow(target_hwnd)
            time.sleep(delay)
            foreground_hwnd = win32gui.GetForegroundWindow()
            if foreground_hwnd == target_hwnd:
                logging.info(f"Window HWND {target_hwnd} ('{win32gui.GetWindowText(target_hwnd)}') successfully activated and brought to foreground.")
            else:
                logging.warning(f"Tried to activate window HWND {target_hwnd} ('{win32gui.GetWindowText(target_hwnd)}'), but foreground is HWND {foreground_hwnd} ('{win32gui.GetWindowText(foreground_hwnd)}'). Script will continue, but may operate on the wrong window.")
            try:
                window = pygetwindow.Win32Window(target_hwnd)
                return window
            except Exception as e:
                logging.warning(f"Error creating pygetwindow object (does not affect activation): {e}")
                return None
        except Exception as e:
            logging.error(f"Unexpected error while activating window HWND {target_hwnd}: {e}")
            return None
