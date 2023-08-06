from typing import Optional

from pandas import DataFrame

from rest_collection_client.response import RestCollectionResponse
from .columns import RestCollectionJoinColumns

__all__ = [
    'RestCollectionJoinRule'
]


class RestCollectionJoinRule(object):
    """
    Container describes rule for performing SQL-like joining data of two join
    models.
    """
    __slots__ = '_root', '_right_columns', '_left_columns'

    def __init__(self,
                 left_join_columns: RestCollectionJoinColumns,
                 right_join_columns: RestCollectionJoinColumns) -> None:
        assert len(right_join_columns) == len(left_join_columns)

        self._root = False
        self._right_columns = right_join_columns
        self._left_columns = left_join_columns

    def set_root(self) -> None:
        self._root = True

    def join(self,
             response: RestCollectionResponse,
             left_df: Optional[DataFrame] = None,
             how: str = 'left') -> DataFrame:
        """Join data of two join models."""
        root = self._root

        assert root or isinstance(left_df, DataFrame), \
            'For non-root rule left_df must be defined.'

        left_columns = self._left_columns
        left_label = left_columns.label

        if root:
            # For root rule there must occurs KeyError if label is not defined
            # in response.
            left_df = left_df if left_df is not None else response[left_label]

        elif left_label not in response:
            # We did not find left model in response and it is not root rule,
            # so, we just omit merging. Probably, left model was outerjoined
            # during quering and had no results.
            return left_df

        right_columns = self._right_columns
        right_label = right_columns.label

        if right_label not in response:
            # Right DF is not in response. Probably, left model was outerjoined
            # during quering and had no results.
            return left_df

        right_df = response[right_label]

        return left_df.merge(
            right_df,
            left_on=list(left_columns),
            right_on=list(right_columns),
            how=how,
        )
