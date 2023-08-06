from typing import Mapping, Optional, TypeVar

import toolz

K = TypeVar("K")
V = TypeVar("V")


def get_from_map(
    m: Mapping[K, V], key: K, default_value_optional: Optional[V] = None
) -> Optional[V]:
    return toolz.get_in([key], m, default_value_optional)
