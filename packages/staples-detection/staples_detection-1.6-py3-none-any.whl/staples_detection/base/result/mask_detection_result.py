import numpy


class MaskDetectionResult:

    def __init__(self,
                 final_mask: numpy.ndarray,
                 colormask: numpy.ndarray,
                 elapsed_time: float):

        self.final_binary_mask = final_mask.astype(int)
        self.colormask = colormask
        self.elapsed_time = round(elapsed_time, 5)

        self.final_mask = numpy.zeros_like(self.final_binary_mask).astype(int)
        self.final_mask[self.final_binary_mask == True] = 255
