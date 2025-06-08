import sys
import os
import questionary
from typing import Optional

SELECT_MODE_CHOICES = [
    "1: Prediction Mode (Please enter the betting page in advance)",
    "2: Review Mode (Please enter the result page showing 5 teams in advance)",
    "3: Anti-Buy Mode (Please enter the betting page in advance)",
    "4: League Prediction Mode (Please enter the league prediction page in advance)",
]

def select_mode() -> Optional[int]:
    try:
        label = questionary.select(
            "Please select a run mode",
            choices=SELECT_MODE_CHOICES
        ).ask()
    except KeyboardInterrupt:
        sys.exit(0)
    if label is None:
        sys.exit(0)
    return SELECT_MODE_CHOICES.index(label) + 1