import os
from typing import List, Tuple


def split_fullpath(full_path: str) -> Tuple[str, str, str]:
    """
    Split path to tuple.

    Parameters
    ----------
    full_path : str
        Full path to be decomposed.

    Returns
    -------
    Tuple[str, str, str]
        (full path, base filename, file extension) tuple.

    Examples
    --------
    >>> split_fullpath("/abc/test_resources/sample.png")
    ('/abc/test_resources', 'sample', '.png')

    >>> split_fullpath("/abc/test_resources")
    ('/abc/test_resources', None, None)
    """
    if os.path.isfile(full_path):
        _s = os.path.splitext(full_path)
        base_filename = os.path.basename(_s[0])
        base_ext = _s[1]
        pathname = os.path.dirname(_s[0])
        return pathname, base_filename, base_ext
    else:
        return full_path, None, None


def get_image_filenames(in_path: str) -> List[str]:
    """
    Get image filenames("jpg", "jpeg", "bmp", "png", "gif") in `in_path` folder.

    Parameters
    ----------
    in_path : str
        Folder name to get image filenames from.

    Returns
    -------
    List[str]
        Image filename list

    Examples
    --------
    >>> get_image_filenames("tests/test_resources)
    ['lenna.png', 'sample.png', 'bone.png', 'a.png']
    """
    included_extensions = ["jpg", "jpeg", "bmp", "png", "gif"]
    return [
        fn
        for fn in os.listdir(in_path)
        if any(fn.endswith(ext) for ext in included_extensions)
    ]
