from typing import Callable, List, Optional, Tuple

import numpy as np
from image_keras.supports.tuple_op import (
    tuple_add,
    tuple_divide_int,
    tuple_element_wise_add,
    tuple_element_wise_divide_int,
    tuple_element_wise_subtract,
    tuple_multiply,
)


def add_zero_padding(
    cv2_image: np.ndarray, padding_height_width: Tuple[int, int]
) -> Optional[np.ndarray]:
    """
    Add zero padding for open cv image. (grayscale image (w, h) or rgb image (w, h, c).)

    Parameters
    ----------
    cv2_image : np.ndarray
        Open cv image to add zero padding.
    padding_height_width : Tuple[int, int]
        Zero padding width and height.

    Returns
    -------
    Optional[np.ndarray]
        Zero padded image. If not image, it will return None.
    """
    if len(cv2_image.shape) == 3:
        return np.pad(
            cv2_image,
            (
                (padding_height_width[0], padding_height_width[0]),
                (padding_height_width[1], padding_height_width[1]),
                (0, 0),
            ),
            "constant",
            constant_values=0,
        )
    elif len(cv2_image.shape) == 2:
        return np.pad(
            cv2_image,
            (
                (padding_height_width[0], padding_height_width[0]),
                (padding_height_width[1], padding_height_width[1]),
            ),
            "constant",
            constant_values=0,
        )
    else:
        return None


def num_total_index_for_slice(
    img_height_width: Tuple[int, int],
    tile_height_width: Tuple[int, int],
    padding_height_width: Tuple[int, int],
    stride_height_width: Tuple[int, int],
    add_same_padding: bool = False,
    discard_horizontal_overflow: bool = True,
    discard_vertical_overflow: bool = True,
) -> Tuple[int, int]:
    base_wh = tuple_element_wise_subtract(img_height_width, tile_height_width)
    if add_same_padding:
        base_wh = tuple_element_wise_add(
            base_wh, tuple_multiply(padding_height_width, 2)
        )
    num_height_width_index = tuple_element_wise_divide_int(
        base_wh,
        stride_height_width,
    )
    num_height_width_index = tuple_add(num_height_width_index, 1)
    if not discard_vertical_overflow:
        num_height_width_index[0] = num_height_width_index[0] + 1
    if not discard_horizontal_overflow:
        num_height_width_index[1] = num_height_width_index[1] + 1
    return num_height_width_index


def slice_by_pixel_size(
    cv2_image: np.ndarray,
    tile_height_width: Tuple[int, int],
    inbox_height_width: Tuple[int, int],
    stride_height_width: Tuple[int, int],
    add_same_padding: bool = False,
    discard_horizontal_overflow: bool = True,
    discard_vertical_overflow: bool = True,
) -> List[List[np.ndarray]]:
    """
    Slice image.

    Parameters
    ----------
    cv2_image : np.ndarray
        [description]
    tile_height_width : Tuple[int, int]
        [description]
    inbox_height_width : Tuple[int, int]
        [description]
    stride_height_width : Tuple[int, int]
        [description]
    discard_horizontal_overflow : bool, optional
        [description], by default True
    discard_vertical_overflow : bool, optional
        [description], by default True

    Returns
    -------
    List[List[np.ndarray]]
        [description]

    Examples
    --------
    >>> image: np.ndarray = cv2.imread('/path/to/image_file.png')
    >>> slice_by_pixel_size(image, tile_height_width=(128, 128), inbox_height_width=(60, 60), stride_height_width=(60, 60))
    """
    padding_height_width = tuple_divide_int(
        tuple_element_wise_subtract(
            tile_height_width,
            inbox_height_width,
        ),
        2,
    )

    num_height_width_index = num_total_index_for_slice(
        cv2_image.shape[:2],
        tile_height_width,
        padding_height_width,
        stride_height_width,
        add_same_padding,
        discard_horizontal_overflow,
        discard_vertical_overflow,
    )

    if add_same_padding:
        padding_cv2_image = add_zero_padding(cv2_image, padding_height_width)
    else:
        padding_cv2_image = cv2_image

    result_block_box: List[List[np.ndarray]] = []
    for ri in range(num_height_width_index[0]):
        result_row: List[np.ndarray] = []
        from_height = stride_height_width[0] * ri
        to_height = stride_height_width[0] * ri + tile_height_width[0]

        for ci in range(num_height_width_index[1]):
            from_width = stride_height_width[1] * ci
            to_width = stride_height_width[1] * ci + tile_height_width[1]

            result_row.append(
                padding_cv2_image[from_height:to_height, from_width:to_width]
            )
        result_block_box.append(result_row)
    return result_block_box


def apply_each_slice(
    sliced_cv2_images: List[List[np.ndarray]],
    func: Callable[[int, int, np.ndarray], Optional[np.ndarray]],
) -> Tuple[int, int, List[List[np.ndarray]]]:
    i = 0
    j = 0
    result_block_box: List[List[np.ndarray]] = []
    for sliced_images_row in sliced_cv2_images:
        j = 0
        result_row: List[np.ndarray] = []
        for sliced_images_col in sliced_images_row:
            optional_r = func(i, j, sliced_images_col)
            if optional_r:
                result_row.append(optional_r)
            j = j + 1
        result_block_box.append(result_row)
        i = i + 1

    return i, j, result_block_box
