from typing import Any, Optional

from .type_cast import TypeCast
from .types import TypedList


class Field:
    """
    Basic field class. Inherit this class if you want to build your custom field
    """

    name: str = None
    fullname: str = None
    base: Any = None
    self_base: bool = None
    alias: str = None
    default: Any = None

    def __init__(
        self,
        base: Any = None,
        self_base: Optional[bool] = None,
        alias: Optional[str] = None,
        default: Any = None,
    ):
        """
        :param base: type of Field value. Type check use this param
        :param self_base: if True -> base = type of this model
        :param alias: alias name for field
        :param default: if value of the field is None and default not None returns
            default value
        """
        self.base = base
        self.self_base = self_base
        self.alias = alias
        self.default = default

    def __set_name__(self, owner, name):
        """
        Set name of attribute

        :param owner: the instance of the class
        :param name: attribute name
        :return: None
        """
        self.name = name
        self.fullname = f"{owner.__name__}.{name}"

    def __get__(self, instance, owner):
        """
        :param instance: instance that the attribute was accessed through,
            or None when the attribute is accessed through the owner
        :param owner: always the owner class
        :return: class (instance == None), field value or default (instance != None)
        """
        # Accessed on a class, not an instance
        if instance is None:
            return self

        value = instance.__dict__.get(self.name, None)
        if value is None and self.default is not None:
            return self.default
        else:
            return value

    def __set__(self, instance, value):
        """
        Set value to the attribute. If value is none -> delete attribute value

        :param instance: instance that the attribute was accessed through,
            or None when the attribute is accessed through the owner
        :param value: The value we want to assign to the attribute
        :return: None
        :raises TypeError: if the value is Field instance
        """
        if isinstance(value, Field):
            raise TypeError('Can\'t change field on the fly')
        elif value is not None:
            instance.__dict__[self.name] = TypeCast.cast(
                self.fullname,
                value,
                type(instance) if self.self_base is True else self.base
            )
        else:
            instance.__dict__.pop(self.name, None)


class ListField(Field):
    item_base: Any = None

    def __init__(
        self,
        item_base: Any = None,
        alias: Optional[str] = None,
        default: list = None
    ):
        super(ListField, self).__init__(base=list, alias=alias, default=default)
        self.item_base = item_base

    def __set__(self, instance, value):
        super().__set__(instance, TypeCast.cast(
            self.fullname,
            value,
            TypedList,
            self.item_base
        ))
