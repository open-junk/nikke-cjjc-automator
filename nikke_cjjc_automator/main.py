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
        s = settings
        # 執行前延遲提示
        logging.info(f"[START_DELAY] 啟動前等待 {getattr(s, 'START_DELAY', 3.0)} 秒...")
        time.sleep(getattr(s, "START_DELAY", 3.0))
        self.mode = mode
        self.hotkey_mgr.setup()
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        window = self.window_mgr.find_and_activate()
        logging.info(f"視窗已激活: {window.title}")
        c = self.coord
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
        from pathlib import Path
        c = self.coord
        s = self.config if hasattr(self, 'config') else __import__('nikke_cjjc_automator.config', fromlist=['settings']).settings
        logging.info(f"[INITIAL_PLAYER_DELAY] 玩家初始點擊後等待 {getattr(s, 'INITIAL_PLAYER_DELAY', 2.0)} 秒...")
        self.action.click(player_coord, window)
        time.sleep(getattr(s, "INITIAL_PLAYER_DELAY", 2.0))
        img_paths = []
        # 玩家資訊1
        info_img = str(Path(out_path).with_name(f"{Path(out_path).stem}_info{Path(out_path).suffix}"))
        self.action.screenshot(s.PLAYER_INFO_REGION, window, info_img)
        img_paths.append(info_img)
        # 玩家詳細資訊2
        if hasattr(s, 'PLAYER_DETAILINFO_2_ABS') and hasattr(s, 'PLAYER_INFO_2_REGION'):
            detail2_coord = c.to_relative(s.PLAYER_DETAILINFO_2_ABS)
            self.action.click(detail2_coord, window)
            time.sleep(2.5)
            info2_img = str(Path(out_path).with_name(f"{Path(out_path).stem}_info2{Path(out_path).suffix}"))
            self.action.screenshot(s.PLAYER_INFO_2_REGION, window, info2_img)
            img_paths.append(info2_img)
            # 玩家詳細資訊3
            if hasattr(s, 'PLAYER_DETAILINFO_3_ABS') and hasattr(s, 'PLAYER_INFO_3_REGION'):
                detail3_coord = c.to_relative(s.PLAYER_DETAILINFO_3_ABS)
                self.action.click(detail3_coord, window)
                time.sleep(1.0)
                info3_img = str(Path(out_path).with_name(f"{Path(out_path).stem}_info3{Path(out_path).suffix}"))
                self.action.screenshot(s.PLAYER_INFO_3_REGION, window, info3_img)
                img_paths.append(info3_img)
                # 關閉詳細資訊
                if hasattr(s, 'PLAYER_DETAILINFO_CLOSE_ABS'):
                    close_coord = c.to_relative(s.PLAYER_DETAILINFO_CLOSE_ABS)
                    self.action.click(close_coord, window)
                    time.sleep(0.3)
        # 處理隊伍
        for i, team_coord in enumerate(team_coords, 1):
            self.action.click(team_coord, window)
            team_img = str(Path(out_path).with_name(f"{Path(out_path).stem}_team{i}{Path(out_path).suffix}"))
            self.action.screenshot(screenshot_region, window, team_img)
            img_paths.append(team_img)
            time.sleep(getattr(s, "ACTION_DELAY", 1.2))
        # 過濾掉 None 或不存在的檔案
        img_paths = [p for p in img_paths if p and Path(p).exists()]
        self.stitcher.stitch(img_paths, out_path, direction="vertical")
        for p in img_paths:
            Path(p).unlink(missing_ok=True)
        return out_path

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
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
    NikkeAutomator.ensure_admin()
    if mode is None:
        mode = NikkeAutomator.select_mode()
    NikkeAutomator().run(mode)
