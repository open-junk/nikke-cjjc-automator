from ..config import settings

class CoordinateHelper:
    """Responsible for all coordinate and ratio conversions."""
    def __init__(self):
        self.base_width = settings.BASE_WIDTH
        self.base_height = settings.BASE_HEIGHT

    def to_relative(self, abs_coords):
        # match abs_coords:
        #     case (int() | float(), int() | float()):
        #         return (abs_coords[0] / self.base_width, abs_coords[1] / self.base_height)
        #     case [(int() | float(), int() | float()), *_]:
        #         return [(x / self.base_width, y / self.base_height) for x, y in abs_coords]
        #     case _:
        #         raise TypeError("Input must be a tuple or list")
        if isinstance(abs_coords, tuple) and len(abs_coords) == 2 and \
              all(isinstance(coord, (int, float)) for coord in abs_coords):
            return (abs_coords[0] / self.base_width, abs_coords[1] / self.base_height)
        elif isinstance(abs_coords, list) and all(
            isinstance(item, (tuple, list)) and len(item) == 2 and
            all(isinstance(coord, (int, float)) for coord in item)
            for item in abs_coords
        ):
            return [(x / self.base_width, y / self.base_height) for x, y in abs_coords]
        else:
            raise TypeError("Input must be a tuple or list")

    def region_to_relative(self, left, top, right, bottom):
        return (
            left / self.base_width,
            top / self.base_height,
            (right - left) / self.base_width,
            (bottom - top) / self.base_height,
        )
