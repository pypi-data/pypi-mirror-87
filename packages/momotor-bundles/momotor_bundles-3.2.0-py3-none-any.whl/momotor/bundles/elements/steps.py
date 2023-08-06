import collections.abc
import copy
import typing
import warnings
from enum import IntEnum
from pathlib import PurePosixPath

import momotor.bundles
from momotor.bundles.binding import DependsComplexType, StepComplexType, DependenciesComplexType, \
    StepsComplexType, RecipeComplexType, StepComplexTypePriority
from momotor.bundles.elements.base import Element, NestedElement, IdMixin
from momotor.bundles.elements.checklets import Checklet, CheckletMixin
from momotor.bundles.elements.files import File, FilesMixin
from momotor.bundles.elements.options import Option, OptionsMixin
from momotor.bundles.elements.resources import ResourcesMixin, Resource
from momotor.bundles.utils.nodes import get_nested_complex_nodes

try:
    from typing import final
except ImportError:
    from typing_extensions import final

__all__ = ['Priority', 'Depends', 'Step']


class Priority(IntEnum):
    """ An enum for the step priority """
    MUST_PASS = 0
    HIGH = 1
    NORMAL = 2
    DEFAULT = 2
    LOW = 3


# Map StepComplexTypePriority to Priority
PRIORITY_LEVEL_MAP: typing.Dict[StepComplexTypePriority, Priority] = {
    StepComplexTypePriority.MUST_PASS: Priority.MUST_PASS,
    StepComplexTypePriority.HIGH: Priority.HIGH,
    StepComplexTypePriority.DEFAULT: Priority.DEFAULT,
    StepComplexTypePriority.NORMAL: Priority.NORMAL,
    StepComplexTypePriority.LOW: Priority.LOW,
}


class Depends(Element[DependsComplexType], OptionsMixin):
    # noinspection PyUnresolvedReferences
    """ A Depends element encapsulating :py:class:`~momotor.bundles.binding.momotor.DependsComplexType`
    """

    _step: typing.Optional[str] = None

    @final
    @property
    def step(self) -> str:
        """ `step` attribute """
        assert self._step is not None
        return self._step

    @step.setter
    def step(self, step: str):
        assert isinstance(step, str)
        self._step = step

    @staticmethod
    def get_node_type() -> typing.Type[DependsComplexType]:
        return DependsComplexType

    def create(self, *,
               step: str,
               options: typing.List[Option] = None
               ) -> "Depends":

        self.step = step
        self.options = options
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) -> "Depends":
        assert target_basesrc is None or isinstance(target_basesrc, PurePosixPath)

        return Depends(target_bundle).create(
            step=self.step,
            options=self.options,
        )

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: DependsComplexType) -> "Depends":
        self._check_node_type(node, DependsComplexType)

        return self.create(
            step=node.step,
            options=self._collect_options(node, []),
        )

    def _construct_node(self) -> DependsComplexType:
        return DependsComplexType(
            step=self.step,
            options=self._construct_options_nodes(self.options),
        )


Depends.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])


class Step(
    NestedElement[StepComplexType, StepsComplexType],
    CheckletMixin[StepComplexType],
    IdMixin, OptionsMixin, FilesMixin, ResourcesMixin,
):
    """ A Step element encapsulating :py:class:`~momotor.bundles.binding.momotor.StepComplexType`
    """
    _priority: typing.Optional[StepComplexTypePriority] = None
    _depends: typing.Optional[typing.List[Depends]] = None
    _checklet: typing.Optional[Checklet] = None
    _merged_resources = None

    @final
    @property
    def priority(self) -> str:
        """ `priority` attribute """
        if self.priority is None:
            raise ValueError("Step not initialized: priority not yet set")

        return self._priority.value

    @priority.setter
    def priority(self, priority: str):
        assert isinstance(priority, str)

        try:
            priority_enum = StepComplexTypePriority(priority)
        except ValueError:
            warnings.warn(f"Invalid priority attribute value '{priority}' ignored (will use 'default")
            priority_enum = StepComplexTypePriority.DEFAULT

        self._priority = priority_enum

    @final
    @property
    def depends(self) -> typing.Optional[typing.List[Depends]]:
        """ `depends` """
        return self._depends

    @depends.setter
    def depends(self, depends: typing.List[Depends]):
        assert depends is None or (
            isinstance(depends, collections.abc.Sequence) and all(depend.bundle == self.bundle for depend in depends)
        )
        self._depends = [*depends] if depends is not None else None

    @final
    @property
    def checklet(self) -> typing.Optional[Checklet]:
        """ `checklet` """
        return self._checklet

    @checklet.setter
    def checklet(self, checklet: Checklet):
        assert checklet is None or (isinstance(checklet, Checklet) and checklet.bundle == self.bundle)
        self._checklet = checklet
        self._merged_resources = None

    def _resources_updated(self):
        super()._resources_updated()
        self._merged_resources = None

    @staticmethod
    def get_node_type() -> typing.Type[StepComplexType]:
        return StepComplexType

    @staticmethod
    def _get_parent_type() -> typing.Type[StepsComplexType]:
        return StepsComplexType

    # noinspection PyShadowingBuiltins
    def create(self, *,
               id: str,
               priority: str = 'default',
               depends: typing.List[Depends] = None,
               checklet: Checklet = None,
               options: typing.List[Option] = None,
               files: typing.List[File] = None,
               resources: typing.List[Resource] = None,
               ) -> "Step":

        self.id = id
        self.priority = priority
        self.depends = depends
        self.checklet = checklet
        self.options = options
        self.files = files
        self.resources = resources
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) \
            -> typing.NoReturn:
        """ not implemented """
        raise NotImplementedError

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: StepComplexType, steps: StepsComplexType, recipe: RecipeComplexType) -> "Step":
        # recipe > steps > step
        #
        # step has <files> children
        #  - file.ref can refer to file in recipe.files
        #
        # step has single <checklet> child
        #  - checklet.ref can refer to checklet in steps.checklets or recipe.checklets

        self._check_node_type(node)
        self._check_parent_type(steps)
        # self._check_node_type(recipe, RecipeComplexType)

        return self.create(
            id=node.id,
            priority=node.priority.value,
            depends=self._collect_depends(node),
            checklet=self._collect_checklet(node, [steps.checklets, recipe.checklets]),
            options=self._collect_options(node, [steps.options, recipe.options]),
            files=self._collect_files(node, [recipe.files]),
            resources=self._collect_resources(node)
        )

    def _collect_depends(self, node: StepComplexType) -> typing.List[Depends]:
        depends: typing.List[Depends] = []
        for tag_name, child in get_nested_complex_nodes(node, 'dependencies', 'depends'):
            if tag_name == 'depends':
                depends_node = typing.cast(DependsComplexType, child)
                # noinspection PyProtectedMember
                depends.append(Depends(self.bundle)._create_from_node(node=depends_node))

        return depends

    def _construct_node(self) -> StepComplexType:
        # noinspection PyProtectedMember,PyArgumentList
        return self.get_node_type()(
            id=self.id,
            priority=self._priority,
            dependencies=[DependenciesComplexType(
                depends=[dep._construct_node() for dep in self.depends]
            )],
            checklet=[self.checklet._construct_node()] if self.checklet else [],
            options=self._construct_options_nodes(self.options),
            files=self._construct_files_nodes(self.files),
            resources=self._construct_resources_nodes(self.resources),
        )

    @property
    def priority_value(self) -> Priority:
        """ `priority` attribute as :py:class:`Priority` instance """
        return PRIORITY_LEVEL_MAP.get(self._priority)

    def get_dependencies_ids(self) -> typing.List[str]:
        """ ids of the dependencies """
        return [
            depends.step for depends in self.depends
        ]

    def get_resources(self) -> typing.Dict[str, typing.Tuple[Resource]]:
        """ get all resources needed by this step """
        if self._merged_resources is None:
            merged_resources = copy.copy(self._get_resources())
            if self.checklet:
                for name, resources in self.checklet.get_resources().items():
                    if name in merged_resources:
                        merged_resources[name] += resources
                    else:
                        merged_resources[name] = resources

            self._merged_resources = merged_resources

        return self._merged_resources


Step.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])
