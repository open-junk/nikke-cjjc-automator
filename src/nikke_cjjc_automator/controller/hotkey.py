import logging
import keyboard
from ..config import settings

class HotkeyManager:
    def __init__(self):
        self.stop_script = False
        self.hotkey: str = settings.STOP_HOTKEY

    def setup(self):
        hotkey = getattr(settings, "STOP_HOTKEY", "ctrl+c").lower()
        logging.info(f"Press {hotkey} to stop the script at any time.")
        keyboard.add_hotkey(hotkey, lambda: self.stop())

    def stop(self):
        logging.warning(f"Stop hotkey {self.hotkey} detected! Attempting to stop the script...")
        self.stop_script = True

    def check(self):
        if self.stop_script:
            logging.info("Script stopped.")
            raise SystemExit(0)
