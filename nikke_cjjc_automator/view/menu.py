import sys
import questionary
from typing import Optional

SELECT_MODE_CHOICES = [
    "1: 買馬預測模式（請提前進入投注頁面）",
    "2: 復盤模式（請提前進入應援結果顯示5隊勝負的頁面）",
    "3: 反買模式（請提前進入投注頁面）",
]

def select_mode() -> Optional[int]:
    try:
        label = questionary.select(
            "请选择运行模式",
            choices=SELECT_MODE_CHOICES
        ).ask()
    except KeyboardInterrupt:
        sys.exit(0)
    if label is None:
        sys.exit(0)
    return SELECT_MODE_CHOICES.index(label) + 1