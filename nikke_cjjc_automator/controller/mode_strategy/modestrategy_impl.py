from typing import Any
from nikke_cjjc_automator.controller.mode_strategy.mode import ModeStrategy

class PredictMode(ModeStrategy):
    def run(self, ctx: Any) -> None:
        c, s, window, automator = ctx['coord'], ctx['settings'], ctx['window'], ctx['automator']
        p1 = automator._process_player(window, c.to_relative(s.PLAYER1_COORD_ABS), c.to_relative(s.TEAM_COORDS_ABS), s.SCREENSHOT_REGION, f"{automator.temp_dir}/p1.png")
        automator.action.click(c.to_relative(s.EXIT_COORD_ABS), window)
        import time
        time.sleep(1)
        p2 = automator._process_player(window, c.to_relative(s.PLAYER2_COORD_ABS), c.to_relative(s.TEAM_COORDS_ABS), s.SCREENSHOT_REGION, f"{automator.temp_dir}/p2.png")
        out = f"{automator.temp_dir}/final1.png"
        automator.stitcher.stitch([p1, p2], out, direction="horizontal", spacing=getattr(s, "HORIZONTAL_SPACING", 50))
        automator._notify(out)

class ReviewMode(ModeStrategy):
    def run(self, ctx: Any) -> None:
        c, s, window, automator = ctx['coord'], ctx['settings'], ctx['window'], ctx['automator']
        result_img = f"{automator.temp_dir}/result.png"
        automator.action.screenshot(s.RESULT_SCREENSHOT_REGION, window, result_img)
        p1 = automator._process_player(window, c.to_relative(s.PLAYER1_COORD_ABS_M2), c.to_relative(s.TEAM_COORDS_ABS), s.SCREENSHOT_REGION, f"{automator.temp_dir}/p1.png")
        automator.action.click(c.to_relative(s.EXIT_COORD_ABS), window)
        import time
        time.sleep(1)
        p2 = automator._process_player(window, c.to_relative(s.PLAYER2_COORD_ABS_M2), c.to_relative(s.TEAM_COORDS_ABS), s.SCREENSHOT_REGION, f"{automator.temp_dir}/p2.png")
        out = f"{automator.temp_dir}/final2.png"
        automator.stitcher.stitch([p1, result_img, p2], out, direction="horizontal", spacing=0, background_color=(255,255,255))
        automator._notify(out)

class AntiBuyMode(ModeStrategy):
    def run(self, ctx: Any) -> None:
        c, s, window, automator = ctx['coord'], ctx['settings'], ctx['window'], ctx['automator']
        vote_img = f"{automator.temp_dir}/vote.png"
        automator.action.screenshot(s.PEOPLE_VOTE_REGION, window, vote_img)
        p1 = automator._process_player(window, c.to_relative(s.PLAYER1_COORD_ABS), c.to_relative(s.TEAM_COORDS_ABS), s.SCREENSHOT_REGION, f"{automator.temp_dir}/p1.png")
        automator.action.click(c.to_relative(s.EXIT_COORD_ABS), window)
        import time
        time.sleep(1)
        p2 = automator._process_player(window, c.to_relative(s.PLAYER2_COORD_ABS), c.to_relative(s.TEAM_COORDS_ABS), s.SCREENSHOT_REGION, f"{automator.temp_dir}/p2.png")
        out = f"{automator.temp_dir}/final3.png"
        automator.stitcher.stitch([p1, vote_img, p2], out, direction="horizontal", spacing=0, background_color=(255,255,255))
        automator._notify(out)
