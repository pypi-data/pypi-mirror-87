import numpy


class MaskDetectionResult:

    def __init__(self,
                 final_mask: numpy.ndarray,
                 colormask: numpy.ndarray,
                 elapsed_time: float):

        self.final_mask = final_mask
        self.colormask = colormask
        self.elapsed_time = round(elapsed_time, 5)
