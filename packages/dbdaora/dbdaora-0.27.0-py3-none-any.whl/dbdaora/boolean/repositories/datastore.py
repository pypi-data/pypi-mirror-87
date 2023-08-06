from typing import Any

from google.cloud.datastore import Entity, Key
from jsondaora.serializers import OrjsonDefaultTypes

from . import BooleanRepository


OrjsonDefaultTypes.types_default_map[Entity] = lambda e: dict(**e)


class DatastoreBooleanRepository(BooleanRepository[Entity, Key]):
    __skip_cls_validation__ = ('DatastoreBooleanRepository',)
    fallback_data_source_key_cls = Key

    async def add_fallback(
        self, entity: Any, *entities: Any, **kwargs: Any
    ) -> None:
        await super().add_fallback(
            entity, *entities, exclude_from_indexes=('value',)
        )
