import collections.abc
import typing
from pathlib import PurePosixPath, Path

import momotor.bundles
from momotor.bundles.binding import FileComplexType, FilesComplexType
from momotor.bundles.elements.base import Element
from momotor.bundles.elements.content import ContentSrcElement
from momotor.bundles.elements.refs import resolve_ref
from momotor.bundles.elements.wildcard import WildcardAttrsMixin
from momotor.bundles.typing.element import ElementMixinProtocol
from momotor.bundles.utils.nodes import get_nested_complex_nodes

try:
    from typing import final
except ImportError:
    from typing_extensions import final

__all__ = ['File', 'FilesMixin']


# def merge(ls: typing.Iterable = None, extra=None) -> typing.List:
#     """ Filter all None values from `ls`, append `extra` """
#     ls = [item for item in ls if item is not None] if ls else []
#     if extra is not None:
#         ls.append(extra)
#     return ls


class File(
    ContentSrcElement[FileComplexType, FilesComplexType],
    WildcardAttrsMixin[FileComplexType]
):
    """ A File element encapsulating :py:class:`~momotor.bundles.binding.momotor.fileComplexType`
    """
    _class: typing.Optional[str] = None

    @final
    @property
    def class_(self) -> typing.Optional[str]:
        """ `class` attribute """
        return self._class

    @class_.setter
    def class_(self, class_: typing.Optional[str]):
        assert class_ is None or isinstance(class_, str)
        self._class = class_

    @staticmethod
    def get_node_type() -> typing.Type[FileComplexType]:
        return FileComplexType

    @staticmethod
    def _get_parent_type() -> typing.Type[FilesComplexType]:
        return FilesComplexType

    # noinspection PyShadowingBuiltins
    def create(self, *,
               class_: str = None,
               name: typing.Union[str, PurePosixPath] = None,
               src: PurePosixPath = None,
               content: typing.Union[bytes, str] = None,
               type: str = None,
               attrs: typing.Mapping[str, str] = None,
               ) -> "File":

        self._create_content(name=name, value=content, src=src, type=type)

        self.attrs = attrs
        self.class_ = class_

        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) -> "File":
        assert target_basesrc is None or isinstance(target_basesrc, PurePosixPath)

        return File(target_bundle).create(
            class_=self.class_,
            name=self.name,
            src=self._recreate_src(target_bundle, target_basesrc),
            content=self.value,
            attrs=self._attrs,
        )

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: FileComplexType,
                          direct_parent: FilesComplexType,
                          ref_parent: typing.Optional[FilesComplexType]) -> "File":
        self._check_node_type(node)
        self._check_parent_type(direct_parent)
        self._check_parent_type(ref_parent, True)

        self._create_content_from_node(node, direct_parent, ref_parent)
        self._create_attrs_from_node(node)

        class_parts = self._get_attr_base_parts('class_value', node, direct_parent, ref_parent, base_attr='baseclass',
                                                allow_base_only=True)
        self.class_ = '.'.join(class_parts) if class_parts else None

        return self

    def _construct_node(self) -> FileComplexType:
        # noinspection PyArgumentList
        return (
            self._construct_attrs(
                self._construct_content(
                    self.get_node_type()(
                        class_value=self.class_,
                    )
                )
            )
        )

    def _join_name(self, parts: typing.Iterable):
        return PurePosixPath(*parts)


File.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])


# noinspection PyProtectedMember
class FilesMixin:
    """ Mixin for `Element` to add file support.
    """
    _has_files: bool = False

    def _collect_files(self: ElementMixinProtocol, parent: object,
                       ref_parents: typing.Iterable[typing.Iterable[FilesComplexType]]) \
            -> typing.List[File]:

        files: typing.List[File] = []
        files_node: typing.Optional[FilesComplexType] = None
        for tag_name, node in get_nested_complex_nodes(parent, 'files', 'file'):
            if tag_name == 'files':
                files_node = typing.cast(FilesComplexType, node)
            else:
                file_node = typing.cast(FileComplexType, node)
                if ref_parents:
                    ref_parent, node = resolve_ref('file', file_node, ref_parents)
                else:
                    ref_parent = None

                files.append(
                    File(self.bundle)._create_from_node(node, files_node, ref_parent)
                )

        return files

    # noinspection PyMethodMayBeStatic
    def _construct_files_nodes(self, files: typing.Optional[typing.List[File]]) -> typing.List[FilesComplexType]:
        # TODO group by class
        if files:
            return [
                FilesComplexType(file=[
                    file._construct_node()
                    for file in files
                ])
            ]

        return []

    def _get_attachment_group_id(self):
        return getattr(self, '_attachments_group_id', getattr(self, 'id', '')) or ''

    @final
    @property
    def files(self: ElementMixinProtocol) -> typing.Optional[typing.List[File]]:
        """ The files
        """
        return self.bundle._get_files(self._get_attachment_group_id())

    @files.setter
    def files(self: ElementMixinProtocol, files: typing.Optional[typing.List[File]]):
        if files is not None:
            assert isinstance(files, collections.abc.Sequence) and all(file.bundle == self.bundle for file in files)
            self._has_files = True
            self.bundle._set_files(self._get_attachment_group_id(), files)

    def copy_files(self: ElementMixinProtocol, dest_dir: Path) -> None:
        """ Copy the files to `dest_dir` """
        self.bundle._copy_files(dest_dir, self._get_attachment_group_id())
