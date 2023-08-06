from enum import Enum


class StapleDetectionMethod(Enum):
    VERTICAL_GRADIENT = 0
    HORIZONTAL_GRADIENT = 1
    COMBINED_GRADIENT = 2
    CANNY = 3
