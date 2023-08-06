import collections
import typing

from momotor.bundles.elements.base import Element

T = typing.TypeVar('T', bound=Element)


def group_by_attr(items: typing.Iterable[T], attr: str) -> typing.Dict[str, typing.Tuple[T]]:
    """ Group a list of elements by the value of an attribute

    :param items: list of elements to group
    :param attr: name of the attribute to group on
    :return: a dictionary of lists of elements
    """
    by_name: typing.Dict[str, typing.List[T]] = collections.defaultdict(lambda: [])
    for item in items:
        key = getattr(item, attr, None)
        by_name[key].append(item)

    return dict(
        (key, tuple(values))
        for key, values in by_name.items()
    )
