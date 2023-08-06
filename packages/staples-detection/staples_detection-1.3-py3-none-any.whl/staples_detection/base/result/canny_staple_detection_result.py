import numpy

from staples_detection.base.result.mask_detection_result import MaskDetectionResult


class CannyStapleDetectionResult(MaskDetectionResult):

    def __init__(self,
                 final_mask: numpy.ndarray,
                 colormask: numpy.ndarray,
                 elapsed_time: float):

        super(CannyStapleDetectionResult, self).__init__(final_mask, colormask, elapsed_time)


