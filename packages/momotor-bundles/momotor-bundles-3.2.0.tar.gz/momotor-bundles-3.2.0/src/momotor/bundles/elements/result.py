import typing
import warnings
from pathlib import PurePosixPath

import momotor.bundles
from momotor.bundles.binding import ResultComplexType, ResultsComplexType, OutcomeSimpleType
from momotor.bundles.elements.base import NestedElement, Element
from momotor.bundles.elements.checklets import CheckletMixin, Checklet
from momotor.bundles.elements.files import FilesMixin, File
from momotor.bundles.elements.options import Option, OptionsMixin
from momotor.bundles.elements.properties import PropertiesMixin, Property

try:
    from typing import final
except ImportError:
    from typing_extensions import final

__all__ = ['Result', 'create_error_result']


class Result(
    NestedElement[ResultComplexType, ResultsComplexType],
    CheckletMixin[ResultComplexType],
    PropertiesMixin, OptionsMixin, FilesMixin
):
    """ A Result element encapsulating :py:class:`~momotor.bundles.binding.momotor.ResultComplexType`
    """
    _attachments_group_id: typing.Optional[str] = None
    _step_id: typing.Optional[str] = None
    _outcome: typing.Optional[OutcomeSimpleType] = None
    _checklet: typing.Optional[Checklet] = None
    _parent_id: typing.Optional[str] = None

    @final
    @property
    def step_id(self) -> str:
        """ `step_id` attribute """
        if self._step_id is None:
            raise ValueError("Result not initialized: step_id not yet set")

        return self._step_id

    @step_id.setter
    def step_id(self, step_id: str):
        assert isinstance(step_id, str)
        self._step_id = step_id
        self._update_attachments_group_id()

    @final
    @property
    def outcome(self) -> str:
        """ `outcome` attribute. Valid values are ``pass``, ``fail`` and ``error`` """
        if self._outcome is None:
            raise ValueError("Result not initialized: outcome not yet set")

        return self._outcome.value

    @outcome.setter
    def outcome(self, outcome: str):
        assert isinstance(outcome, str)

        try:
            outcome_enum = OutcomeSimpleType(outcome)
        except ValueError:
            warnings.warn(f"Invalid outcome attribute value '{outcome}' ignored (will use 'error')")
            outcome_enum = OutcomeSimpleType.ERROR

        self._outcome = outcome_enum

    @final
    @property
    def checklet(self) -> typing.Optional[Checklet]:
        """ `checklet` """
        return self._checklet

    @checklet.setter
    def checklet(self, checklet: typing.Optional[Checklet]):
        assert checklet is None or (isinstance(checklet, Checklet) and checklet.bundle == self.bundle)
        self._checklet = checklet

    def set_parent_id(self, parent_id: typing.Optional[str]):
        """ Set the id of the result parent """
        assert parent_id is None or isinstance(parent_id, str)
        assert not self._has_files, "parent id must be set before files are added"
        self._parent_id = parent_id
        self._update_attachments_group_id()

    def _update_attachments_group_id(self):
        if self._step_id:
            if self._parent_id:
                self._attachments_group_id = f'{self._step_id}@{self._parent_id}'
            else:
                self._attachments_group_id = self._step_id
        elif self._parent_id:
            self._attachments_group_id = f'@{self._parent_id}'

    @staticmethod
    def get_node_type() -> typing.Type[ResultComplexType]:
        return ResultComplexType

    @staticmethod
    def _get_parent_type() -> typing.Type[ResultsComplexType]:
        return ResultsComplexType

    def create(self, *,
               step_id: str,
               outcome: str,
               checklet: Checklet = None,
               properties: typing.List[Property] = None,
               options: typing.List[Option] = None,
               files: typing.List[File] = None,
               parent_id: str = None,
               ) -> "Result":

        self.set_parent_id(parent_id)
        self.step_id = step_id
        self.outcome = outcome
        self.checklet = checklet
        self.properties = properties
        self.options = options
        self.files = files
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) -> "Result":
        assert target_basesrc is None or isinstance(target_basesrc, PurePosixPath)

        return Result(target_bundle).create(
            step_id=self.step_id,
            outcome=self.outcome,
            checklet=self.checklet.recreate(target_bundle) if self.checklet is not None else None,
            properties=self.recreate_list(self.properties, target_bundle, target_basesrc),
            options=self.recreate_list(self.options, target_bundle, target_basesrc),
            files=self.recreate_list(self.files, target_bundle, target_basesrc),
            parent_id=self._parent_id,
        )

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: ResultComplexType, results: ResultsComplexType = None) -> "Result":
        self._check_node_type(node)
        self._check_parent_type(results, True)

        return self.create(
            step_id=node.step,
            outcome=node.outcome.value,
            checklet=self._collect_checklet(node, [results.checklets] if results else []),
            properties=self._collect_properties(node),
            options=self._collect_options(node, []),
            files=self._collect_files(node, []),
            parent_id=results.id if results else None,
        )

    def _construct_node(self) -> ResultComplexType:
        # noinspection PyArgumentList
        return self.get_node_type()(
            step=self.step_id,
            outcome=self._outcome,
            # TODO checklet
            properties=self._construct_properties_nodes(self.properties),
            options=self._construct_options_nodes(self.options),
            files=self._construct_files_nodes(self.files),
        )

    @final
    @property
    def passed(self) -> bool:
        """ Returns True if `outcome` is ``pass`` """
        return self._outcome == OutcomeSimpleType.PASS

    @final
    @property
    def failed(self) -> bool:
        """ Returns True if `outcome` is ``fail`` """
        return self._outcome == OutcomeSimpleType.FAIL

    @final
    @property
    def erred(self) -> bool:
        """ Returns True if `outcome` is ``error`` """
        return self._outcome == OutcomeSimpleType.ERROR


Result.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])


def create_error_result(bundle, step_id, status, report=None):
    """ Create an error result """
    return Result(bundle).create(
        step_id=step_id,
        outcome='error',
        properties=[
            Property(bundle).create(name='status', type='string', value=status),
            Property(bundle).create(name='report', type='string', value=report or status),
        ]
    )
