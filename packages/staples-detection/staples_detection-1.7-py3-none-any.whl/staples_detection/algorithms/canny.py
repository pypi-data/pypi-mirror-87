import cv2
import time
from skimage import img_as_ubyte

from staples_detection.algorithms.utils import *
from staples_detection.base.result.canny_staple_detection_result import CannyStapleDetectionResult


def generate_canny_mask(image: numpy.ndarray, ground_truth_mask: numpy.ndarray = None,
                        **kwargs) -> CannyStapleDetectionResult:
    """
    Detects the staples in an image with a the Canny method.

    Args:
        image: A numpy array, representing the RGB image in [0, 1] range.
        ground_truth_mask: A numpy array, representing the ground truth mask of the detection.
        **kwargs: The parameters of the method.

    Returns:
        A CannyStapleDetectionResult object, containing the results and the elapsed time.
    """
    # PARAMETER EXTRACTION
    gaussian_sigma: float = kwargs.get("gaussian_sigma", 1)
    lower_threshold = kwargs.get("canny_min_threshold", 100)
    upper_threshold = kwargs.get("canny_max_threshold", 200)
    area_threshold = kwargs.get("canny_area_threshold", 40)
    morphological_kernel = kwargs.get("canny_morphological_kernel", numpy.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))
    # END

    elapsed_time = time.time()

    cv_image = img_as_ubyte(image)
    hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

    v_channel = hsv_image[:, :, 2]

    edges = cv2.Canny(v_channel, lower_threshold, upper_threshold)

    number_components, output, stats, centroids = cv2.connectedComponentsWithStats(edges, connectivity=8)
    sizes = stats[1:, -1]
    number_components = number_components - 1

    filtered_image = numpy.zeros(output.shape)
    for i in range(0, number_components):
        if sizes[i] >= area_threshold:
            filtered_image[output == i + 1] = True

    filtered_image = cv2.dilate(filtered_image, morphological_kernel, iterations=2)

    elapsed_time = time.time()-elapsed_time

    return CannyStapleDetectionResult(filtered_image, draw_mask_over_image(image, filtered_image),
                                      elapsed_time, ground_truth_mask)

