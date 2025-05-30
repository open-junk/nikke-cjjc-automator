# 將原 nikke_automator.py 的主邏輯與函數重構到這裡，並用 dynaconf 讀取設定
import logging
from nikke_cjjc_automator.model.coordinates import CoordinateHelper
from nikke_cjjc_automator.controller.action import ActionPerformer
from nikke_cjjc_automator.controller.stitch import ImageStitcher
from nikke_cjjc_automator.controller.hotkey import HotkeyManager
from nikke_cjjc_automator.controller.window import WindowManager
from nikke_cjjc_automator.view.notify import notify_image
from nikke_cjjc_automator.view.menu import select_mode
from nikke_cjjc_automator.config import settings
import sys
import os
import ctypes
import tempfile
from dataclasses import dataclass, field
from typing import Self, Any, Optional
from nikke_cjjc_automator.controller.mode_strategy.modestrategy_impl import PredictMode, ReviewMode, AntiBuyMode
from nikke_cjjc_automator.controller.mode_strategy.mode import ModeContext
from pathlib import Path

@dataclass(slots=True)
class NikkeAutomator:
    hotkey_mgr: HotkeyManager = field(default_factory=HotkeyManager)
    coord: CoordinateHelper = field(default_factory=CoordinateHelper)
    window_mgr: WindowManager = field(init=False)
    action: ActionPerformer = field(init=False)
    stitcher: ImageStitcher = field(init=False)
    temp_dir: Path = field(init=False)
    mode: Optional[int] = None
    mode_map: dict[int, PredictMode | ReviewMode | AntiBuyMode] = field(init=False)

    def __post_init__(self: Self) -> None:
        self.window_mgr = WindowManager(self.hotkey_mgr)
        self.action = ActionPerformer(self.hotkey_mgr)
        self.stitcher = ImageStitcher(self.hotkey_mgr)
        self.temp_dir = Path(tempfile.gettempdir()) / "nikke_cjjc_automator"
        self.mode_map = {
            1: PredictMode(),
            2: ReviewMode(),
            3: AntiBuyMode(),
        }

    def run(self: Self, mode: int) -> None:
        import shutil, time, logging
        self.mode = mode
        self.hotkey_mgr.setup()
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        window = self.window_mgr.find_and_activate()
        logging.info(f"視窗已激活: {window.title}")
        c = self.coord
        s = settings
        try:
            ctx = {
                'coord': c,
                'settings': s,
                'window': window,
                'automator': self
            }
            match mode:
                case 1 | 2 | 3:
                    ModeContext(self.mode_map[mode]).execute(ctx)
                case _:
                    raise ValueError(f"未知模式: {mode}")
        finally:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            logging.info(f"已清理 {self.temp_dir}")
            import keyboard
            keyboard.remove_hotkey(s.STOP_HOTKEY)

    def _process_player(self: Self, window, player_coord, team_coords, screenshot_region, out_path):
        import time, logging
        self.action.click(player_coord, window)
        time.sleep(3)
        img_paths = []
        info_img = str(Path(out_path).with_name(f"{Path(out_path).stem}_info{Path(out_path).suffix}"))
        self.action.screenshot(settings.PLAYER_INFO_REGION, window, info_img)
        img_paths.append(info_img)
        for i, team_coord in enumerate(team_coords, 1):
            self.action.click(team_coord, window)
            team_img = str(Path(out_path).with_name(f"{Path(out_path).stem}_team{i}{Path(out_path).suffix}"))
            self.action.screenshot(screenshot_region, window, team_img)
            img_paths.append(team_img)
            time.sleep(getattr(settings, "ACTION_DELAY", 1.2))
        self.stitcher.stitch(img_paths, out_path, direction="vertical")
        for p in img_paths:
            Path(p).unlink(missing_ok=True)
        return None

    def _notify(self: Self, img_path: str) -> None:
        notify_image(img_path)

    @staticmethod
    def ensure_admin() -> None:
        if sys.platform == 'win32' and not NikkeAutomator.is_admin():
            import shlex
            exe = sys.executable
            script = Path(sys.argv[0]).resolve()
            args = ' '.join([shlex.quote(str(script))] + [shlex.quote(str(a)) for a in sys.argv[1:]])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", exe, args, None, 1
            )
            sys.exit(0)

    @staticmethod
    def is_admin() -> bool:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    @staticmethod
    def select_mode() -> int:
        return select_mode()

# 供 CLI 直接調用

def main(mode: int | None = None) -> None:
    print(f"[DEBUG] main() called, mode = {mode}")
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
    NikkeAutomator.ensure_admin()
    if mode is None:
        print("[DEBUG] main() calling select_mode()...")
        mode = NikkeAutomator.select_mode()
    NikkeAutomator().run(mode)
