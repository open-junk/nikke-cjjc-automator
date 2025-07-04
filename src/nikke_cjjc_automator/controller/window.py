import logging
import time
import psutil
import win32gui
import win32process
import win32con
import pygetwindow
from typing import Any
from .hotkey import HotkeyManager

class WindowManager:
    def __init__(self, settings: Any, hotkey_mgr: HotkeyManager):
        self.hotkey_mgr = hotkey_mgr
        self.settings = settings
        self.process_name: str = getattr(settings, "PROCESS_NAME", "nikke.exe")
        # Use a list of possible window titles for auto-detection
        self.window_titles = getattr(settings, "WINDOW_TITLES", ["NIKKE", "勝利女神：妮姬", "胜利女神：新的希望"])

    def find_and_activate(self):
        self.hotkey_mgr.check()
        logging.info(f"Searching for process '{self.process_name}' and possible window titles: {self.window_titles}")
        delay = getattr(self.settings, "ACTION_DELAY", 1.2)
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
        # 2. Find HWND by PID and try all possible window titles
        hwnds = []
        win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), hwnds)
        target_hwnd = None
        matched_title = None
        for title_candidate in self.window_titles:
            target_title = title_candidate.lower().strip()
            for hwnd in hwnds:
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    title = win32gui.GetWindowText(hwnd).lower().strip()
                    if pid == target_pid and title == target_title and win32gui.IsWindowVisible(hwnd):
                        logging.info(f"Found window: HWND={hwnd}, Title='{win32gui.GetWindowText(hwnd)}'")
                        target_hwnd = hwnd
                        matched_title = win32gui.GetWindowText(hwnd)
                        break
                except Exception:
                    continue
            if target_hwnd:
                break
        if target_hwnd is None:
            logging.error(f"Error: Found process PID {target_pid}, but no visible main window with any of the titles: {self.window_titles}.")
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
                logging.info(f"Window HWND {target_hwnd} ('{matched_title}') successfully activated and brought to foreground.")
            else:
                logging.warning(f"Tried to activate window HWND {target_hwnd} ('{matched_title}'), but foreground is HWND {foreground_hwnd} ('{win32gui.GetWindowText(foreground_hwnd)}'). Script will continue, but may operate on the wrong window.")
            try:
                window = pygetwindow.Win32Window(target_hwnd)
                return window
            except Exception as e:
                logging.warning(f"Error creating pygetwindow object (does not affect activation): {e}")
                return None
        except Exception as e:
            logging.error(f"Unexpected error while activating window HWND {target_hwnd}: {e}")
            return None
