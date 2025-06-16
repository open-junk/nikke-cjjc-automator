import logging
import keyboard

class HotkeyManager:
    def __init__(self):
        self.stop_script = False
        self.hotkey: str = None

    def setup(self, hotkey: str = None):
        if hotkey:
            self.hotkey = hotkey
        logging.info(f"Press {self.hotkey} to stop the script at any time.")
        keyboard.add_hotkey(self.hotkey, lambda: self.stop())

    def stop(self):
        logging.warning(f"Stop hotkey {self.hotkey} detected! Attempting to stop the script...")
        self.stop_script = True

    def check(self):
        if self.stop_script:
            logging.info("Script stopped.")
            raise SystemExit(0)

    def remove(self):
        try:
            keyboard.remove_hotkey(self.hotkey)
        except Exception as e:
            logging.debug(f"Failed to remove hotkey: {e}")
