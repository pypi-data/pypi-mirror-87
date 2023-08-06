from typing import List

import numpy

from staples_detection.base.result.mask_detection_result import MaskDetectionResult


class GradientDirectionResult:

    def __init__(self):
        self.original_image: numpy.ndarray = None
        self.hsv_image: numpy.ndarray = None
        self.v_channel: numpy.ndarray = None

        self.gradient: numpy.ndarray = None
        self.binarization: numpy.ndarray = None
        self.morphological_closing: numpy.ndarray = None
        self.hole_filling: numpy.ndarray = None
        self.area_filtering: numpy.ndarray = None

        self.mask_dilations: List[numpy.ndarray] = []

        self.final_mask: numpy.ndarray = None
        self.colormask: numpy.ndarray = None

    def set_original_image(self, image: numpy.ndarray):
        self.original_image = image

    def set_hsv_image(self, hsv_image: numpy.ndarray):
        self.hsv_image = hsv_image

    def set_value_channel(self, value_channel: numpy.ndarray):
        self.v_channel = value_channel

    def set_gradient(self, gradient: numpy.ndarray):
        self.gradient = gradient

    def set_binarized_gradient(self, binary_image: numpy.ndarray):
        self.binarization = binary_image

    def set_morphological_closing(self, closing: numpy.ndarray):
        self.morphological_closing = closing

    def set_filled_holes(self, filled_holes: numpy.ndarray):
        self.hole_filling = filled_holes

    def set_area_filtering(self, filtered_area: numpy.ndarray):
        self.area_filtering = filtered_area

    def set_mask_dilations(self, dilations: List[numpy.ndarray]):
        self.mask_dilations = dilations

    def set_final_mask(self, final_mask: numpy.ndarray):
        self.final_mask = final_mask

    def set_colormask(self, colormask: numpy.ndarray):
        self.colormask = colormask


class GradientStapleDetectionResult(MaskDetectionResult):

    def __init__(self,
                 vertical_gradient_result: GradientDirectionResult,
                 horizontal_gradient_result: GradientDirectionResult,
                 final_mask: numpy.ndarray,
                 colormask: numpy.ndarray,
                 elapsed_time: float):

        super(GradientStapleDetectionResult, self).__init__(final_mask, colormask, elapsed_time)

        self.vertical_gradient_result: GradientDirectionResult = vertical_gradient_result
        self.horizontal_gradient_result: GradientDirectionResult = horizontal_gradient_result
