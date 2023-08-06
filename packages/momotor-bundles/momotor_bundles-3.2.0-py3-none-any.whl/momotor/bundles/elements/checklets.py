import collections.abc
import typing
from dataclasses import dataclass, field
from pathlib import PurePosixPath

import momotor.bundles
from momotor.bundles.binding import CheckletComplexType, CheckletsComplexType, LinkComplexType
from momotor.bundles.elements.base import NestedElement, Element
from momotor.bundles.elements.refs import resolve_ref
from momotor.bundles.elements.resources import Resource, ResourcesMixin
from momotor.bundles.typing.element import ElementMixinProtocol

try:
    from typing import final
except ImportError:
    from typing_extensions import final

__all__ = ['Checklet', 'CheckletMixin']

CT = typing.TypeVar('CT', bound=object)


@dataclass(frozen=True)
class Repository:
    """ An immutable `dataclass` for a reference to a repository
    """
    #: The src of the repository. Can be a url or a local path
    src: str = field()
    #: The type of the repository
    type: str = field()
    #: The revision of the repository
    revision: str = field()


@dataclass(frozen=True)
class Link:
    """ An immutable `dataclass` for a reference to a link
    """
    #: The src of the link
    src: str = field()


@dataclass(frozen=True)
class PackageVersion:
    """ An immutable `dataclass` for a reference to a package with version
    """
    #: The name of the package
    name: str = field()
    #: The version qualifier for the package
    version: str = field()


class Checklet(
    NestedElement[CheckletComplexType, CheckletsComplexType],
    ResourcesMixin,
):
    """ A Checklet element encapsulating :py:class:`~momotor.bundles.binding.momotor.checkletComplexType`
    """
    _name: typing.Optional[str] = None
    _extras: typing.Optional[typing.List[str]] = None
    _version: typing.Optional[str] = None
    _entrypoint: typing.Optional[str] = None
    _repository: typing.Optional[Repository] = None
    _link: typing.Optional[Link] = None
    _indices: typing.Optional[typing.List[Link]] = None
    _package_versions: typing.Optional[typing.List[PackageVersion]] = None

    @final
    @property
    def name(self) -> typing.Optional[str]:
        """ `name` attribute: The Python package name of the checklet """
        return self._name

    @name.setter
    def name(self, name: typing.Optional[str]):
        assert name is None or isinstance(name, str)
        self._name = name

    @final
    @property
    def extras(self) -> typing.Optional[typing.List[str]]:
        """ `extras` attribute: The Python package extras (eg. "requests") """
        return None if self._extras is None else [*self._extras]

    @extras.setter
    def extras(self, extras: typing.Optional[typing.Sequence[str]]):
        assert extras is None or isinstance(extras, collections.abc.Sequence)
        self._extras = None if extras is None else [*extras]

    @final
    @property
    def version(self) -> typing.Optional[str]:
        """ `version` attribute: A :pep:`440` Python package version specifier (eg. ">=1.0") """
        return self._version

    @version.setter
    def version(self, version: typing.Optional[str]):
        assert version is None or isinstance(version, str)
        self._version = version

    @final
    @property
    def entrypoint(self) -> typing.Optional[str]:
        """ `entrypoint` attribute: Override the default package entrypoint (unused, untested) """
        return self._entrypoint

    @entrypoint.setter
    def entrypoint(self, entrypoint: typing.Optional[str]):
        assert entrypoint is None or isinstance(entrypoint, str)
        self._entrypoint = entrypoint

    @final
    @property
    def repository(self) -> typing.Optional[Repository]:
        """ `repository` attribute: where to retrieve the package from """
        return self._repository

    @repository.setter
    def repository(self, repository: typing.Optional[Repository]):
        assert repository is None or isinstance(repository, Repository)
        if self._repository:
            # noinspection PyProtectedMember
            self.bundle._unregister_attachment(PurePosixPath(self._repository.src))

        self._repository = repository

        if repository:
            # noinspection PyProtectedMember
            self.bundle._register_attachment(PurePosixPath(repository.src))

    @final
    @property
    def link(self) -> typing.Optional[Link]:
        """ `link` attribute: (unused, untested) """
        return self._link

    @link.setter
    def link(self, link: typing.Optional[Link]):
        assert link is None or isinstance(link, Link)
        if self._link:
            # noinspection PyProtectedMember
            self.bundle._unregister_attachment(PurePosixPath(self._link.src))

        self._link = link

        if link:
            # noinspection PyProtectedMember
            self.bundle._register_attachment(PurePosixPath(link.src))

    @final
    @property
    def indices(self) -> typing.Optional[typing.List[Link]]:
        """ `indices` attribute: (unused, untested) """
        return None if self._indices is None else [*self._indices]

    @indices.setter
    def indices(self, indices: typing.Optional[typing.Sequence[Link]]):
        assert indices is None or isinstance(indices, collections.abc.Sequence)
        if indices is not None:
            raise ValueError("'Index' type checklets are not supported yet")

    @final
    @property
    def package_versions(self) -> typing.Optional[typing.List[PackageVersion]]:
        """ `package_versions` attribute: (unused, untested) """
        return None if self._package_versions is None else [*self._package_versions]

    @package_versions.setter
    def package_versions(self, package_versions: typing.Optional[typing.Sequence[PackageVersion]]):
        assert package_versions is None or isinstance(package_versions, collections.abc.Sequence)
        self._package_versions = None if package_versions is None else [*package_versions]

    @staticmethod
    def get_node_type() -> typing.Type[CheckletComplexType]:
        return CheckletComplexType

    @staticmethod
    def _get_parent_type() -> typing.Type[CheckletsComplexType]:
        return CheckletsComplexType

    # noinspection PyAttributeOutsideInit
    def create(self,
               name: str = None,
               extras: typing.Sequence[str] = None,
               version: str = None,
               entrypoint: str = None,
               repository: Repository = None,
               link: Link = None,
               indices: typing.List[Link] = None,
               package_versions: typing.Sequence[PackageVersion] = None,
               resources: typing.Sequence[Resource] = None,
               ) -> "Checklet":

        self.name = name
        self.extras = extras
        self.version = version
        self.entrypoint = entrypoint
        self.repository = repository
        self.link = link
        self.indices = indices
        self.package_versions = package_versions
        self.resources = resources
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle",
                 target_basesrc: PurePosixPath = None) -> "Checklet":
        assert target_basesrc is None or isinstance(target_basesrc, PurePosixPath)

        return Checklet(target_bundle).create(
            name=self.name,
            extras=self.extras,
            version=self.version,
            entrypoint=self.entrypoint,
            repository=self.repository,
            link=self.link,
            indices=self.indices,
            package_versions=self.package_versions,
            resources=self.resources,
        )

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: CheckletComplexType, parent: CheckletsComplexType = None) -> "Checklet":
        self._check_node_type(node)
        self._check_parent_type(parent, True)

        name = []
        if parent and parent.basename:
            name.append(parent.basename)
        if node.name:
            name.append(node.name)

        extras = [extra.strip() for extra in node.extras.split(',')] if node.extras else None

        if node.repository:
            assert len(node.repository) == 1
            repository = Repository(node.repository[0].src, node.repository[0].type, node.repository[0].revision)
        else:
            repository = None

        if node.link:
            assert len(node.link) == 1
            # assert not repository
            link = Link(node.link[0].src)
        else:
            link = None

        if node.index:
            assert not repository
            assert not link
            indices = [
                Link(src=index.src) for index in node.index
            ]
        else:
            indices = None

        if node.package_version:
            package_versions = [
                PackageVersion(package_version.name, package_version.version)
                for package_version in node.package_version
            ]
        else:
            package_versions = None

        return self.create(
            name='.'.join(name) if name else None,
            extras=extras,
            version=node.version,
            entrypoint=node.entrypoint,
            repository=repository,
            link=link,
            indices=indices,
            package_versions=package_versions,
            resources=self._collect_resources(node)
        )

    def _construct_repository_nodes(self):
        if self._repository:
            # noinspection PyCallByClass
            return [
                CheckletComplexType.Repository(
                    src=self._repository.src,
                    type=self._repository.type,
                    revision=self._repository.revision
                )
            ]

        return []

    def _construct_link_nodes(self):
        if self._link:
            return [
                LinkComplexType(src=self._link.src)
            ]

        return []

    def _construct_index_nodes(self):
        if self._indices:
            return [
                LinkComplexType(src=i.src)
                for i in self._indices
            ]

        return []

    def _construct_package_version_nodes(self):
        if self._package_versions:
            # noinspection PyCallByClass
            return [
                CheckletComplexType.PackageVersion(name=pv.name, version=pv.version)
                for pv in self._package_versions
            ]

        return []

    def _construct_node(self) -> CheckletComplexType:
        # noinspection PyArgumentList
        return self.get_node_type()(
            name=self.name,
            extras=','.join(self.extras) if self.extras else None,
            version=self.version,
            entrypoint=self.entrypoint,
            repository=self._construct_repository_nodes(),
            link=self._construct_link_nodes(),
            index=self._construct_index_nodes(),
            package_version=self._construct_package_version_nodes(),
            resources=self._construct_resources_nodes(self.resources),
        )


# Extend the docstring with the generic documentation of Element
Checklet.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])


class CheckletMixin(typing.Generic[CT]):
    def _collect_checklet(self: ElementMixinProtocol, node: CT,
                          ref_groups: typing.Iterable[typing.Iterable[object]]) \
            -> typing.Optional[Checklet]:

        # TODO use top-level <checklets> node and refs
        if node.checklet:
            if len(node.checklet) > 1:
                raise ValueError("Only one <checklet> node allowed")

            ref_parent, checklet_node = resolve_ref('checklet', node.checklet[0], ref_groups)
            # noinspection PyProtectedMember
            return Checklet(self.bundle)._create_from_node(checklet_node, ref_parent)

        return None
