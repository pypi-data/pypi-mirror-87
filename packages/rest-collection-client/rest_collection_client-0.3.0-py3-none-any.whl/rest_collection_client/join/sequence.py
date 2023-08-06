from typing import Tuple as TupleType

from extra_collections import Tuple
from pandas import DataFrame

from rest_collection_client.response import RestCollectionResponse
from .rule import RestCollectionJoinRule

__all__ = [
    'RestCollectionJoinSequence'
]


class RestCollectionJoinSequence(Tuple):
    """Container for join rules."""
    __slots__ = ()

    def __init__(self,
                 root_rule: RestCollectionJoinRule,
                 *other_rules: RestCollectionJoinRule) -> None:
        root_rule.set_root()
        super().__init__(root_rule, *other_rules)

    @property
    def _root_rule(self) -> RestCollectionJoinRule:
        return self._data[0]

    @property
    def _other_rules(self) -> TupleType[RestCollectionJoinRule, ...]:
        return self._data[1:]

    def join(self,
             response: RestCollectionResponse,
             how: str = 'left') -> DataFrame:
        # Join of root rule makes first joined result.
        joined = self._root_rule.join(response, how=how)

        for rule in self._other_rules:
            joined = rule.join(response, left_df=joined)

        return joined
