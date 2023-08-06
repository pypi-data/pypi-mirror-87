from .types import TypedList


class SerializableModel:
    """
    Inherit this class if you want to serialize/deserialize his objects
    """

    _unused_fields: dict

    def __init__(self, **kwargs):
        """
        Recursively deserializes an api object
        """
        self._unused_fields = kwargs.copy()
        aliases = getattr(self, '_aliases', {})
        for field in getattr(self, '_fields', set()):
            field_alias = aliases.get(field)
            if field_alias is not None:
                value = self._unused_fields.pop(field_alias, None)
                if value is None:
                    value = self._unused_fields.pop(field, None)
            else:
                value = self._unused_fields.pop(field, None)
            setattr(self, field, value)

    def serialize(self) -> dict:
        """
        Recursively serializes an api object

        :return: dict
        """
        serialized_obj = {}
        aliases = getattr(self, '_aliases', {})
        for field in getattr(self, '_fields', set()):
            value = getattr(self, field)
            if value is None:
                continue
            serialized_obj[aliases.get(field, field)] = self._serialize_value(value)
        return serialized_obj

    @staticmethod
    def _serialize_value(value):
        if type(value) == TypedList:
            return [i.serialize() if isinstance(i, SerializableModel) else i
                    for i in value]
        elif isinstance(value, SerializableModel):
            return value.serialize()
        else:
            return value
