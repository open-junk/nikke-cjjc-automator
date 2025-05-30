from ..config import settings

class CoordinateHelper:
    """負責所有座標與比例換算"""
    def __init__(self):
        self.base_width = settings.BASE_WIDTH
        self.base_height = settings.BASE_HEIGHT

    def to_relative(self, abs_coords):
        match abs_coords:
            case (int() | float(), int() | float()):
                return (abs_coords[0] / self.base_width, abs_coords[1] / self.base_height)
            case [(int() | float(), int() | float()), *_]:
                return [(x / self.base_width, y / self.base_height) for x, y in abs_coords]
            case _:
                raise TypeError("輸入必須是元組或列表")

    def region_to_relative(self, left, top, right, bottom):
        return (
            left / self.base_width,
            top / self.base_height,
            (right - left) / self.base_width,
            (bottom - top) / self.base_height,
        )
