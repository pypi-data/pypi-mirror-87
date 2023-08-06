import collections.abc
import typing
from pathlib import PurePosixPath

import momotor.bundles
from momotor.bundles.binding import ResultsComplexType, TestResultComplexType
from momotor.bundles.elements.base import Element, IdMixin, NestedElement
from momotor.bundles.elements.result import Result
from momotor.bundles.utils.keyedlist import KeyedList

try:
    from typing import final
except ImportError:
    from typing_extensions import final

__all__ = ['Results', 'ResultKeyedList']

# noinspection PyTypeChecker
RT = typing.TypeVar('RT', bound="Results")


ResultsType = typing.Union[KeyedList[Result], typing.Mapping[str, Result], typing.Sequence[Result]]


class ResultKeyedList(KeyedList[Result]):
    """ The results as a :py:class:`~momotor.bundles.utils.keyedlist.KeyedList`
    of :py:class:`~momotor.bundles.elements.result.Result` objects.

    The KeyedList allows access as a list or a mapping. Results are indexed by their `step_id` attribute
    """

    def __init__(self, results: ResultsType = None):
        super().__init__(results, key_attr='step_id')


# noinspection PyProtectedMember
class Results(NestedElement[ResultsComplexType, TestResultComplexType], IdMixin):
    # noinspection PyUnresolvedReferences
    """ A Results element encapsulating :py:class:`~momotor.bundles.binding.momotor.ResultsComplexType`
    """
    _results: ResultKeyedList = ResultKeyedList()

    @final
    @property
    def results(self) -> ResultKeyedList:
        # TODO raise exception if results was not initialized yet (this is a breaking change)
        return self._results.copy()

    @results.setter
    def results(self, results: typing.Optional[typing.Sequence[Result]]):
        assert results is None or (
            isinstance(results, collections.abc.Sequence) and all(result.bundle == self.bundle for result in results)
        )

        self._results = ResultKeyedList(results)

    @staticmethod
    def get_node_type() -> typing.Type[ResultsComplexType]:
        return ResultsComplexType

    @staticmethod
    def _get_parent_type() -> typing.Type[TestResultComplexType]:
        return TestResultComplexType

    # noinspection PyShadowingBuiltins
    def create(self: RT, *, id: str = None, results: ResultsType = None) -> RT:
        # TODO: meta
        self.id = id
        self.results = results
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) \
            -> typing.NoReturn:
        """ not implemented """
        raise NotImplementedError

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: ResultsComplexType, testresult: TestResultComplexType = None) -> "Results":
        self._check_node_type(node)
        self._check_parent_type(testresult, True)

        return self.create(
            id=node.id,
            results=[
                Result(self.bundle)._create_from_node(result, node) for result in node.result
            ] if node.result else None
        )

    def _construct_node(self) -> ResultsComplexType:
        # noinspection PyArgumentList
        return self.get_node_type()(
            id=self.id,
            result=[
                result._construct_node() for result in self._results.values()
            ] if self.results else None
        )


Results.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])
