from ..controller.hotkey import HotkeyManager
from typing import Any

class BaseAction:
    """Abstracts all shared logic related to window, clicking, and screenshotting."""
    def __init__(self, settings: Any, hotkey_mgr: HotkeyManager):
        self.settings = settings
        self.hotkey_mgr = hotkey_mgr

    def _get_window_rect(self, window: Any) -> tuple[int, int, int, int]:
        hwnd = window._hWnd
        from win32gui import GetClientRect, ClientToScreen
        left, top, right, bottom = GetClientRect(hwnd)
        width, height = right - left, bottom - top
        screen_left, screen_top = ClientToScreen(hwnd, (left, top))
        return screen_left, screen_top, width, height

    def to_screen_coords(self, rel_coord: Any, window: Any) -> tuple[int, int]:
        screen_left, screen_top, width, height = self._get_window_rect(window)
        x = screen_left + round(rel_coord[0] * width)
        y = screen_top + round(rel_coord[1] * height)
        return x, y

    def to_screen_region(self, rel_region: Any, window: Any) -> tuple[int, int, int, int]:
        screen_left, screen_top, width, height = self._get_window_rect(window)
        region_left = screen_left + round(rel_region[0] * width)
        region_top = screen_top + round(rel_region[1] * height)
        region_width = round(rel_region[2] * width)
        region_height = round(rel_region[3] * height)
        return (region_left, region_top, region_width, region_height)

class ActionPerformer(BaseAction):
    """Handles clicking and screenshotting, inherits shared logic."""
    def click(self, rel_coord: Any, window: Any, delay: float = None):
        self.hotkey_mgr.check()
        import pyautogui, time, logging
        x, y = self.to_screen_coords(rel_coord, window)
        logging.info(f"Click at {x},{y}")
        pyautogui.moveTo(x, y, duration=0.2)
        pyautogui.click(x, y)
        time.sleep(delay or getattr(self.settings, "ACTION_DELAY", 1.2))

    def screenshot(self, rel_region: Any, window: Any, filename: str):
        self.hotkey_mgr.check()
        import pyautogui, time, logging
        region = self.to_screen_region(rel_region, window)
        logging.info(f"Screenshot region {region} -> {filename}")
        img = pyautogui.screenshot(region=region)
        img.save(filename)
        time.sleep(0.2)
