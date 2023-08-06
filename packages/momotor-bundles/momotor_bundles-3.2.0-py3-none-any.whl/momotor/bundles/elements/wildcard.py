import collections
import typing

try:
    from typing import final
except ImportError:
    from typing_extensions import final

__all__ = ['WildcardAttrsMixin']


CT = typing.TypeVar('CT', bound=object)


class WildcardAttrsMixin(typing.Generic[CT]):
    _attrs: typing.Dict[str, str] = None

    @final
    @property
    def attrs(self) -> typing.Dict[str, str]:
        """ Wildcard attributes """
        return self._attrs or {}

    @attrs.setter
    def attrs(self, attrs: typing.Mapping[str, str]):
        assert attrs is None or isinstance(attrs, collections.abc.Mapping)
        self._attrs = {**attrs} if attrs else {}

    def _create_attrs_from_node(self, node: CT):
        self._attrs = {**node.any_attributes}

    def _construct_attrs(self, node: CT) -> CT:
        node.any_attributes = {**self._attrs} if self._attrs else {}
        return node
