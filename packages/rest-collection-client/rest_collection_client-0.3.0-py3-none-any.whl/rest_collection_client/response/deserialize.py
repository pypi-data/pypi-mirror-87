from typing import Callable, Sequence, Tuple

from extra_collections import Map

from rest_collection_client.typing import RawRestCollectionResponse, \
    SequenceOfMapping

__all__ = [
    'RestCollectionDeserializeMap',
]


class RestCollectionDeserializeMap(Map):
    """Deserializer map for rest collection response."""
    __slots__ = ()

    def __init__(
        self,
        **data: Callable[[SequenceOfMapping], SequenceOfMapping]
    ) -> None:
        super().__init__(data)

    def deserialize(self,
                    data: SequenceOfMapping,
                    key: str) -> SequenceOfMapping:
        return self.__getitem__(key)(data)

    def deserialize_response(
        self,
        data: RawRestCollectionResponse
    ) -> RawRestCollectionResponse:
        return {
            key: self.deserialize(data[key], key)
            for key in self
            if key in data
        }

    # Backward compatibility.
    deserialize_all = deserialize_response

    def deserialize_chunked_response(
        self,
        data: Sequence[RawRestCollectionResponse]
    ) -> Tuple[RawRestCollectionResponse, ...]:
        return tuple(map(self.deserialize_response, data))
