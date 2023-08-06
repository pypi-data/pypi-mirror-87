from skimage.color import rgb2hsv

import numpy


def convert_hsv(image: numpy.ndarray) -> numpy.ndarray:
    """
    Converts an image in the RGB colour space into the HSV colour space.

    Args:
        image: A numpy array, representing the RGB image in [0, 1] range.

    Returns:
        A numpy array, representing the input image in HSV colour space.
    """
    return rgb2hsv(image)


def get_value_channel(image: numpy.ndarray) -> numpy.ndarray:
    """
    Gets the Value channel of the image. The input image is assumed to be represented in the HSV colour space.

    Args:
        image: A numpy array, representing the HSV image in [0, 1] range.

    Returns:
        A two dimensional numpy array, representing the value channel.
    """
    return image[:, :, 2]


def draw_mask_over_image(image: numpy.ndarray, mask: numpy.ndarray, color=None):
    """
    Draws the mask over the image. All the pixels marked as True will be overwritten in the original image wih a
    certain colour.

    Args:
        image: A numpy array, representing the RGB image in [0, 1] range.
        mask: A two dimensional array, representing the mask of the staples. It must be white with black background;
              that is, the objects must be masked as True.
        color: An RGB colour, representing the color that will be used to draw the objects in the image.

    Returns:
        A numpy array, representing the RGB image in [0, 1] range with the drawn objects.
    """
    if color is None:
        color = [70, 253, 52]

    colormask = image.copy()
    colormask[mask[:, :] == True] = color

    return colormask
