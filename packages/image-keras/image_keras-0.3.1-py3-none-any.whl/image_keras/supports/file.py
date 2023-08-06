import glob
import os
import re
import shutil
from typing import Callable, List, Optional, Tuple

from image_keras.supports.folder import files_in_folder
from image_keras.supports.functional.either import Either, Left, Right


def move_all_file(
    from_folder: str, target_folder: str, overwrite: bool = True
) -> Either[int, Exception]:
    """
    Move all files from `from_folder` to `target_folder`.


    Parameters
    ----------
    from_folder : str
        Original folder
    target_folder : str
        Target folder
    overwrite : bool
        If this is True, the files are overwritten if they exist. by default True.

    Returns
    -------
    Either[int, Exception]

        - Right(int) Success. Number of files moved.
        - Left(FileNotFoundError) Failure. If there is no `from_folder` or `target_folder`.
        - Left(Exception) Failure. Failed for another reason.

    Notes
    -----
    .. versionadded:: 0.1.0
    """
    try:
        cwd = os.getcwd()
        files: List[str] = files_in_folder(from_folder, include_hidden_file=True)
        for file in files:
            if overwrite:
                shutil.move(
                    os.path.join(cwd, from_folder, file),
                    os.path.join(cwd, target_folder, file),
                )
            else:
                shutil.move(os.path.join(from_folder, file), target_folder)
        return Right(len(files))
    except FileNotFoundError as err:
        return Left(err)
    except Exception as err:
        return Left(err)


def copy_all_file(from_folder: str, target_folder: str) -> Either[int, Exception]:
    """
    Copy all files from `from_folder` to `target_folder`.

    Parameters
    ----------
    from_folder : str
        Original folder
    target_folder : str
        Target folder

    Returns
    -------
    Either[int, Exception]

        - Right(int) Success. Number of files copied.
        - Left(Exception) Failure. Failed for another reason.

    Notes
    -----
    .. versionadded:: 0.1.0
    """
    try:
        files: List[str] = files_in_folder(from_folder, include_hidden_file=True)
        for file in files:
            shutil.copy2(os.path.join(from_folder, file), target_folder)
        return Right(len(files))
    except Exception as err:
        return Left(err)


def remove_all_files(target_folder: str) -> Either[int, Exception]:
    """
    In `target_folder`, remove all files.

    Parameters
    ----------
    target_folder : str
        Target folder

    Returns
    -------
    Either[int, Exception]

        - Right(int) Success. Number of files deleted.
        - Left(Exception) Failure. Failed for another reason.

    Notes
    -----
    .. versionadded:: 0.1.0
    """
    try:
        count = 0
        for file in files_in_folder(target_folder, True):
            os.remove(os.path.join(target_folder, file))
            count += 1
        return Right(count)
    except Exception as err:
        return Left(err)


def remove_files(
    starts_with_list: List[str], target_folder: str
) -> Either[int, Exception]:
    """
    In `target_folder`, Remove files starting with those defined in `starts_with_list`.

    Parameters
    ----------
    starts_with_list : List[str]
        List of starting words of files to be deleted
    target_folder : str
        Target folder

    Returns
    -------
    Either[int, Exception]

        - Right(int) Success. Number of files deleted.
        - Left(Exception) Failure. Failed for another reason.

    Notes
    -----
    .. versionadded:: 0.1.0
    """
    starts_with_list2: List[str] = starts_with_list.copy()
    try:
        count = 0
        for starts_with in starts_with_list2:
            for file in glob.glob("{}/{}*".format(target_folder, starts_with)):
                os.remove(file)
                count += 1
        return Right(count)
    except Exception as err:
        return Left(err)


def rename_file(
    original_filename: str, change_to: str, path: str
) -> Either[str, Exception]:
    """
    In `path` folder, change file name `original_filename` to `change_to`.

    Parameters
    ----------
    original_filename : str
        Original file name
    change_to : str
        File name to change
    path : str
        File path

    Returns
    -------
    Either[str, Exception]

        - Right(str) Success. Changed file path and name.
        - Left(FileNotFoundError) Failure. `original_filename` does not exist.
        - Left(Exception) Failure. Failed for another reason.

    Notes
    -----
    .. versionadded:: 0.1.0
    """
    try:
        os.rename(os.path.join(path, original_filename), os.path.join(path, change_to))
        return Right(os.path.join(path, change_to))
    except Exception as err:
        return Left(err)


def rename_files(
    original_filename__change_to_list: List[Tuple[str, str]], path: str
) -> Either[List[str], Exception]:
    """
    In `path` folder, change multiple file names.

    Even if an error occurs during the name change, the name change until the error occurs is applied.

    Parameters
    ----------
    original_filename__change_to_list : List[Tuple[str, str]]
        List of tuples, of original file name and file name to change
    path : str
        File path

    Returns
    -------
    Either[List[str], Exception]

        - Right(str) Success. Changed file path and name.
        - Left(FileNotFoundError) Failure. `original_filename` does not exist.
        - Left(Exception) Failure. Failed for another reason.

    Notes
    -----
    .. versionadded:: 0.1.0
    """
    results: List[Either[str, Exception]] = []
    for original_filename__change_to in original_filename__change_to_list:
        results.append(
            rename_file(
                original_filename=original_filename__change_to[0],
                change_to=original_filename__change_to[1],
                path=path,
            )
        )
    return sequences(results)


def rename_file_with_regex(
    from_regex: str,
    to_regex: Callable[[int], str],
    path: str,
    sort_f_optional: Optional[Callable[[List[str]], List[str]]] = None,
) -> Either[List[str], Exception]:
    """
    In `path` folder, change file names with regex.

    Even if an error occurs during the name change, the name change until the error occurs is applied.

    Parameters
    ----------
    from_regex : str
        Regex to select files to rename.
    to_regex : Callable[[int], str]
        Regex function `(counter: int) -> name`. Using this regex, file names will be changed.
    path : str
        File path
    sort_f_optional : Optional[Callable[[List[str]], List[str]]], optional
        Sort function if necessary, by default None

    Returns
    -------
    Either[List[str], Exception]
        Either List for rename results.

    Notes
    -----
    .. versionadded:: 0.1.0

    Examples
    -------
    >>> from_regex = "(.*)(.{3}).*\\.txt"
    >>> to_regex = (lambda counter: "\\g<1>_\\g<2>"+re.escape("_{:03d}".format(counter))+".txt")
    >>> path = self.base_folder
    >>> sort_f = (lambda l: sorted(l, reverse=True))
    >>> rename_file_with_regex(from_regex=from_regex, to_regex=to_regex, path=path, sort_f_optional=sort_f)
    ["tiger_01.txt", "tile_02.txt", "robot_03.txt"]
        -> ["tiger__01_001.txt", "tile__02_000.txt", "robot__03_002.txt"]
    """
    results: List[Either[str, Exception]] = []
    try:
        files: List[str] = files_in_folder(path)
        files_path: List[str] = glob.glob("{}/{}*".format(path, files))
        files_path = (
            sorted(files_path)
            if sort_f_optional is None
            else sort_f_optional(files_path)
        )

        for index, file_path in enumerate(files_path):
            new_name = re.sub(
                from_regex,
                to_regex(index),
                os.path.basename(file_path),
            )
            os.rename(file_path, os.path.join(path, new_name))
            results.append(Right(os.path.join(path, new_name)))
        return sequences(results)
    except Exception as err:
        return Left(err)
