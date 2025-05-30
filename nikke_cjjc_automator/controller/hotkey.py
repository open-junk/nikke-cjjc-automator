import logging
import keyboard
from ..config import settings

class HotkeyManager:
    def __init__(self):
        self.stop_script = False
        self.hotkey: str = settings.STOP_HOTKEY

    def setup(self):
        hotkey = getattr(settings, "STOP_HOTKEY", "ctrl+c").lower()
        logging.info(f"按下 {hotkey} 可以隨時停止腳本。")
        keyboard.add_hotkey(hotkey, lambda: self.stop())

    def stop(self):
        logging.warning(f"偵測到停止熱鍵 {self.hotkey}！正在嘗試停止腳本...")
        self.stop_script = True

    def check(self):
        if self.stop_script:
            logging.info("腳本已停止。")
            raise SystemExit(0)
