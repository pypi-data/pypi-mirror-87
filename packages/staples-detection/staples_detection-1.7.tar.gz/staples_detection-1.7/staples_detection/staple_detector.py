import numpy

from staples_detection.base.result.mask_detection_result import MaskDetectionResult
from staples_detection.base.staple_detection_methods import StapleDetectionMethod
from staples_detection.algorithms import gradient, canny


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
                       ground_truth_mask: numpy.ndarray = None,
                       **kwargs) -> MaskDetectionResult:
        """
        Detects the staples in an image.

        Args:
            method: A StapleDetectionMethod value, representing the method to be used.
            ground_truth_mask: Represents the ground truth mask. If it is passed, the results contains the performance
                               metrics.
            **kwargs: The parameters of the different methods.

        Returns:
            A GradientStapleDetectionResult, containing the partial results of each process and the global elapsed time.
        """
        if method == StapleDetectionMethod.CANNY:
            return canny.generate_canny_mask(self.__image, ground_truth_mask, **kwargs)
        else:
            return gradient.generate_gradient_mask(self.__image, method, ground_truth_mask, **kwargs)
