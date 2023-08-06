from scipy.ndimage import convolve
from skimage import morphology

import scipy
import time

from staples_detection.algorithms.utils import *
from staples_detection.base.staple_detection_methods import StapleDetectionMethod
from staples_detection.base.result.gradient_staple_detection_result import GradientDirectionResult, \
    GradientStapleDetectionResult


def generate_gradient_mask(image: numpy.ndarray,
                           gradient_method: StapleDetectionMethod,
                           **kwargs) -> GradientStapleDetectionResult:
    """
    Detects the staples in an image with a certain method.

    Args:
        image: A numpy array, representing the RGB image in [0, 1] range.
        gradient_method: A StapleDetectionMethod value, representing the method to be used.
        **kwargs: The parameters of the different methods.

    Returns:
        A GradientStapleDetectionResult, containing the partial results of each process and the global elapsed time.
    """
    if gradient_method == StapleDetectionMethod.COMBINED_GRADIENT:

        elapsed_time = time.time()
        vertical_gradient_result = generate_gradient_staple_result(image, StapleDetectionMethod.VERTICAL_GRADIENT,
                                                                   **kwargs)
        horizontal_gradient_result = generate_gradient_staple_result(image, StapleDetectionMethod.HORIZONTAL_GRADIENT,
                                                                     **kwargs)

        final_mask = vertical_gradient_result.final_mask | horizontal_gradient_result.final_mask
        colormask = draw_mask_over_image(image, final_mask)
        elapsed_time = time.time() - elapsed_time

        return GradientStapleDetectionResult(vertical_gradient_result=vertical_gradient_result,
                                             horizontal_gradient_result=horizontal_gradient_result,
                                             final_mask=final_mask,
                                             colormask=colormask,
                                             elapsed_time=elapsed_time)

    elif gradient_method == StapleDetectionMethod.VERTICAL_GRADIENT:
        elapsed_time = time.time()
        vertical_gradient_result = generate_gradient_staple_result(image, StapleDetectionMethod.VERTICAL_GRADIENT,
                                                                   **kwargs)
        elapsed_time = time.time() - elapsed_time

        return GradientStapleDetectionResult(vertical_gradient_result=vertical_gradient_result,
                                             horizontal_gradient_result=None,
                                             final_mask=vertical_gradient_result.final_mask,
                                             colormask=vertical_gradient_result.colormask,
                                             elapsed_time=elapsed_time)

    elif gradient_method == StapleDetectionMethod.HORIZONTAL_GRADIENT:
        elapsed_time = time.time()
        horizontal_gradient_result = generate_gradient_staple_result(image, StapleDetectionMethod.HORIZONTAL_GRADIENT,
                                                                     **kwargs)
        elapsed_time = time.time() - elapsed_time

        return GradientStapleDetectionResult(vertical_gradient_result=None,
                                             horizontal_gradient_result=horizontal_gradient_result,
                                             final_mask=horizontal_gradient_result.final_mask,
                                             colormask=horizontal_gradient_result.colormask,
                                             elapsed_time=elapsed_time)


def generate_gradient_staple_result(image: numpy.ndarray, gradient_method: StapleDetectionMethod,
                                    **kwargs) -> GradientDirectionResult:
    """
    Detects the staples with a certain method.

    Args:
        image: A numpy array, representing the RGB image in [0, 1] range.
        gradient_method: A StapleDetectionMethod value, representing the method to be used.
        **kwargs: The parameters of the different methods.

    Returns:
        A GradientDirectionResult object, representing the partial results.
    """
    # PARAMETER EXTRACTION
    gradient_binarization_threshold: float = kwargs.get("gradient_binarization_threshold", 60 / 255)
    morphological_closing_se: numpy.ndarray = kwargs.get("morphological_closing_structuring_element",
                                                         numpy.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))
    area_filtering_threshold: float = kwargs.get("area_filtering_threshold", 50)
    number_dilations: int = kwargs.get("mask_number_dilations", 4)
    morphological_dilation_se: numpy.ndarray = kwargs.get("morphological_dilation_structuring_element",
                                                          numpy.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))
    # END
    result = GradientDirectionResult()
    result.set_original_image(image)

    hsv_image = convert_hsv(image=image)
    result.set_hsv_image(hsv_image)

    value_channel = get_value_channel(image=hsv_image)
    result.set_value_channel(value_channel)

    gradient: numpy.ndarray = None
    if gradient_method == StapleDetectionMethod.VERTICAL_GRADIENT:
        gradient = sobel_vertical_gradient(value_channel)
    elif gradient_method == StapleDetectionMethod.HORIZONTAL_GRADIENT:
        gradient = sobel_horizontal_gradient(value_channel)
    result.set_gradient(gradient)

    binary_image = binarize_image(gradient, gradient_binarization_threshold)
    result.set_binarized_gradient(binary_image)

    closing = morphological_closing(binary_image, morphological_closing_se)
    result.set_morphological_closing(closing)

    hole_filling = fill_small_holes(closing)
    result.set_filled_holes(hole_filling)

    area_filtering = remove_small_objects(hole_filling, area_filtering_threshold)
    result.set_area_filtering(area_filtering)

    dilated_mask = area_filtering
    dilated_masks = [dilated_mask]
    for _ in range(number_dilations):
        dilated_mask = morphological_dilation(dilated_mask, morphological_dilation_se)
        dilated_masks.append(dilated_mask)
    result.set_mask_dilations(dilated_masks)
    result.set_final_mask(dilated_mask)

    colormask = draw_mask_over_image(image, dilated_mask)
    result.set_colormask(colormask)

    return result


def sobel_vertical_gradient(image: numpy.ndarray) -> numpy.ndarray:
    """
    Computes the Sobel gradient in the vertical direction.

    Args:
        image: A two dimensional array, representing the image from which the vertical gradient will be calculated.

    Returns:
        A two dimensional array, representing the vertical gradient of the image.
    """
    ky = numpy.array([[1, 2, 1],
                      [0, 0, 0],
                      [-1, -2, -1]])
    return scipy.ndimage.convolve(image, ky)


def sobel_horizontal_gradient(image: numpy.ndarray) -> numpy.ndarray:
    """
    Computes the Sobel gradient in the horizontal direction.

    Args:
        image: A two dimensional array, representing the image from which the horizontal gradient will be calculated.

    Returns:
        A two dimensional array, representing the horizontal gradient of the image.
    """
    kx = numpy.array([[-1, 0, 1],
                      [-2, 0, 2],
                      [-1, 0, 1]])
    return scipy.ndimage.convolve(image, kx)


def binarize_image(image: numpy.ndarray, threshold: float) -> numpy.ndarray:
    """
    Binarizes the image with a threshold.

    Args:
        image: A two dimensional array, representing the image to be binarized.
        threshold: A float value, representing the threshold in the binarization.

    Returns:
        A two dimensional array, representing the binary image.
    """
    binary_image = image.copy()

    binary_image[binary_image > threshold] = 1
    binary_image[binary_image <= threshold] = 0

    return binary_image


def morphological_closing(image: numpy.ndarray, structuring_element: numpy.ndarray) -> numpy.ndarray:
    """
    Computes the morphological closing in a binary image.

    Args:
        image: A two dimensional array, representing the binary image.
        structuring_element: A two dimensional array, representing the structuring element to use in the closing.

    Returns:
        A two dimensional array, representing the closed version of the input binary image.
    """
    return morphology.binary_closing(image, structuring_element)


def morphological_dilation(image: numpy.ndarray, structuring_element: numpy.ndarray) -> numpy.ndarray:
    """
    Computes the morphological dilation in a binary image.

    Args:
        image: A two dimensional array, representing the binary image.
        structuring_element: A two dimensional array, representing the structuring element to use in the dilation.

    Returns:
        A two dimensional array, representing the dilated version of the input binary image.
    """
    return morphology.binary_dilation(image, structuring_element)


def fill_small_holes(image: numpy.ndarray) -> numpy.ndarray:
    """
    Fills the small holes in a binary image.

    Args:
        image: A two dimensional array, representing the binary image.

    Returns:
        A two dimensional array, representing the filled version of the input binary image.
    """
    return scipy.ndimage.binary_fill_holes(image)


def remove_small_objects(image: numpy.ndarray, area: float) -> numpy.ndarray:
    """
    Removes the connected components in a binary image which area is less than the threshold.

    Args:
        image: A two dimensional array, representing the binary image.
        area: A float number, representing the threshold of the area.

    Returns:
        A two dimensional array, representing the image with the small objects removed.
    """
    return morphology.remove_small_objects(image, area)

