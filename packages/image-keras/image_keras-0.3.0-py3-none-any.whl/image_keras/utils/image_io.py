import os
from typing import Tuple

import cv2
import numpy as np
from PIL import Image


def image_read(folder: str, name: str, verbose: int = 1) -> Tuple[str, np.ndarray]:
    print("Image read {}".format(name)) if verbose == 1 else None
    return name, cv2.imread(os.path.join(folder, name))


def image_read_16bit_grayscale(folder: str, name: str, verbose: int = 1):
    print("Image read {}".format(name)) if verbose == 1 else None
    return name, cv2.imread(os.path.join(folder, name), cv2.IMREAD_ANYDEPTH)


def image_write(folder: str, name: str, img: np.ndarray, verbose: int = 1) -> bool:
    print("Image write {}".format(name)) if verbose == 1 else None
    return cv2.imwrite(os.path.join(folder, name), img)


def to_pillow_image(cv2_image: np.ndarray, is_gray_image: bool = False) -> Image:
    cv2_image = (
        cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        if is_gray_image is not True
        else cv2_image
    )
    pil_image = Image.fromarray(cv2_image)
    return pil_image
