from extra_collections import Tuple

__all__ = [
    'RestCollectionJoinColumns',
]


class RestCollectionJoinColumns(Tuple):
    """Container for describing join columns in join rules."""
    __slots__ = '_label', '_prefix', '_delimiter'

    def __init__(self,
                 label: str,
                 *columns: str,
                 prefix: bool = True,
                 delimiter: str = '.') -> None:
        super().__init__(*columns)
        self._label = label
        self._prefix = prefix
        self._delimiter = delimiter

    @property
    def label(self) -> str:
        return self._label

    @property
    def columns(self) -> tuple:
        return self._data

    def __getitem__(self, index: int) -> str:
        column = super().__getitem__(index)

        if not self._prefix:
            return column

        return '{}{}{}'.format(self._label, self._delimiter, column)

    @classmethod
    def just_id_column(cls,
                       name: str,
                       prefix: bool = True,
                       delimiter: str = '.') -> 'RestCollectionJoinColumns':
        return cls(name, 'id', prefix=prefix, delimiter=delimiter)
