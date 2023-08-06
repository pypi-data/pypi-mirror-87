import typing
from pathlib import PurePosixPath

import momotor.bundles
from momotor.bundles.binding import PropertyComplexType, PropertiesComplexType
from momotor.bundles.elements.base import Element
from momotor.bundles.elements.content import ContentTypeElement
from momotor.bundles.elements.wildcard import WildcardAttrsMixin
from momotor.bundles.typing.element import ElementMixinProtocol
from momotor.bundles.utils.grouping import group_by_attr
from momotor.bundles.utils.nodes import get_nested_complex_nodes

try:
    from typing import final
except ImportError:
    from typing_extensions import final

__all__ = ['Property', 'PropertiesMixin']


class Property(
    ContentTypeElement[PropertyComplexType, PropertiesComplexType],
    WildcardAttrsMixin[PropertyComplexType],
):
    """ A Property element encapsulating :py:class:`~momotor.bundles.binding.momotor.PropertyComplexType`
    """
    _accept: typing.Optional[str] = None

    @final
    @property
    def accept(self) -> typing.Optional[str]:
        return self._accept

    @accept.setter
    def accept(self, accept: typing.Optional[str]):
        assert accept is None or isinstance(accept, str)
        self._accept = accept

    @staticmethod
    def get_node_type() -> typing.Type[PropertyComplexType]:
        return PropertyComplexType

    @staticmethod
    def _get_parent_type() -> typing.Type[PropertiesComplexType]:
        return PropertiesComplexType

    # noinspection PyShadowingBuiltins
    def create(self, *,
               name: str,
               value: typing.Any = None,
               type: str = None,
               accept: str = None,
               attrs: typing.Dict[str, str] = None,
               ) -> "Property":

        self._create_content(name=name, value=value, type=type)

        self.accept = accept
        self.attrs = attrs

        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) -> "Property":
        assert target_basesrc is None or isinstance(target_basesrc, PurePosixPath)

        return Property(target_bundle).create(
            name=self.name,
            value=self.value,
            accept=self.accept,
            attrs=self._attrs,
        )

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: PropertyComplexType,
                          parent: PropertiesComplexType,
                          ref_parent: typing.Optional[PropertiesComplexType]) -> "Property":
        self._check_node_type(node)
        self._check_parent_type(parent)
        self._check_parent_type(ref_parent, True)

        super()._create_content_from_node(node, parent, ref_parent)
        super()._create_attrs_from_node(node)

        self.accept = node.accept

        return self

    def _construct_node(self) -> PropertyComplexType:
        # noinspection PyArgumentList
        return (
            self._construct_attrs(
                self._construct_content(
                    self.get_node_type()(
                        accept=self.accept,
                    )
                )
            )
        )


Property.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])


# noinspection PyProtectedMember
class PropertiesMixin:
    _properties: typing.Optional[typing.List[Property]] = None
    _properties_by_name: typing.Optional[typing.Dict[str, typing.Tuple[Property]]] = None

    @final
    @property
    def properties(self) -> typing.Optional[typing.List[Property]]:
        """ `properties` children """
        return None if self._properties is None else [*self._properties]

    @properties.setter
    def properties(self: ElementMixinProtocol, properties: typing.Iterable[Property]):
        assert properties is None or all(prop.bundle == self.bundle for prop in properties)
        self._properties = None if properties is None else [*properties]
        self._properties_by_name = None

    def _collect_properties(self: ElementMixinProtocol, parent: object) -> typing.List[Property]:
        properties: typing.List[Property] = []
        properties_node: typing.Optional[PropertiesComplexType] = None
        for tag_name, node in get_nested_complex_nodes(parent, 'properties', 'property'):
            if tag_name == 'properties':
                properties_node = typing.cast(PropertiesComplexType, node)
            else:
                property_node = typing.cast(PropertyComplexType, node)
                properties.append(
                    Property(self.bundle)._create_from_node(property_node, properties_node, None)
                )

        return properties

    # noinspection PyMethodMayBeStatic
    def _construct_properties_nodes(self, properties: typing.Optional[typing.List[Property]]) \
            -> typing.List[PropertiesComplexType]:
        if properties:
            return [
                PropertiesComplexType(property=[
                    prop._construct_node()
                    for prop in properties
                ])
            ]

        return []

    def get_properties(self, name: str) -> typing.Tuple[Property]:
        """ Get properties

        :param name: `name` of the properties to get
        :return: A list of all matching properties.
        """
        if self._properties_by_name is None:
            self._properties_by_name = group_by_attr(self._properties, 'name')

        return self._properties_by_name[name]

    def get_property_value(self, name: str) -> typing.Any:
        """ Get the value for a single property.
        If multiple properties match, the value of the first one found will be returned

        :param name: `name` of the property to get
        :return: The property value
        """
        try:
            return self.get_properties(name)[0].value
        except KeyError:
            return None
