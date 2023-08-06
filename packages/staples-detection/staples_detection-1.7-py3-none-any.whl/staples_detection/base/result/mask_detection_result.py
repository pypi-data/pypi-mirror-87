import numpy

from staples_detection.base.performance.mask_performance import MaskPerformance


class MaskDetectionResult:
    """
    Object that stores the results of any mask detection algorithm. Furthermore, contains the performance metrics
    of the classification.
    """

    def __init__(self,
                 final_mask: numpy.ndarray,
                 colormask: numpy.ndarray,
                 elapsed_time: float,
                 ground_truth: numpy.ndarray = None):

        self.final_binary_mask = final_mask.astype(int)
        self.colormask = colormask
        self.elapsed_time = round(elapsed_time, 5)

        self.final_mask = numpy.zeros_like(self.final_binary_mask).astype(int)
        self.final_mask[self.final_binary_mask == True] = 255

        self.performance: MaskPerformance
        if ground_truth is None:
            self.performance = None
        else:
            self.performance = MaskPerformance()
            self.performance.compute_raw_performance(prediction_mask=self.final_mask, ground_truth_mask=ground_truth)
