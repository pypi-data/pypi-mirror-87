import copy
import typing
from pathlib import PurePosixPath

import momotor.bundles
from momotor.bundles.binding import ResourceComplexType, ResourcesComplexType
from momotor.bundles.elements.base import Element
from momotor.bundles.elements.content import ContentElement
from momotor.bundles.typing.element import ElementMixinProtocol
from momotor.bundles.utils.grouping import group_by_attr
from momotor.bundles.utils.nodes import get_nested_complex_nodes

try:
    from typing import final
except ImportError:
    from typing_extensions import final

__all__ = ['Resource', 'ResourcesMixin']


class Resource(ContentElement[ResourceComplexType, ResourcesComplexType]):
    # noinspection PyUnresolvedReferences
    """ A Resource element encapsulating :py:class:`~momotor.bundles.binding.momotor.ResourceComplexType`
    """
    @staticmethod
    def get_node_type() -> typing.Type[ResourceComplexType]:
        return ResourceComplexType

    @staticmethod
    def _get_parent_type() -> typing.Type[ResourcesComplexType]:
        return ResourcesComplexType

    def create(self, *, name: str, value: str = None) -> "Resource":
        self._create_content(name=name, value=value)
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) \
            -> "Resource":
        assert target_basesrc is None or isinstance(target_basesrc, PurePosixPath)

        return Resource(target_bundle).create(
            name=self.name,
            value=self.value
        )

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: ResourceComplexType,
                          direct_parent: ResourcesComplexType,
                          ref_parent: typing.Optional[ResourcesComplexType]) -> "Resource":
        self._check_node_type(node)
        self._check_parent_type(direct_parent)
        self._check_parent_type(ref_parent, True)

        self._create_content_from_node(node, direct_parent, ref_parent)

        return self

    def _construct_node(self) -> ResourceComplexType:
        return (
            self._construct_content(
                self.get_node_type()()
            )
        )


Resource.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])


# noinspection PyProtectedMember
class ResourcesMixin:
    _resources: typing.Optional[typing.List[Resource]] = None
    _resources_by_name: typing.Optional[typing.Dict[str, typing.Tuple[Resource]]] = None

    @final
    @property
    def resources(self) -> typing.Optional[typing.List[Resource]]:
        """ `resources` attribute """
        return None if self._resources is None else [*self._resources]

    @resources.setter
    def resources(self: ElementMixinProtocol, resources: typing.Optional[typing.Sequence[Resource]]):
        assert resources is None or all(resource.bundle == self.bundle for resource in resources)
        self._resources = None if resources is None else [*resources]
        self._resources_updated()

    def _resources_updated(self):
        self._resources_by_name = None

    def _collect_resources(self: ElementMixinProtocol, parent: object) -> typing.List[Resource]:
        resources: typing.List[Resource] = []
        resources_node: typing.Optional[ResourcesComplexType] = None
        for tag_name, node in get_nested_complex_nodes(parent, 'resources', 'resource'):
            if tag_name == 'resources':
                resources_node = typing.cast(ResourcesComplexType, node)
            else:
                resource_node = typing.cast(ResourceComplexType, node)
                resources.append(
                    Resource(self.bundle)._create_from_node(resource_node, resources_node, None)
                )

        return resources

    # noinspection PyMethodMayBeStatic
    def _construct_resources_nodes(self, resources: typing.Optional[typing.List[Resource]]) \
            -> typing.List[ResourcesComplexType]:
        if resources:
            return [
                ResourcesComplexType(resource=[
                    resource._construct_node()
                    for resource in resources
                ])
            ]

        return []

    def _get_resources(self) -> typing.Dict[str, typing.Tuple[Resource]]:
        if self._resources_by_name is None:
            self._resources_by_name = group_by_attr(self.resources, 'name')

        return self._resources_by_name

    def get_resources(self) -> typing.Dict[str, typing.Tuple[Resource]]:
        """ Get the resources as a dictionary name -> Resource """
        return copy.copy(self._get_resources())
