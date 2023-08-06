from functools import partial
from typing import Hashable

from extra_collections import Map

__all__ = [
    'RestCollectionRenameFactory',
]


class RestCollectionRenameFactory(Map):
    __slots__ = '_delimiter',

    def __init__(self, delimiter: str = '.') -> None:
        super().__init__({})
        self._delimiter = delimiter

    def _rename(self, label: str, suffix: str) -> str:
        return '{}{}{}'.format(label, self._delimiter, suffix)

    def __getitem__(self, key: Hashable) -> str:
        if key not in self._data:
            self._data[key] = partial(self._rename, key)
        return super().__getitem__(key)

    def __contains__(self, key: Hashable) -> bool:
        return key in self._data
