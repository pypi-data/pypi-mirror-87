from typing import Any, Iterable


class TypedList(list):
    """
    Default list + type checking
    """

    item_type: Any

    def __init__(self, seq=(), item_type=None):
        self.item_type = item_type
        self._check_iterable_item_type(seq)
        super().__init__(seq)

    def append(self, item: Any) -> None:
        self._check_item_type(item)
        return super(TypedList, self).append(item)

    def extend(self, iterable: Iterable) -> None:
        self._check_iterable_item_type(iterable)
        return super(TypedList, self).extend(iterable)

    def insert(self, index: int, item: Any) -> None:
        self._check_item_type(item)
        return super(TypedList, self).insert(index, item)

    def __iadd__(self, iterable: Iterable):
        self._check_iterable_item_type(iterable)
        return super(TypedList, self).__iadd__(iterable)

    def __setitem__(self, index, item):
        self._check_item_type(item)
        return super(TypedList, self).__setitem__(index, item)

    def _check_item_type(self, item):
        if self.item_type is not None and not isinstance(item, self.item_type):
            raise TypeError(
                f'TypedList item must be a {self.item_type}, not {type(item)}'
            )

    def _check_iterable_item_type(self, iterable: Iterable):
        if self.item_type is not None:
            for new_item in iterable:
                self._check_item_type(new_item)
