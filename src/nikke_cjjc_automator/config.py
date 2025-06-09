import sys
from pathlib import Path
from dynaconf import Dynaconf
import shutil
import logging

SETTINGS_VERSION = "1.1.0"  # Keep in sync with settings.default.toml

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

settings = Dynaconf(
    envvar_prefix="NIKKE",
    settings_files=[str(SETTINGS_PATH)],
)

def ensure_settings_file():
    """Ensure settings.toml exists, copying from default if needed."""
    if not SETTINGS_PATH.exists():
        if BUNDLE_DEFAULT_SETTINGS_PATH.exists():
            logging.info(f"Copying default settings from {BUNDLE_DEFAULT_SETTINGS_PATH} to {SETTINGS_PATH}")
            shutil.copy(BUNDLE_DEFAULT_SETTINGS_PATH, SETTINGS_PATH)
        elif DEFAULT_SETTINGS_PATH.exists():
            logging.info(f"Copying default settings from {DEFAULT_SETTINGS_PATH} to {SETTINGS_PATH}")
            shutil.copy(DEFAULT_SETTINGS_PATH, SETTINGS_PATH)
        else:
            raise FileNotFoundError(f"Cannot find {BUNDLE_DEFAULT_SETTINGS_PATH} or {DEFAULT_SETTINGS_PATH}")

def check_settings_version():
    """Check if the user's settings.toml version matches the required version."""
    user_ver = getattr(settings, "SETTINGS_VERSION", None)
    if user_ver != SETTINGS_VERSION:
        logging.warning(f"settings.toml version {user_ver} does not match required version {SETTINGS_VERSION}.\n"
              f"To auto-apply the latest settings, delete your settings.toml and restart the program.")

def ensure_settings():
    """Ensure settings file exists and is up-to-date."""
    ensure_settings_file()
    check_settings_version()

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
    getattr(settings, "SCREENSHOT_LEFT_ABS", 1433),
    getattr(settings, "SCREENSHOT_TOP_ABS", 1134),
    getattr(settings, "SCREENSHOT_RIGHT_ABS", 2417),
    getattr(settings, "SCREENSHOT_BOTTOM_ABS", 1530),
    getattr(settings, "BASE_WIDTH", 3840),
    getattr(settings, "BASE_HEIGHT", 2160),
)
settings.PLAYER_INFO_REGION = calc_region(
    getattr(settings, "PLAYER_INFO_LEFT_ABS", 1433),
    getattr(settings, "PLAYER_INFO_TOP_ABS", 768),
    getattr(settings, "PLAYER_INFO_RIGHT_ABS", 2417),
    getattr(settings, "PLAYER_INFO_BOTTOM_ABS", 963),
    getattr(settings, "BASE_WIDTH", 3840),
    getattr(settings, "BASE_HEIGHT", 2160),
)
settings.PLAYER_INFO_2_REGION = calc_region(
    getattr(settings, "PLAYER_INFO_2_LEFT_ABS", 1433),
    getattr(settings, "PLAYER_INFO_2_TOP_ABS", 1344),
    getattr(settings, "PLAYER_INFO_2_RIGHT_ABS", 2417),
    getattr(settings, "PLAYER_INFO_2_BOTTOM_ABS", 1529),
    getattr(settings, "BASE_WIDTH", 3840),
    getattr(settings, "BASE_HEIGHT", 2160),
)
settings.PLAYER_INFO_3_REGION = calc_region(
    getattr(settings, "PLAYER_INFO_3_LEFT_ABS", 1433),
    getattr(settings, "PLAYER_INFO_3_TOP_ABS", 1768),
    getattr(settings, "PLAYER_INFO_3_RIGHT_ABS", 2417),
    getattr(settings, "PLAYER_INFO_3_BOTTOM_ABS", 1850),
    getattr(settings, "BASE_WIDTH", 3840),
    getattr(settings, "BASE_HEIGHT", 2160),
)
settings.PEOPLE_VOTE_REGION = calc_region(
    getattr(settings, "PEOPLE_VOTE_LEFT_ABS", 1395),
    getattr(settings, "PEOPLE_VOTE_TOP_ABS", 285),
    getattr(settings, "PEOPLE_VOTE_RIGHT_ABS", 2433),
    getattr(settings, "PEOPLE_VOTE_BOTTOM_ABS", 1944),
    getattr(settings, "BASE_WIDTH", 3840),
    getattr(settings, "BASE_HEIGHT", 2160),
)
settings.RESULT_SCREENSHOT_REGION = calc_region(
    getattr(settings, "RESULT_SCREENSHOT_LEFT_ABS", 1600),
    getattr(settings, "RESULT_SCREENSHOT_TOP_ABS", 958),
    getattr(settings, "RESULT_SCREENSHOT_RIGHT_ABS", 2109),
    getattr(settings, "RESULT_SCREENSHOT_BOTTOM_ABS", 1651),
    getattr(settings, "BASE_WIDTH", 3840),
    getattr(settings, "BASE_HEIGHT", 2160),
)

ensure_settings_file()