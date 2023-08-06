from typing import Dict, List, Mapping, Sequence, Union

__all__ = [
    'JsonContentOrText',
    'SequenceOfMapping',
    'RawRestCollectionResponse',
]

JsonContentOrText = Union[Dict, List, str, int, float, None]
SequenceOfMapping = Sequence[Mapping]
RawRestCollectionResponse = Mapping[str, SequenceOfMapping]
