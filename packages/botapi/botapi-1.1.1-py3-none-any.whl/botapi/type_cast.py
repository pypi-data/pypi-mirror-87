from typing import Any

from .serialize import SerializableModel
from .types import TypedList


class TypeCast:
    @staticmethod
    def cast(
        name: str,
        value: Any,
        new_type: Any = None,
        item_type: Any = None
    ) -> Any:
        """
        Casts the value to the new_type. If new_type is TypedList, casts every
        item of value to item_type if item_type is not None

        :param name: name of the attribute (used to raise errors)
        :param value: value to cast
        :param new_type: desired type
        :param item_type: type of the TypedList item
        :return: casted value
        """
        if value is None:
            return None
        elif new_type is None or isinstance(value, new_type):
            return value
        elif issubclass(new_type, SerializableModel) and isinstance(value, dict):
            return new_type(**value)
        elif issubclass(new_type, TypedList):
            return TypeCast.typed_list_cast(
                name,
                value,
                item_type
            )
        else:
            raise TypeError(
                f"Can't cast {name} new value from {type(value)} to {new_type}"
            )

    @staticmethod
    def typed_list_cast(name, value, item_type=None) -> TypedList:
        """
        Returns TypedList with type casted items

        :param name: name of the attribute (used to raise errors)
        :param value: iterable to cast
        :param item_type: type of EVERY item
        :return: TypedList
        """
        if item_type is None:
            return TypedList(value, None)
        elif issubclass(item_type, SerializableModel):
            return TypedList(
                [
                    TypeCast.cast(
                        name,
                        item,
                        item_type
                    ) for item in value
                ],
                item_type
            )
        else:
            for item in value:
                if not isinstance(item, item_type):
                    raise TypeError(
                        f"Can't cast {name} new item value "
                        f"from {type(item)} to {item_type}"
                    )
            return TypedList(value, item_type)
