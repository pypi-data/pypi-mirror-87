from skimage.io import imread

import numpy
import os
import os.path as osp


data_dir = osp.abspath(osp.dirname(__file__))


def get_example_asset(number: int) -> numpy.ndarray:
    return imread(os.path.join(data_dir, f"img00{number}.png"))
