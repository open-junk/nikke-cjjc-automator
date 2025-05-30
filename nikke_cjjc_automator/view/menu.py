import questionary
from typing import Optional

def select_mode() -> Optional[int]:
    return int(questionary.select(
        "請選擇運行模式:",
        choices=[
            ("1: 買馬預測模式（請提前進入投注頁面）", 1),
            ("2: 復盤模式（請提前進入應援結果顯示5隊勝負的頁面）", 2),
            ("3: 反買模式（請提前進入投注頁面）", 3),
        ]
    ).ask())
