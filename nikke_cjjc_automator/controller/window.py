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

    def find_and_activate(self):
        self.hotkey_mgr.check()
        target_pid = self._find_pid()
        hwnd = self._find_hwnd(target_pid)
        self._activate_hwnd(hwnd)
        return pygetwindow.Win32Window(hwnd)

    def _find_pid(self) -> int:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == self.process_name.lower():
                    return proc.info['pid']
            except Exception:
                continue
        raise RuntimeError(f"Process {self.process_name} not found")

    def _find_hwnd(self, pid: int) -> int:
        hwnds = []
        win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), hwnds)
        for hwnd in hwnds:
            try:
                _, win_pid = win32process.GetWindowThreadProcessId(hwnd)
                if win_pid == pid and win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                    return hwnd
            except Exception:
                continue
        raise RuntimeError(f"Main window for PID={pid} not found")

    def _activate_hwnd(self, hwnd: int):
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(1.5)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)
