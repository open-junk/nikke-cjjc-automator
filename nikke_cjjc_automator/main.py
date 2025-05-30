# Importing necessary modules and classes
import logging
from nikke_cjjc_automator.model.coordinates import CoordinateHelper
from nikke_cjjc_automator.controller.action import ActionPerformer
from nikke_cjjc_automator.controller.stitch import ImageStitcher
from nikke_cjjc_automator.controller.hotkey import HotkeyManager
from nikke_cjjc_automator.controller.window import WindowManager
from nikke_cjjc_automator.view.notify import notify, notify_image
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
    # Defining attributes with default factories for complex types
    hotkey_mgr: HotkeyManager = field(default_factory=HotkeyManager)
    coord: CoordinateHelper = field(default_factory=CoordinateHelper)
    window_mgr: WindowManager = field(init=False)
    action: ActionPerformer = field(init=False)
    stitcher: ImageStitcher = field(init=False)
    temp_dir: Path = field(init=False)
    mode: Optional[int] = None
    mode_map: dict[int, PredictMode | ReviewMode | AntiBuyMode] = field(init=False)

    def __post_init__(self: Self) -> None:
        # Initializing managers and creating temp directory
        self.window_mgr = WindowManager(self.hotkey_mgr)
        self.action = ActionPerformer(self.hotkey_mgr)
        self.stitcher = ImageStitcher(self.hotkey_mgr)
        self.temp_dir = Path(tempfile.gettempdir()) / "nikke_cjjc_automator"
        # Mapping mode numbers to mode strategies
        self.mode_map = {
            1: PredictMode(),
            2: ReviewMode(),
            3: AntiBuyMode(),
        }

    def run(self: Self, mode: int) -> None:
        import shutil, time, logging
        s = settings
        # Waiting before starting
        logging.info(f"[START_DELAY] Waiting {getattr(s, 'START_DELAY', 3.0)} seconds before starting...")
        time.sleep(getattr(s, "START_DELAY", 3.0))
        self.mode = mode
        self.hotkey_mgr.setup()
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        window = self.window_mgr.find_and_activate()
        logging.info(f"Window activated: {window.title}")
        c = self.coord
        try:
            ctx = {
                'coord': c,
                'settings': s,
                'window': window,
                'automator': self
            }
            # Executing the corresponding mode strategy
            match mode:
                case 1 | 2 | 3:
                    ModeContext(self.mode_map[mode]).execute(ctx)
                case _:
                    raise ValueError(f"Unknown mode: {mode}")
        finally:
            # Cleanup
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            logging.info(f"Cleaned up {self.temp_dir}")
            import keyboard
            keyboard.remove_hotkey(s.STOP_HOTKEY)

    def _process_player(self: Self, window, player_coord, team_coords, screenshot_region, out_path):
        import time, logging
        from pathlib import Path
        c = self.coord
        s = self.config if hasattr(self, 'config') else __import__('nikke_cjjc_automator.config', fromlist=['settings']).settings
        # Waiting after initial player click
        logging.info(f"[INITIAL_PLAYER_DELAY] Waiting {getattr(s, 'INITIAL_PLAYER_DELAY', 2.0)} seconds after initial player click...")
        self.action.click(player_coord, window)
        time.sleep(getattr(s, "INITIAL_PLAYER_DELAY", 2.0))
        img_paths = []
        # Capturing player information
        info_img = str(Path(out_path).with_name(f"{Path(out_path).stem}_info{Path(out_path).suffix}"))
        self.action.screenshot(s.PLAYER_INFO_REGION, window, info_img)
        img_paths.append(info_img)
        # Capturing detailed player information if available
        if hasattr(s, 'PLAYER_DETAILINFO_2_ABS') and hasattr(s, 'PLAYER_INFO_2_REGION'):
            detail2_coord = c.to_relative(s.PLAYER_DETAILINFO_2_ABS)
            self.action.click(detail2_coord, window)
            time.sleep(2.5)
            info2_img = str(Path(out_path).with_name(f"{Path(out_path).stem}_info2{Path(out_path).suffix}"))
            self.action.screenshot(s.PLAYER_INFO_2_REGION, window, info2_img)
            img_paths.append(info2_img)
            if hasattr(s, 'PLAYER_DETAILINFO_3_ABS') and hasattr(s, 'PLAYER_INFO_3_REGION'):
                detail3_coord = c.to_relative(s.PLAYER_DETAILINFO_3_ABS)
                self.action.click(detail3_coord, window)
                time.sleep(1.0)
                info3_img = str(Path(out_path).with_name(f"{Path(out_path).stem}_info3{Path(out_path).suffix}"))
                self.action.screenshot(s.PLAYER_INFO_3_REGION, window, info3_img)
                img_paths.append(info3_img)
                if hasattr(s, 'PLAYER_DETAILINFO_CLOSE_ABS'):
                    close_coord = c.to_relative(s.PLAYER_DETAILINFO_CLOSE_ABS)
                    self.action.click(close_coord, window)
                    time.sleep(0.3)
        # Processing team information
        for i, team_coord in enumerate(team_coords, 1):
            self.action.click(team_coord, window)
            team_img = str(Path(out_path).with_name(f"{Path(out_path).stem}_team{i}{Path(out_path).suffix}"))
            self.action.screenshot(screenshot_region, window, team_img)
            img_paths.append(team_img)
            time.sleep(getattr(s, "ACTION_DELAY", 1.2))
        # Filtering out non-existent image paths
        img_paths = [p for p in img_paths if p and Path(p).exists()]
        self.stitcher.stitch(img_paths, out_path, direction="vertical")
        for p in img_paths:
            Path(p).unlink(missing_ok=True)
        return out_path

    def _notify(self: Self, img_path: str) -> None:
        notify_image(img_path)

    @staticmethod
    def get_manual_path():
        # Determining the manual path based on the execution environment
        if hasattr(sys, "_MEIPASS"):
            return Path(sys._MEIPASS) / "manual.jpg"
        else:
            return Path(__file__).resolve().parent.parent / "img" / "manual.jpg"

    @staticmethod
    def ensure_admin() -> None:
        import shlex
        # Ensuring the program is run as administrator on Windows
        if sys.platform == 'win32' and not NikkeAutomator.is_admin():
            exe = sys.executable
            script = Path(sys.argv[0]).resolve()
            manual_path = NikkeAutomator.get_manual_path()
            if manual_path.exists():
                os.startfile(manual_path)
                notify(
            """Please run this program as administrator. The manual image has been opened automatically.\n\nAfter closing this window, the program will restart with administrator privileges.\n\nIf you run this program as administrator (double-click or CLI mode), this message will not appear again.\n""", "Administrator Privileges Required")
            args = ' '.join([shlex.quote(str(script))] + [shlex.quote(str(a)) for a in sys.argv[1:]])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", exe, args, None, 1
            )
            sys.exit(1)

    @staticmethod
    def is_admin() -> bool:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    @staticmethod
    def select_mode() -> int:
        return select_mode()

# Main function for CLI execution
def main(mode: int | None = None) -> None:
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
    NikkeAutomator.ensure_admin()
    if mode is None:
        mode = NikkeAutomator.select_mode()
    NikkeAutomator().run(mode)
