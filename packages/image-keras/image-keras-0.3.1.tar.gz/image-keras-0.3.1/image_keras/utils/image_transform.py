from enum import Enum
from typing import Tuple

import cv2
import numpy as np


class InterpolationEnum(Enum):
    inter_nearest = "inter_nearest"  # a nearest-neighbor interpolation
    inter_linear = "inter_linear"  # a bilinear interpolation (used by default)
    inter_area = "inter_area"  # resampling using pixel area relation. It may be a preferred method for image decimation, as it gives moire’-free results. But when the image is zoomed, it is similar to the INTER_NEAREST method.
    inter_cubic = "inter_cubic"  # a bicubic interpolation over 4×4 pixel neighborhood
    inter_lanczos4 = (
        "inter_lanczos4"  # a Lanczos interpolation over 8×8 pixel neighborhood
    )

    def get_cv2_interpolation(self):
        if self == InterpolationEnum.inter_nearest:
            return cv2.INTER_NEAREST
        elif self == InterpolationEnum.inter_linear:
            return cv2.INTER_LINEAR
        elif self == InterpolationEnum.inter_area:
            return cv2.INTER_AREA
        elif self == InterpolationEnum.inter_cubic:
            return cv2.INTER_CUBIC
        elif self == InterpolationEnum.inter_lanczos4:
            return cv2.INTER_LANCZOS4


def img_resize(
    img: np.ndarray,
    target_size: Tuple[int, int],
    interpolation: InterpolationEnum = InterpolationEnum.inter_nearest,
):
    return cv2.resize(
        img, target_size, interpolation=interpolation.get_cv2_interpolation()
    )


def gray_image_apply_clahe(
    gray_cv2_img: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: Tuple[int, int] = (8, 8),
) -> np.ndarray:
    """
    clahe 필터를 적용합니다. 그레이스케일 이미지에서만 동작합니다.

    Parameters
    ----------
    gray_cv2_img : np.ndarray
        그레이스케일 이미지
    clip_limit : float, optional
        Clip limit, by default 2.0
    tile_grid_size : Tuple[int, int], optional
        타일 그리드 사이즈, by default (8, 8)

    Returns
    -------
    np.ndarray
        clahe 필터를 적용한 이미지
    """
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    result_img = clahe.apply(gray_cv2_img)
    return result_img


def img_to_ratio(img: np.ndarray) -> np.ndarray:
    """
    이미지를 비율로 전환합니다.

    Parameters
    ----------
    img : np.ndarray
        비율로 변환할 이미지

    Returns
    -------
    np.ndarray
        비율
    """
    return img / 255.0


def ratio_to_img(ratio_img: np.ndarray) -> np.ndarray:
    """
    비율을 이미지로 전환합니다.

    Parameters
    ----------
    img : np.ndarray
        이미지로 변환할 비율

    Returns
    -------
    np.ndarray
        이미지
    """
    return ratio_img * 255


def img_to_minmax(
    img: np.ndarray,
    threshold: float = 0.5,
    min_max: Tuple[float, float] = (0.0, 1.0),
) -> np.ndarray:
    """
    Threshold를 기준으로, 최소, 최대로 변경합니다.

    Parameters
    ----------
    img : np.ndarray
        이미지
    threshold : float, optional
        Threshold, by default 0.5
    min_max : Tuple[float, float], optional
        최소, 최대 값, by default (0.0, 1.0)

    Returns
    -------
    np.ndarray
        최소, 최대로 변환된 이미지
    """
    result_img = img.copy()
    result_img[result_img > threshold] = min_max[1]
    result_img[result_img <= threshold] = min_max[0]
    return result_img


def img_color_to_bw(cv2_color_img: np.ndarray) -> np.ndarray:
    gray_img = cv2.cvtColor(cv2_color_img, cv2.COLOR_BGR2GRAY)
    return cv2.threshold(gray_img, 1, 255, cv2.THRESH_BINARY)[1]


def draw__edge_only(cv2_image: np.ndarray, edge_size: int) -> np.ndarray:
    """
    Get the edges from the image. (by `edge_size` using Canny, 100, 50)

    .. image:: https://i.imgur.com/RKRgyFz.png
        :width: 2496px
        :height: 1018px
        :scale: 25%
        :alt: edge_detection
        :align: center

    Parameters
    ----------
    cv2_image : np.ndarray
        BGR color image
    edge_size : int
        Edge size

    Returns
    -------
    np.ndarray
        Grayscale image with white edge line.

    Examples
    --------
    >>> cv2_img: np.ndarray = cv2.imread("...")
    >>> draw__edge_only(cv2_img, 10)
    """
    image_canny: np.ndarray = cv2.Canny(cv2_image, 100, 50)
    all_one_kernel: np.ndarray = np.ones((edge_size, edge_size), np.uint8)
    return cv2.dilate(image_canny, all_one_kernel, 1)


def draw__mask_with_edge(cv2_image: np.ndarray, edge_size: int = 10) -> np.ndarray:
    """
    From a color image, get a black white image each instance separated by a border.

    1. Change a color image to black white image.
    2. Get edge image from `cv2_image`, then invert it to separate instance by a border.
    3. Merge 1 and 2.

    .. image:: https://i.imgur.com/YAHVVSl.png
        :width: 2496px
        :height: 1018px
        :scale: 25%
        :alt: mask_with_edge
        :align: center

    Parameters
    ----------
    cv2_image : np.ndarray
        BGR color Image
    edge_size : int
        Edge size, by default 10

    Returns
    -------
    np.ndarray
        Grayscale image each instance separated by a border.

    Examples
    --------
    >>> cv2_img: np.ndarray = cv2.imread("...")
    >>> edge_masked_image: np.ndarray = mask_with_edge(cv2_img, edge_size=10)
    """
    img_edge = draw__edge_only(cv2_image, edge_size)
    not_img_edge = cv2.bitwise_not(img_edge)
    bw_image = img_color_to_bw(cv2_image)
    return mask_image(bw_image, mask_image=not_img_edge)


def mask_image(original_image, mask_image):
    return cv2.bitwise_and(original_image, original_image, mask=mask_image)
