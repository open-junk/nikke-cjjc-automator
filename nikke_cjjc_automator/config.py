import sys
from pathlib import Path
from dynaconf import Dynaconf


def resource_path(filename: str) -> str:
    # 若為 PyInstaller 執行環境，資源會被放在 _MEIPASS
    if hasattr(sys, "_MEIPASS"):
        return str(Path(sys._MEIPASS) / filename)
    # 開發環境下，尋找專案根目錄下的設定檔
    return str((Path(__file__).parent.parent / filename).resolve())


settings = Dynaconf(
    envvar_prefix="NIKKE",
    settings_files=[resource_path("settings.toml")],
)

settings.setenv("default")  # 強制切到 default 環境

# Debug print for troubleshooting
print("[DEBUG] settings.toml path:", resource_path("settings.toml"))
print("[DEBUG] BASE_WIDTH:", settings.get("BASE_WIDTH"))
print("[DEBUG] SCREENSHOT_LEFT_ABS:", settings.get("SCREENSHOT_LEFT_ABS"))


def calc_region(left, top, right, bottom, base_width, base_height):
    if None in (left, top, right, bottom, base_width, base_height):
        raise ValueError(
            f"calc_region got None: {left=}, {top=}, {right=}, {bottom=}, {base_width=}, {base_height=}"
        )
    return [
        left / base_width,
        top / base_height,
        (right - left) / base_width,
        (bottom - top) / base_height,
    ]


settings.SCREENSHOT_REGION = calc_region(
    settings.get("SCREENSHOT_LEFT_ABS"),
    settings.get("SCREENSHOT_TOP_ABS"),
    settings.get("SCREENSHOT_RIGHT_ABS"),
    settings.get("SCREENSHOT_BOTTOM_ABS"),
    settings.get("BASE_WIDTH"),
    settings.get("BASE_HEIGHT"),
)
settings.PLAYER_INFO_REGION = calc_region(
    settings.get("PLAYER_INFO_LEFT_ABS"),
    settings.get("PLAYER_INFO_TOP_ABS"),
    settings.get("PLAYER_INFO_RIGHT_ABS"),
    settings.get("PLAYER_INFO_BOTTOM_ABS"),
    settings.get("BASE_WIDTH"),
    settings.get("BASE_HEIGHT"),
)
settings.PLAYER_INFO_2_REGION = calc_region(
    settings.get("PLAYER_INFO_2_LEFT_ABS"),
    settings.get("PLAYER_INFO_2_TOP_ABS"),
    settings.get("PLAYER_INFO_2_RIGHT_ABS"),
    settings.get("PLAYER_INFO_2_BOTTOM_ABS"),
    settings.get("BASE_WIDTH"),
    settings.get("BASE_HEIGHT"),
)
settings.PLAYER_INFO_3_REGION = calc_region(
    settings.get("PLAYER_INFO_3_LEFT_ABS"),
    settings.get("PLAYER_INFO_3_TOP_ABS"),
    settings.get("PLAYER_INFO_3_RIGHT_ABS"),
    settings.get("PLAYER_INFO_3_BOTTOM_ABS"),
    settings.get("BASE_WIDTH"),
    settings.get("BASE_HEIGHT"),
)
settings.PEOPLE_VOTE_REGION = calc_region(
    settings.get("PEOPLE_VOTE_LEFT_ABS"),
    settings.get("PEOPLE_VOTE_TOP_ABS"),
    settings.get("PEOPLE_VOTE_RIGHT_ABS"),
    settings.get("PEOPLE_VOTE_BOTTOM_ABS"),
    settings.get("BASE_WIDTH"),
    settings.get("BASE_HEIGHT"),
)
settings.RESULT_SCREENSHOT_REGION = calc_region(
    settings.get("RESULT_SCREENSHOT_LEFT_ABS"),
    settings.get("RESULT_SCREENSHOT_TOP_ABS"),
    settings.get("RESULT_SCREENSHOT_RIGHT_ABS"),
    settings.get("RESULT_SCREENSHOT_BOTTOM_ABS"),
    settings.get("BASE_WIDTH"),
    settings.get("BASE_HEIGHT"),
)
