import typing
from abc import ABC
from collections import deque
from contextlib import contextmanager
from io import BytesIO
from pathlib import PurePosixPath, Path, PurePath

import shutil
import time
import warnings
from xsdata.formats.dataclass.models.generics import AnyElement
from xsdata.utils.namespaces import build_qname

import momotor.bundles
from momotor.bundles.binding.momotor_1_0 import __NAMESPACE__
from momotor.bundles.const import DEFAULT_TIME_STAMP
from momotor.bundles.elements.base import NestedElement, Element
from momotor.bundles.utils.encoding import decode_data, encode_data, encode_posix_path

try:
    from typing import final
except ImportError:
    from typing_extensions import final

__all__ = ['ContentElement', 'ContentTypeElement', 'ContentSrcElement']


def is_printable(s: str):
    return all((32 <= ord(c) < 127 or ord(c) >= 160) for c in s)


VALUE_TYPE_MAP = {
    'string': str,
    'integer': int,
    'float': float,
}

DEPRECATED_VALUE_TYPES = {
    'int': 'integer'
}

CT = typing.TypeVar('CT', bound=object)
PCT = typing.TypeVar('PCT', bound=object)

true_qname = build_qname(__NAMESPACE__, 'true')
false_qname = build_qname(__NAMESPACE__, 'false')
none_qname = build_qname(__NAMESPACE__, 'none')


class ContentElement(NestedElement[CT, PCT], ABC):
    """ Base class for elements with content, either as a value attribute, child nodes or as an attachment.
    Handles 'name', 'src', 'type', 'value' and 'encoding' attributes and child node content.
    This unifies the handling of <option>, <property> and <file> nodes

    The subclasses ContentTypeElement and ContentSrcElement exist mainly to create the proper documentation of the
    properties and methods.

    'src', 'value' and child nodes with content are mutually exclusive.
    'type' has a double role: For nodes with a 'value' attribute it indicates the type (string, integer or float),
    for nodes with child content or src, it is the content mime type.
    'encoding' is only used with child content, it is either 'base64' or 'quopri'
    """
    MAX_VALUE_LENGTH = 1000

    _name: typing.Optional[str] = None  # The name attribute
    _src_path: typing.Optional[PurePosixPath] = None  # The src attribute
    _type: typing.Optional[str] = None  # The type attribute
    _value: typing.Optional[str] = None  # The value attribute
    _encoding: typing.Optional[str] = None  # The encoding attribute

    _raw_content: typing.Optional[typing.Sequence] = None  # Unprocessed content
    _processed_value: typing.Optional[typing.Tuple] = None  # Processed content
    _content_type: typing.Optional[str] = None  # The child content

    @property
    def name(self) -> typing.Optional[str]:
        """ `name` attribute """
        return self._name

    @name.setter
    def name(self, name: typing.Optional[str]):
        assert name is None or isinstance(name, str)
        self._name = name

    @property
    def value(self) -> typing.Any:
        """ `value` attribute: The content """
        return self._process_value()[0]

    @value.setter
    def value(self, value: typing.Any):
        self._src_path = None
        self._value = None
        self._processed_value = (value,)
        self._raw_content = None

    @property
    def encoding(self) -> typing.Optional[str]:
        """ `encoding` attribute: read-only, the encoding is automatically determined from the value """
        self._create_node_content()
        return self._encoding

    def _create_content(self, *, name: typing.Union[str, PurePosixPath] = None, value: typing.Any = None) -> None:
        self.name = name
        self.value = value

    def _join_name(self, parts: typing.Iterable):
        return '.'.join(parts)

    def _create_content_from_node(self, node: CT, direct_parent: PCT, ref_parent: typing.Optional[PCT]):
        """ Set the attributes from the XML dom node

        Child content is saved as-is and processing is postponed until the value or type properties are accessed

        :param node: the node to copy the attributes from
        :param direct_parent: the node's direct parent
        :param ref_parent: the node's ref-parent, the predecessor to which the 'ref' attribute refers
        :return:
        """
        name_parts = self._get_attr_base_parts('name', node, direct_parent, ref_parent)
        src_parts = self._get_attr_base_parts(
            'src', node, direct_parent, ref_parent,
            lambda src: src[5:] if src.lower().startswith('file:') else src
        )

        self._name = self._join_name(name_parts) if name_parts else None
        self._src_path = PurePosixPath(*src_parts) if src_parts else None
        self._type = getattr(node, 'type', None)
        self._value = getattr(node, 'value', None)
        self._encoding = getattr(node, 'encoding', None)

        raw_content = None
        for item in node.any_element:
            if raw_content is None:
                raw_content = deque()

            if isinstance(item, str):
                raw_content.append(item)
            else:
                # TODO 'list' and 'tuple' elements
                if item.qname == true_qname:
                    raw_content.append(True)
                elif item.qname == false_qname:
                    raw_content.append(False)
                elif item.qname == none_qname:
                    raw_content.append(None)

        self._raw_content = raw_content
        self._processed_value = None
        self._content_type = None

    def _process_value(self) -> typing.Tuple[typing.Optional[typing.Any], typing.Optional[str]]:
        """ Get the processed value and content_type by decoding 'value' or raw content
        """
        if self._src_path:
            return None, self._content_type

        if self._processed_value is None:
            if self._raw_content is not None:
                content, content_text, has_text_content = [], '', False
                for item in self._raw_content:
                    if isinstance(item, str):
                        content_text += item
                        has_text_content |= (item.strip() != '')

                    elif has_text_content:
                        warnings.warn("Mixed content of strings and elements not supported")

                    else:
                        content.append(item)

                if has_text_content:
                    if self._encoding:
                        decoded = decode_data(content_text, self._encoding)
                        self._processed_value = (decoded,)
                    else:
                        self._processed_value = (content_text,)
                else:
                    self._processed_value = (content[0],)

                self._content_type = self._type

            elif self._value:
                typename = self._type

                correct_type = DEPRECATED_VALUE_TYPES.get(typename)
                if correct_type:
                    # noinspection PyTypeChecker
                    warnings.warn(f"Type '{typename}' deprecated, use '{correct_type}'", category=DeprecationWarning)
                    typename = correct_type

                if typename and typename not in VALUE_TYPE_MAP:
                    warnings.warn(f"Invalid type '{typename}' ignored")
                    datatype = str
                else:
                    datatype = VALUE_TYPE_MAP.get(typename, str)

                try:
                    self._processed_value = (datatype(self._value),)
                except ValueError:
                    self._processed_value = (self._value,)

                self._content_type = None

            else:
                # No content at all
                self._processed_value = tuple()
                self._content_type = None

        return self._processed_value[0] if self._processed_value else None, self._content_type

    def _create_node_content(self):
        """ Update __raw_content, __encoding, _type and _value attributes based on __processed_value and __content_type
        """
        if self._src_path:
            self._type = self._content_type
            self._raw_content = None
            self._encoding = None

        elif self._processed_value is not None and self._raw_content is None and self._value is None:
            value = self._processed_value[0] if self._processed_value else None
            if not self._processed_value:
                # Empty tuple, indicates empty node
                self._raw_content = tuple()
                self._encoding = None
                self._value = None
                self._type = None
                if self._content_type:
                    warnings.warn('"type" attribute cannot be used for empty content nodes')

            elif value is None or isinstance(value, bool):
                # Encoded using child elements <none/>, <true/> or <false/>
                self._raw_content = (value,)
                self._encoding = None
                self._value = None
                self._type = None

                if self._content_type:
                    warnings.warn('"type" attribute cannot be combined with None or boolean values')

            elif self._content_type is not None or isinstance(value, bytes) or (
                    isinstance(value, str) and (len(value) > self.MAX_VALUE_LENGTH or not is_printable(value))
            ):
                # Text content that needs to be encoded as child content
                encoded, encoding = encode_data(value)
                self._raw_content = (encoded,)
                self._encoding = encoding
                self._value = None
                self._type = self._content_type

            else:
                # Something that can be stored in the value attributed
                self._raw_content = None
                self._encoding = None
                self._value = str(value)

                # TODO 'list' and 'tuple' elements
                if isinstance(value, int):
                    self._type = 'integer'
                elif isinstance(value, float):
                    self._type = 'float'
                else:  # 'string' is default
                    self._type = None

                if self._content_type:
                    warnings.warn('"type" attribute cannot be used for numeric values')

    def __construct_raw_node(self, item: typing.Any) -> typing.Union[AnyElement, str]:
        if isinstance(item, bool):
            return AnyElement(qname=true_qname if item else false_qname)
        elif item is None:
            return AnyElement(qname=none_qname)
        elif isinstance(item, str):
            return item

        raise ValueError("Unable to convert convert element {}".format(item))

    # noinspection PyProtectedMember
    def _construct_content(self, node: CT) -> CT:
        """ Update the attributes of an XML dom node

        :param node: The node to update
        :return: node
        """
        self._create_node_content()

        if self._name is not None:
            setattr(node, 'name', str(self._name))

        if self._src_path is not None:
            setattr(node, 'src', str(self._src_path))

        if self._encoding is not None:
            setattr(node, 'encoding', self._encoding)

        if self._value is not None:
            setattr(node, 'value', self._value)

        if self._type is not None:
            setattr(node, 'type', self._type)

        if self._raw_content:
            node.any_element = [
                self.__construct_raw_node(item)
                for item in self._raw_content
            ]

        return node

    def has_inline_content(self) -> bool:
        """ Returns True if element has inline content
        """
        return self._processed_value is not None or self._raw_content is not None

    def has_inline_text_content(self) -> bool:
        """ Returns True if self.value would return text content
        (either bytes or str), without processing the content.
        """
        if self._processed_value and len(self._processed_value) == 1 \
                and isinstance(self._processed_value[0], (bytes, str)):
            return True

        elif self._raw_content is not None:
            for item in self._raw_content:
                if isinstance(item, str):
                    if item.strip() != '':
                        return True
                else:
                    return False

        elif self._value is not None:
            return self._type is None or self._type == 'string'

        return False

    # noinspection PyProtectedMember
    def has_attachment_content(self) -> bool:
        """ Returns True if this element has an existing attachment  """
        return False

    def has_text_content(self) -> bool:
        """ Returns True if the element has text content """
        return self.has_inline_text_content() or self.has_attachment_content()

    @contextmanager
    def open(self) -> typing.ContextManager[typing.BinaryIO]:
        """ Context manager to open the content """
        if self.has_inline_text_content():
            yield BytesIO(self.value)
        else:
            raise FileNotFoundError

    # noinspection PyProtectedMember
    def _copy(self, dest_path: Path):
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        if self.has_inline_text_content() or self.bundle._zip_wrapper:
            with self.open() as reader, open(str(dest_path), 'wb') as writer:
                shutil.copyfileobj(reader, writer)
        else:
            raise FileNotFoundError

    def copy_to(self, dest_dir: Path):
        """ Copy content to given directory

        :param dest_dir: base destination directory

        The file is created relative to `dest_dir`. If the node has a `src` attribute this is used as the remaining
        path and file name, otherwise the `name` attribute is used.

        So, if `src` is ``lorem/ipsum.txt`` and `dest_dir` is ``/tmp/``, the content will be written to a file
        ``/tmp/lorem/ipsum.txt``. Any missing intermediate directories will be created.

        TODO: The final path is currently not validated, so make sure it cannot be used to
              overwrite any important files!
        """
        self._copy(dest_dir / (self._name or self._src_path))


class ContentTypeElement(ContentElement[CT, PCT], ABC):
    """ A :py:class:`~momotor.bundles.elements.content.ContentElement` variant exposing the type property
    """
    @property
    def type(self) -> typing.Optional[str]:
        """ The `type` attribute. Indicates the type of the `value` attribute: string, integer or float """
        return self._process_value()[1]

    # noinspection PyShadowingBuiltins
    @type.setter
    def type(self, type: typing.Optional[str]):
        assert type is None or isinstance(type, str)
        self._type = type

    # noinspection PyShadowingBuiltins
    def _create_content(self, *, name: typing.Union[str, PurePosixPath] = None, value: typing.Any = None,
                        type: str = None) -> None:

        ContentElement._create_content(self, name=name, value=value)
        self.type = type


class ContentSrcElement(ContentTypeElement[CT, PCT], ABC):
    """ A :py:class:`~momotor.bundles.elements.content.ContentElement` variant exposing the type and src properties
    """
    _name: typing.Optional[typing.Union[str, PurePath]] = None  # The name attribute

    def _recreate_src(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) \
            -> typing.Optional[PurePosixPath]:

        if self.has_attachment_content():
            target_src = self.relative_path
            if target_src:
                if target_basesrc:
                    try:
                        new_src = target_src.relative_to(target_basesrc)
                    except ValueError:
                        target_src = target_basesrc / target_src
                    else:
                        target_src = target_basesrc / new_src

                target_src = encode_posix_path(target_src)
                # noinspection PyProtectedMember
                self._copy(target_bundle._base / target_src)
                return target_src

        return None

    @property
    def name(self) -> typing.Optional[typing.Union[str, PurePath]]:
        """ `name` attribute """
        return self._name

    @name.setter
    def name(self, name: typing.Optional[typing.Union[str, PurePath]]):
        assert name is None or isinstance(name, (str, PurePath))
        if hasattr(name, 'as_posix'):
            assert not name.is_absolute(), "'name' must be a string or relative path"
            name = name.as_posix()

        self._name = name

    @property
    def value(self) -> typing.Any:
        """ `value` attribute: The literal content. Mutually exclusive with `src` """
        return self._process_value()[0]

    @value.setter
    def value(self, value: typing.Any):
        self._src_path = None
        self._processed_value = (value,)
        self._raw_content = None

    @property
    def type(self) -> typing.Optional[str]:
        """ The `type` attribute. For nodes with a `value` attribute it indicates the type (string, integer or float),
        for nodes with child content or a `src` attribute, it is the content mime type. """
        return self._process_value()[1]

    # noinspection PyShadowingBuiltins
    @type.setter
    def type(self, type: typing.Optional[str]):
        assert type is None or isinstance(type, str)
        self._type = type

    @property
    def src(self) -> typing.Optional[PurePath]:
        """ `src` attribute: File path of the content. Mutually exclusive with `value` """
        return self._src_path

    @src.setter
    def src(self, src: typing.Optional[PurePath]):
        assert src is None or isinstance(src, PurePath)

        if src and self._value:
            raise ValueError("Cannot provide 'src' and 'content' for the same element")

        if hasattr(src, 'as_posix'):
            assert not src.is_absolute(), "'src' must be a path relative to bundle.base"
            if not isinstance(src, PurePosixPath):
                src = PurePosixPath(src.as_posix())

            if src != encode_posix_path(src):
                warnings.warn("The source path (src) should not contain any non-ascii characters")

        self._src_path = src
        self._processed_value = None
        self._raw_content = None

    # noinspection PyShadowingBuiltins
    def _create_content(self, *, name: typing.Union[str, PurePosixPath] = None, value: typing.Any = None,
                        src: PurePosixPath = None, type: str = None) -> None:
        ContentTypeElement._create_content(self, name=name, value=value, type=type)
        if src is not None:
            self.src = src

    def file_info(self) -> typing.Optional[typing.Tuple[int, time.struct_time]]:
        """ Get file info for the content. For inline content, a time stamp of midnight January 1st, 1980
        will be returned.

        :return: A tuple containing size and creation time timestamp.
        """
        value = self.value
        if isinstance(value, (bytes, str)):
            return len(value), DEFAULT_TIME_STAMP

        # noinspection PyProtectedMember
        return self.bundle._attachment_info(self.relative_path)

    # noinspection PyProtectedMember
    def has_attachment_content(self) -> bool:
        rel_path = self.relative_path
        if rel_path:
            return self.bundle._has_file_attachment(rel_path)

        return False

    @property
    def relative_path(self) -> PurePosixPath:
        return self._src_path or PurePosixPath(self._name)

    # noinspection PyProtectedMember
    @property
    def absolute_path(self) -> typing.Optional[Path]:
        rel_path = self.relative_path
        if self.bundle._base and rel_path:
            return self.bundle._base / rel_path

    @contextmanager
    def open(self) -> typing.ContextManager[typing.BinaryIO]:
        if self.has_inline_text_content():
            yield BytesIO(self.value)
        else:
            # noinspection PyProtectedMember
            with self.bundle._open_file_attachment(self.relative_path) as f:
                yield f

    # noinspection PyProtectedMember
    def _copy(self, dest_path: Path):
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        if self.has_inline_text_content() or self.bundle._zip_wrapper:
            with self.open() as reader, open(str(dest_path), 'wb') as writer:
                shutil.copyfileobj(reader, writer)
        else:
            abs_path = self.absolute_path
            if abs_path:
                # Direct file copy
                try:
                    shutil.copy(str(abs_path), str(dest_path))
                except shutil.SameFileError:
                    pass
            else:
                raise FileNotFoundError


# Extend the docstrings with the generic documentation of Element
ContentElement.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])
ContentSrcElement.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])
ContentTypeElement.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])
