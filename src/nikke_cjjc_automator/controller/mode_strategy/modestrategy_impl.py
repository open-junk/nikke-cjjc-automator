from typing import Any
from nikke_cjjc_automator.controller.mode_strategy.mode import ModeStrategy
from pathlib import Path
import time
from datetime import datetime

class PredictMode(ModeStrategy):
    def run(self, ctx: Any) -> None:
        # Unpack context
        c, s, window, automator = ctx['coord'], ctx['settings'], ctx['window'], ctx['automator']
        temp_dir = automator.temp_dir
        output_dir = Path(s.OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        p1_path = temp_dir / "p1.png"
        p2_path = temp_dir / "p2.png"
        out_path = output_dir / f"prediction-{now_str}.png"
        # Process player 1
        automator._process_player(window, c.to_relative(s.PLAYER1_COORD_ABS), c.to_relative(s.TEAM_COORDS_ABS), s.SCREENSHOT_REGION, str(p1_path))
        # Process player 2
        automator._process_player(window, c.to_relative(s.PLAYER2_COORD_ABS), c.to_relative(s.TEAM_COORDS_ABS), s.SCREENSHOT_REGION, str(p2_path))
        # Stitch images horizontally
        automator.stitcher.stitch([
            str(p1_path),
            str(p2_path)
        ], str(out_path), direction="horizontal", spacing=getattr(s, "HORIZONTAL_SPACING", 50))
        # Notify user
        automator._notify(str(out_path))

class ReviewMode(ModeStrategy):
    def run(self, ctx: Any) -> None:
        c, s, window, automator = ctx['coord'], ctx['settings'], ctx['window'], ctx['automator']
        temp_dir = automator.temp_dir
        output_dir = Path(s.OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_img_path = temp_dir / "result.png"
        p1_path = temp_dir / "p1.png"
        p2_path = temp_dir / "p2.png"
        out_path = output_dir / f"review-{now_str}.png"
        # Screenshot result region
        automator.action.screenshot(s.RESULT_SCREENSHOT_REGION, window, str(result_img_path))
        # Process player 1
        automator._process_player(window, c.to_relative(s.PLAYER1_COORD_ABS_M2), c.to_relative(s.TEAM_COORDS_ABS), s.SCREENSHOT_REGION, str(p1_path))
        # Process player 2
        automator._process_player(window, c.to_relative(s.PLAYER2_COORD_ABS_M2), c.to_relative(s.TEAM_COORDS_ABS), s.SCREENSHOT_REGION, str(p2_path))
        # Stitch images horizontally with result in the middle
        automator.stitcher.stitch([
            str(p1_path),
            str(result_img_path),
            str(p2_path)
        ], str(out_path), direction="horizontal", spacing=0, background_color=(255,255,255))
        automator._notify(str(out_path))

class AntiBuyMode(ModeStrategy):
    def run(self, ctx: Any) -> None:
        c, s, window, automator = ctx['coord'], ctx['settings'], ctx['window'], ctx['automator']
        temp_dir = automator.temp_dir
        output_dir = Path(s.OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        vote_img_path = temp_dir / "vote.png"
        p1_path = temp_dir / "p1.png"
        p2_path = temp_dir / "p2.png"
        out_path = output_dir / f"anti_buy-{now_str}.png"
        # Screenshot vote region
        automator.action.screenshot(s.PEOPLE_VOTE_REGION, window, str(vote_img_path))
        # Process player 1
        automator._process_player(window, c.to_relative(s.PLAYER1_COORD_ABS), c.to_relative(s.TEAM_COORDS_ABS), s.SCREENSHOT_REGION, str(p1_path))
        # Process player 2
        automator._process_player(window, c.to_relative(s.PLAYER2_COORD_ABS), c.to_relative(s.TEAM_COORDS_ABS), s.SCREENSHOT_REGION, str(p2_path))
        # Stitch images horizontally with vote in the middle
        automator.stitcher.stitch([
            str(p1_path),
            str(vote_img_path),
            str(p2_path)
        ], str(out_path), direction="horizontal", spacing=0, background_color=(255,255,255))
        automator._notify(str(out_path))

class LeaguePredictMode(ModeStrategy):
    def run(self, ctx: Any) -> None:
        c, s, window, automator = ctx['coord'], ctx['settings'], ctx['window'], ctx['automator']
        temp_dir = automator.temp_dir
        output_dir = Path(s.OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Get player entry coordinates (should be 4 entries)
        player_entries, player_img_paths = [
            c.to_relative(getattr(s, "PLAYER1_COORD_ABS_M4", [1480, 860])),
            c.to_relative(getattr(s, "PLAYER2_COORD_ABS_M4", [1480, 1130])),
            c.to_relative(getattr(s, "PLAYER3_COORD_ABS_M4", [1480, 1400])),
            c.to_relative(getattr(s, "PLAYER4_COORD_ABS_M4", [1480, 1670]))
        ], []
        for i, player_entry_rel in enumerate(player_entries):
            player_num = i + 1
            player_img_path = temp_dir / f"league_player_{player_num}.png"
            # Process each player (simulate _process_player, but can be customized)
            automator._process_player(window, player_entry_rel, c.to_relative(s.TEAM_COORDS_ABS), s.SCREENSHOT_REGION, str(player_img_path))
            player_img_paths.append(str(player_img_path))
        # Output file
        out_path = output_dir / f"league-predict-{now_str}.png"
        # Stitch all 4 player images horizontally
        automator.stitcher.stitch(player_img_paths, str(out_path), direction="horizontal", spacing=getattr(s, "HORIZONTAL_SPACING", 20))
        automator._notify(str(out_path))
