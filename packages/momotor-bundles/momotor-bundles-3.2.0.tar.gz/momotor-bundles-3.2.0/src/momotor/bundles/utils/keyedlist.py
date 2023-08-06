import typing
from collections import OrderedDict
from collections.abc import MutableSequence, MutableMapping

__all__ = ['KeyedList']


IT = typing.TypeVar('IT')


class KeyedList(typing.Generic[IT], MutableSequence, MutableMapping):
    """ A list of objects with an indexable attribute that acts as both a sequence and a mapping.
    Elements can be accessed by their numeric index or the key attribute.

    :param items: the initial items for the list. can be a sequence, mapping, another :py:class:`KeyedList`, or None
    :param key_attr: the attribute to index the items on. defaults to 'id'

    If `items` is another :py:class:`KeyedList`, `key_attr` must either be the same as the `key_attr` of `items`, or not provided.
    """
    __marker = object()

    def __init__(self, items: typing.Union["KeyedList[IT]", typing.Mapping[str, IT], typing.Sequence[IT]] = None, *,
                 key_attr: str = None):
        if key_attr is None:
            key_attr = items.__key_attr if isinstance(items, KeyedList) else 'id'

        self.__key_attr = key_attr
        self.__dict = OrderedDict()
        if items is not None:
            self.extend(items)

    def __get_key(self, key_or_index: typing.Union[str, int, IT]) -> str:
        if isinstance(key_or_index, slice):
            raise IndexError("slicing of a KeyedList is not supported")

        if hasattr(key_or_index, self.__key_attr):
            key = str(getattr(key_or_index, self.__key_attr))
            if key not in self.__dict or self.__dict[key] != key_or_index:
                raise KeyError

            return key

        if not isinstance(key_or_index, (str, int)):
            raise ValueError(f"access items by index (as int) or id (as str), not {type(key_or_index)}")

        if isinstance(key_or_index, int):
            return list(self.__dict.keys())[key_or_index]

        return key_or_index

    def __getitem__(self, key_or_index: typing.Union[str, int, IT]) -> IT:
        return self.__dict[self.__get_key(key_or_index)]

    def __setitem__(self, key_or_index: typing.Union[str, int, IT], value: IT) -> None:
        if isinstance(key_or_index, int):
            raise IndexError(f"items cannot be replaced")
        else:
            raise KeyError(f"items cannot be replaced")

    def __delitem__(self, key_or_index: typing.Union[str, int, IT]) -> None:
        del self.__dict[self.__get_key(key_or_index)]

    def extend(self, items: typing.Union["KeyedList[IT]", typing.Mapping[str, IT], typing.Sequence[IT]]):
        """ Extend sequence by appending elements

        :param items: the items to add to the sequence. Can be a :py:class:`KeyedList`, sequence or mapping

        If `items` is a :py:class:`KeyedList`, it must be compatible, ie. have the same `key_attr` value
        """
        key_attr = self.__key_attr
        if isinstance(items, KeyedList) and items.__key_attr != key_attr:
            raise ValueError(f"items.key_attr '{items.__key_attr}' is not '{key_attr}'")

        # Validate all items before adding
        def iter_keys():
            if isinstance(items, KeyedList):
                # a KeyedList validated all key-value pairs already
                yield from items.keys()

            elif hasattr(items, 'items'):
                # Mapping -- need to validate the keys with the items
                for k, v in items.items():
                    try:
                        iik = getattr(v, key_attr)
                    except AttributeError:
                        raise ValueError(f"item {v} does not have key attribute '{key_attr}'")

                    if iik != k:
                        raise KeyError(f"key '{k}' does not match the item {v} key '{iik}'")

                    yield k

            else:
                # Sequence -- generate keys from items
                for v in items:
                    try:
                        yield getattr(v, key_attr)
                    except AttributeError:
                        raise ValueError(f"item {v} does not have key attribute '{key_attr}'")

        for key in iter_keys():
            if key in self.__dict:
                raise ValueError(f"item with key '{key}' already exists")

        if hasattr(items, 'keys'):
            # Mapping or KeyedList
            self.__dict.update(items)
        else:
            # Sequence
            self.__dict.update((getattr(item, key_attr), item) for item in items)

    def insert(self, key_or_index: typing.Union[str, int, IT], value: IT) -> None:
        """ insertion is not supported """
        if isinstance(key_or_index, int):
            raise IndexError(f"insertion is not supported")
        else:
            raise KeyError(f"items cannot be inserted")

    def append(self, item: IT) -> None:
        """ append `item` to the end of the sequence.

        :param item: the items to add to the sequence, must have a key attribute which does not yet exist in this list
        """
        self.extend([item])

    def get(self, key_or_index: typing.Union[str, int, IT], default=None):
        """ Get an item from the sequence by index, key or item

        :param key_or_index: index, key or item
        :param default: the value to return if item does not exist
        :return: the item or `default`
        """
        return self.__dict.get(self.__get_key(key_or_index), default)

    # noinspection PyMethodOverriding
    @typing.overload
    def pop(self, key_or_index: typing.Union[str, int, IT]) -> IT:
        ...

    # noinspection PyMethodOverriding
    def pop(self, key_or_index: typing.Union[str, int, IT], default=__marker) -> IT:
        """ Pop an item from the sequence by index, key or item

        :param key_or_index: index, key or item
        :param default: the value to return if item does not exist
        :return: the item or `default`. If `default` is not provided and item does not exist, raises KeyError
        """
        if default == self.__marker:
            return self.__dict.pop(self.__get_key(key_or_index))
        else:
            return self.__dict.pop(self.__get_key(key_or_index), default)

    def keys(self) -> typing.KeysView[str]:
        """ A set-like object providing a view on the keys """
        return self.__dict.keys()

    def values(self) -> typing.ValuesView[IT]:
        """ A set-like object providing a view on the values """
        return self.__dict.values()

    def items(self) -> typing.ItemsView[str, IT]:
        """ A set-like object providing a view on the items """
        return self.__dict.items()

    def popitem(self, last=True) -> typing.Tuple[str, IT]:
        """ Remove and return a (key, value) pair from the dictionary.

        Pairs are returned in LIFO order if last is true or FIFO order if false.
        """
        return self.__dict.popitem(last)

    def __iter__(self):
        for item in self.values():
            yield item

    def copy(self) -> "KeyedList[IT]":
        """ Create a shallow copy """
        return KeyedList(self)

    __copy__ = copy

    def clear(self) -> None:
        """ Remove all items """
        self.__dict.clear()

    def __contains__(self, key_or_index: typing.Union[str, int, IT]) -> bool:
        if isinstance(key_or_index, int):
            return 0 <= key_or_index < len(self.__dict)

        try:
            key = getattr(key_or_index, self.__key_attr)
        except AttributeError:
            return key_or_index in self.__dict
        else:
            return self.__dict.get(key) == key_or_index

    def __len__(self) -> int:
        return len(self.__dict)

    def __eq__(self, other) -> bool:
        if isinstance(other, KeyedList):
            return other.__key_attr == self.__key_attr and other.__dict == self.__dict
        elif isinstance(other, list):
            return other == list(self)
        else:
            return other == self.__dict

    def count(self, item: IT) -> int:
        try:
            key = getattr(item, self.__key_attr)
        except AttributeError:
            return 0
        else:
            return 1 if self.__dict.get(key) == item else 0

    def remove(self, item: IT):
        try:
            key = getattr(item, self.__key_attr)
        except AttributeError:
            raise ValueError("incompatible item")

        if self.__dict.get(key) != item:
            raise ValueError("item does not exist")

        del self.__dict[key]
