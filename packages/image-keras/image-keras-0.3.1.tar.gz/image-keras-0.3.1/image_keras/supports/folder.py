import glob
import os
import re
import shutil
from typing import Callable, List, Optional, Tuple

import toolz


def files_in_folder(
    folder_name: str, file_name_filter_optional: Optional[Callable[[str], bool]] = None
) -> List[str]:
    """
    Get files in folder without hidden file (starts with '.').

    Filtering using `file_name_filter_optional`.

    Args:
        folder_name (str): folder name
        file_name_filter_optional (Optional[Callable[[str], bool]]): optional filter

    Returns:
        File name lists
    """
    ff = (
        (lambda file_name: file_name == file_name)
        if file_name_filter_optional is None
        else (file_name_filter_optional)
    )
    return toolz.pipe(
        folder_name,
        os.listdir,
        toolz.curried.filter(lambda f: os.path.isfile(folder_name + "/" + f)),
        toolz.curried.filter(lambda file: not file.startswith(".")),
        toolz.curried.filter(ff),
        list,
        sorted,
    )


def create_folder_if_not_exist(folder_path: str) -> None:
    os.makedirs(folder_path) if not os.path.exists(folder_path) else None


def get_files_only_in_folder(folder_path: str) -> List[str]:
    files = files_in_folder(folder_path)
    files = list(
        filter(lambda el: os.path.isfile(os.path.join(folder_path, el)), files)
    )
    return files


def move_all_file_to_folder(from_folder: str, _target_folder: str) -> None:
    for file in get_files_only_in_folder(from_folder):
        shutil.move(os.path.join(from_folder, file), _target_folder)


def move_overwrite_all_file_to_folder(from_folder: str, _target_folder: str) -> None:
    cwd = os.getcwd()
    for file in get_files_only_in_folder(from_folder):
        shutil.move(
            os.path.join(cwd, from_folder, file),
            os.path.join(cwd, _target_folder, file),
        )


def copy_all_file_to_folder(from_folder: str, _target_folder: str) -> None:
    for file in get_files_only_in_folder(from_folder):
        shutil.copy2(os.path.join(from_folder, file), _target_folder)


def remove_files(starts_with_list: List[str], target_path: str) -> None:
    for _file_starts_with in starts_with_list:
        for _file in glob.glob("{}/{}*".format(target_path, _file_starts_with)):
            os.remove(_file)


def rename_files(
    sorted_list1: List[str], sorted_list2: List[str], target_path: str
) -> None:
    rename_files_from_list: List[Tuple[int, Tuple[str, str]]] = []
    _rev_current_file_names = sorted_list1
    for index, current_file_name in enumerate(sorted_list2):
        rename_files_from_list.append(
            (index, (current_file_name, _rev_current_file_names[index]))
        )
    for rename_files_for_prev_from_to in sorted(rename_files_from_list):
        for old_name in glob.glob(
            "{}/{}*".format(target_path, rename_files_for_prev_from_to[1][0])
        ):
            new_name = re.sub(
                r"(.*)(.{6}).*\.png",
                rename_files_for_prev_from_to[1][1] + r"\2.png",
                os.path.basename(old_name),
            )
            os.rename(old_name, os.path.join(target_path, new_name))
