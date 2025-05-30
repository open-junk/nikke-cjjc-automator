import sys
from pathlib import Path
from dynaconf import Dynaconf
import shutil

SETTINGS_VERSION = "1.0.0"  # Keep in sync with settings.default.toml

# Handle bundle path for PyInstaller onefile mode
if hasattr(sys, "_MEIPASS"):
    BUNDLE_DIR = Path(sys._MEIPASS)
    APP_ROOT = Path(sys.executable).parent
else:
    BUNDLE_DIR = Path(__file__).parent.parent
    APP_ROOT = BUNDLE_DIR

SETTINGS_PATH = APP_ROOT / "settings.toml"
DEFAULT_SETTINGS_PATH = APP_ROOT / "settings.default.toml"
BUNDLE_DEFAULT_SETTINGS_PATH = BUNDLE_DIR / "settings.default.toml"

# If settings.toml does not exist, copy default from bundle or app root
if not SETTINGS_PATH.exists():
    if BUNDLE_DEFAULT_SETTINGS_PATH.exists():
        shutil.copy(BUNDLE_DEFAULT_SETTINGS_PATH, SETTINGS_PATH)
    elif DEFAULT_SETTINGS_PATH.exists():
        shutil.copy(DEFAULT_SETTINGS_PATH, SETTINGS_PATH)
    else:
        raise FileNotFoundError(f"Cannot find {BUNDLE_DEFAULT_SETTINGS_PATH} or {DEFAULT_SETTINGS_PATH}")

settings = Dynaconf(
    envvar_prefix="NIKKE",
    settings_files=[str(SETTINGS_PATH)],
)

# Version check
user_ver = getattr(settings, "SETTINGS_VERSION", None)
if user_ver != SETTINGS_VERSION:
    print(f"[Warning] Config version mismatch: current settings.toml version {user_ver}, recommended to match program version {SETTINGS_VERSION}!")

# settings.setenv("default")  # Force switch to default environment if needed

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


# Calculate and assign all region settings in relative coordinates
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
