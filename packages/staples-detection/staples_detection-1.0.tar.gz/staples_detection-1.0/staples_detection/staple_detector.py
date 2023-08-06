import numpy

from staples_detection.base.staple_detection_methods import StapleDetectionMethod
from staples_detection.algorithms.utils import generate_mask
from staples_detection.base.staple_detection_result import GradientStapleDetectionResult


class StapleDetector:

    def __init__(self, image: numpy.ndarray):
        """
        Initializes the object that detects the staples in a given image.

        Args:
            image: A numpy array, representing the BGR image of the staples.
        """
        self.__image = image

    def detect_staples(self,
                       method: StapleDetectionMethod = StapleDetectionMethod.COMBINED_GRADIENT,
                       **kwargs) -> GradientStapleDetectionResult:
        """
        Detects the staples in an image.

        Args:
            method: A StapleDetectionMethod value, representing the method to be used.
            **kwargs: The parameters of the different methods.

        Returns:
            A GradientStapleDetectionResult, containing the partial results of each process and the global elapsed time.
        """
        return generate_mask(self.__image, method, **kwargs)
