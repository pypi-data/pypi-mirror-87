import collections.abc
import typing
from pathlib import PurePosixPath

import momotor.bundles
from momotor.bundles.binding import OptionComplexType, OptionsComplexType
from momotor.bundles.elements.base import Element
from momotor.bundles.elements.content import ContentTypeElement
from momotor.bundles.elements.refs import resolve_ref
from momotor.bundles.elements.wildcard import WildcardAttrsMixin
from momotor.bundles.typing.element import ElementMixinProtocol
from momotor.bundles.utils.nodes import get_nested_complex_nodes

try:
    from typing import final
except ImportError:
    from typing_extensions import final

__all__ = ['Option', 'OptionsMixin']


DEFAULT_DOMAIN = 'checklet'


class Option(
    ContentTypeElement[OptionComplexType, OptionsComplexType],
    WildcardAttrsMixin[OptionComplexType],
):
    """ An Option element encapsulating :py:class:`~momotor.bundles.binding.momotor.OptionComplexType`
    """
    _domain: str = DEFAULT_DOMAIN
    _external: typing.Optional[bool] = None
    _description: typing.Optional[str] = None

    @final
    @property
    def domain(self) -> str:
        """ `domain` attribute """
        return self._domain

    @domain.setter
    def domain(self, domain: typing.Optional[str]):
        assert domain is None or isinstance(domain, str)
        self._domain = domain or DEFAULT_DOMAIN

    @final
    @property
    def external(self) -> typing.Optional[bool]:
        """ `external` attribute """
        return self._external

    @external.setter
    def external(self, external: typing.Optional[bool]):
        assert external in (None, True, False)
        self._external = external
        
    @final
    @property
    def description(self) -> typing.Optional[str]:
        """ `description` attribute """
        return self._description

    @description.setter
    def description(self, description: typing.Optional[str]):
        assert description is None or isinstance(description, str)
        self._description = description

    @staticmethod
    def get_node_type() -> typing.Type[OptionComplexType]:
        return OptionComplexType

    @staticmethod
    def _get_parent_type() -> typing.Type[OptionsComplexType]:
        return OptionsComplexType

    # noinspection PyShadowingBuiltins
    def create(self, *,
               name: str,
               value: typing.Any = None,
               type: str = None,
               domain: str = None,
               external: bool = None,
               description: str = None,
               attrs: typing.Dict[str, str] = None,
               ) -> "Option":

        self._create_content(name=name, value=value, type=type)

        self.domain = domain or DEFAULT_DOMAIN
        self.external = external
        self.description = description
        self.attrs = attrs

        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) -> "Option":
        assert target_basesrc is None or isinstance(target_basesrc, PurePosixPath)

        return Option(target_bundle).create(
            name=self.name,
            value=self.value,
            domain=self.domain,
            external=self.external,
            description=self.description,
            attrs=self._attrs,
        )

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: OptionComplexType,
                          direct_parent: OptionsComplexType,
                          ref_parent: typing.Optional[OptionsComplexType]) -> "Option":
        self._check_node_type(node)
        self._check_parent_type(direct_parent)
        self._check_parent_type(ref_parent, True)

        self._create_content_from_node(node, direct_parent, ref_parent)
        self._create_attrs_from_node(node)

        domain = DEFAULT_DOMAIN
        domain_parts = self._get_attr_base_parts('domain', node, direct_parent, ref_parent,
                                                 base_attr='domain', allow_base_only=True)
        if domain_parts:
            for dp in domain_parts:
                domain = (domain.split('#', 1)[0] if dp.startswith('#') else '') + dp

        self.domain = domain
        self.external = node.external
        self.description = node.description

        return self

    def _construct_node(self) -> OptionComplexType:
        domain = self.domain
        if domain == DEFAULT_DOMAIN:
            domain = None
        elif domain.startswith(DEFAULT_DOMAIN + '#'):
            domain = domain[len(DEFAULT_DOMAIN):]

        # noinspection PyArgumentList
        return (
            self._construct_attrs(
                self._construct_content(
                    self.get_node_type()(
                        domain=domain,
                        external=self.external,
                        description=self.description,
                    )
                )
            )
        )


Option.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])


# noinspection PyProtectedMember
class OptionsMixin:
    # noinspection PyUnresolvedReferences
    """ A mixin for Elements to implement options

    :ivar options: List of :py:class:`~momotor.bundles.options.Option` objects
    """
    _options: typing.Optional[typing.List[Option]] = None
    _options_by_domain_name: typing.Optional[typing.Dict[str, typing.Dict[str, typing.List[Option]]]] = None

    @final
    @property
    def options(self) -> typing.Optional[typing.List[Option]]:
        """ `options` children """
        return None if self._options is None else [*self._options]

    @options.setter
    def options(self, options: typing.Optional[typing.Sequence[Option]]):
        assert options is None or isinstance(options, collections.abc.Sequence)
        self._options = None if options is None else [*options]
        self._options_by_domain_name = None

    def _collect_options(self: ElementMixinProtocol,
                         parent: object,
                         ref_parents: typing.Iterable[typing.Iterable[OptionComplexType]]) \
            -> typing.List[Option]:

        options: typing.List[Option] = []
        options_node: typing.Optional[OptionsComplexType] = None
        for tag_name, node in get_nested_complex_nodes(parent, 'options', 'option'):
            if tag_name == 'options':
                options_node = typing.cast(OptionsComplexType, node)
            else:
                option_node = typing.cast(OptionComplexType, node)
                if ref_parents:
                    ref_parent, option_node = resolve_ref('option', option_node, ref_parents)
                else:
                    ref_parent = None

                options.append(
                    Option(self.bundle)._create_from_node(option_node, options_node, ref_parent)
                )

        return options

    # noinspection PyMethodMayBeStatic
    def _construct_options_nodes(self, options: typing.Optional[typing.List[Option]]) \
            -> typing.List[OptionsComplexType]:
        # TODO group by domain
        if options:
            return [
                OptionsComplexType(option=[
                    option._construct_node()
                    for option in options
                ])
            ]

        return []

    def get_options(self, name: str, *, domain: str = DEFAULT_DOMAIN) -> typing.List[Option]:
        """ Get options

        :param name: `name` of the options to get
        :param domain: `domain` of the options to get. Defaults to "checklet"
        :return: A list of all matching options.
        """
        if self._options_by_domain_name is None:
            self._options_by_domain_name = {}
            for option in self.options:
                option_domain, option_name = option.domain, option.name

                if option_domain not in self._options_by_domain_name:
                    domain_options = self._options_by_domain_name[option_domain] = {}
                else:
                    domain_options = self._options_by_domain_name[option_domain]

                if option_name not in domain_options:
                    options = domain_options[option_name] = []
                else:
                    options = domain_options[option_name]

                options.append(option)

        return self._options_by_domain_name[domain][name]

    def get_option_value(self, name: str, *, domain: str = DEFAULT_DOMAIN) -> typing.Any:
        """ Get the value for a single option.
        If multiple options match, the value of the first one found will be returned

        :param name: `name` of the option to get
        :param domain: `domain` of the option to get. Defaults to "checklet"
        :return: The option value
        """
        return self.get_options(name, domain=domain)[0].value
