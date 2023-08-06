import contextlib
import pathlib
import typing
from abc import ABC
from collections import defaultdict
from contextlib import contextmanager
from io import BytesIO, open as io_open

import shutil
import sys
import time
import zipfile

from xsdata.exceptions import ParserError
from xsdata.models.enums import Namespace
from xsdata.utils.namespaces import build_qname

from momotor.bundles.binding.momotor_1_0 import __NAMESPACE__
from momotor.bundles.const import BundleFormat, BundleCategory, DEFAULT_TIME_STAMP
from momotor.bundles.elements.base import Element
from momotor.bundles.elements.files import File
from momotor.bundles.exception import BundleError, BundleLoadError, InvalidBundle, LxmlMissingError, BundleFormatError
from momotor.bundles.parsers.config import BundleParserConfig
from momotor.bundles.parsers.handlers.exceptions import ValidationError
from momotor.bundles.parsers.xml import XmlBundleParser
from momotor.bundles.serializers.xml import XmlBundleSerializer
from momotor.bundles.utils.zipwrapper import ZipWrapper

# lxml is an optional dependency
try:
    from lxml import etree as lxml_etree, sax as lxml_sax
    has_lxml = True
except ImportError:
    lxml_etree, lxml_sax = None, None
    has_lxml = False


__all__ = ["Bundle"]


SCHEMA_FILE_PATH = pathlib.Path(__file__).parent / 'schema' / 'momotor-1.0.xsd'
SCHEMA_NAMESPACE_LOCATION = 'http://momotor.org/schema/momotor-1.0.xsd'


PY37 = sys.version_info >= (3, 7)

# noinspection PyTypeChecker
BT = typing.TypeVar('BT', bound='Bundle')
CT = typing.TypeVar('CT', bound=object)


class Bundle(Element[CT], ABC, typing.Generic[CT]):
    """ Access a Momotor bundle

    :param base: A path to the directory containing the XML source file in `instance`.
                 Any file path is relative to this base.
    :param zip_wrapper: A :py:class:`~momotor.bundles.utils.zipwrapper.ZipWrapper` instance for the zip-file
                        containing the bundle, for internal use by the :py:meth:`~Bundle.from_bytes_factory` and
                        :py:meth:`~Bundle.from_file_factory` methods
    """
    _base: typing.Optional[pathlib.Path]
    _zip_wrapper: typing.Optional[ZipWrapper]
    _file_attachments: typing.Dict[str, typing.List[File]]
    _other_attachments: typing.Set[pathlib.PurePosixPath]

    def __init__(self, base: typing.Union[str, pathlib.Path] = None, zip_wrapper: ZipWrapper = None):
        Element.__init__(self, self)

        self._base = pathlib.Path(base) if base else None
        self._zip_wrapper = zip_wrapper
        self._file_attachments = defaultdict(list)
        self._other_attachments = set()

    def create(self: BT, **kwargs) -> BT:
        """ Set this bundle's attributes

        Usage:

        .. code-block:: python

           bundle = Bundle(...).create(...)

        :return: self
        """
        # noinspection PyTypeChecker
        return super().create(**kwargs)

    def close(self):
        """ Close bundle and release all files and resources held.

        Any access to the bundle after calling :py:meth:`~momotor.bundles.Bundle.close` will reopen
        the bundle and will require :py:meth:`~momotor.bundles.Bundle.close` to be called again.
        """
        if self._zip_wrapper:
            self._zip_wrapper.close()

    @staticmethod
    def get_default_xml_name() -> str:
        """ Get the default XML file name
        """
        raise NotImplementedError

    @classmethod
    def get_root_tag(cls) -> str:
        """ Get the XML root tag for this bundle
        """
        return cls.get_node_type().Meta.name

    @classmethod
    def get_root_qname(cls) -> str:
        """ Get the XML root tag for this bundle
        """
        return build_qname(cls.get_node_type().Meta.namespace, cls.get_root_tag())

    @staticmethod
    def get_category() -> BundleCategory:
        """ Get the category for this bundle
        """
        raise NotImplementedError

    # Attachments - files
    # TODO deduplicate files

    @contextmanager
    def _open_file_attachment(self, path: pathlib.PurePosixPath) -> typing.BinaryIO:
        assert isinstance(path, pathlib.PurePosixPath)
        if self._zip_wrapper:
            with self._zip_wrapper as zip_file, zip_file.open(str(path), 'r') as f:
                yield f

        elif self._base:
            abs_path = (self._base / path).resolve()
            with abs_path.open('rb') as f:
                yield f
        else:
            raise BundleError("Internal error: missing base")

    def _attachment_info(self, path: pathlib.PurePosixPath) -> typing.Optional[typing.Tuple[int, time.struct_time]]:
        """
        :param path:
        :return: tuple with file size and creation time tuple
        """
        assert isinstance(path, pathlib.PurePosixPath)
        if self._zip_wrapper:
            with self._zip_wrapper as zip_file:
                info = zip_file.getinfo(str(path))

            # ZipInfo.date_time is a 6-tuple. Convert it into a proper time.time_struct
            dt: typing.Tuple[int, int, int, int, int, int] = info.date_time
            try:
                time_stamp = time.localtime(time.mktime((dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], -1, -1, -1)))
            except (ValueError, OverflowError):
                time_stamp = DEFAULT_TIME_STAMP

            return info.file_size, time_stamp

        elif self._base:
            stat = (self._base / path).resolve().stat()
            return stat.st_size, time.localtime(stat.st_ctime)

        else:
            return None

    def _has_file_attachment(self, path: pathlib.PurePosixPath) -> bool:
        if self._zip_wrapper:
            with self._zip_wrapper as zip_file:
                try:
                    zip_file.getinfo(str(path))
                except KeyError:
                    return False
                else:
                    return True

        elif self._base:
            abs_path = (self._base / path).resolve()
            return abs_path.exists()

        else:
            return False

    # noinspection PyShadowingBuiltins
    def _get_files(self, id: str) -> typing.Optional[typing.List[File]]:
        """ Get files with `id`

        :param id: File id to get
        :return: List of files with `id`, or None of no files with that id exist
        """
        return self._file_attachments.get(id)

    def _all_files(self) -> typing.Generator[File, None, None]:
        """ Get all files

        :return: A generator producing every file attachment for this bundle
        """
        src_seen = set()
        for section in self._file_attachments.values():
            for file in section:
                if file.src not in src_seen:
                    yield file
                    src_seen.add(file.src)

    # noinspection PyShadowingBuiltins
    def _set_files(self, id: str, files: typing.List[File]):
        """ Set files with `id`

        :param: id: `id` of files
        :param: files: list of files
        """
        if files:
            self._file_attachments[id] = files
        else:
            try:
                del self._file_attachments[id]
            except KeyError:
                pass

    # noinspection PyShadowingBuiltins
    def _copy_files(self, dest_dir: pathlib.Path, id: str = None) -> None:
        """ Copy (write) files in a destination directory

        :param: dest_dir: Destination path
        :param: id: File id. If None, writes all files
        """
        files = self._all_files() if id is None else self._get_files(id)
        for file in files:
            file.copy_to(dest_dir)

    # Attachments - other

    def _register_attachment(self, path: pathlib.PurePosixPath) -> None:
        assert isinstance(path, pathlib.PurePosixPath)
        self._other_attachments.add(path)

    def _unregister_attachment(self, path: pathlib.PurePosixPath) -> None:
        assert isinstance(path, pathlib.PurePosixPath)
        self._other_attachments.remove(path)

    def _all_attachments(self) -> typing.Generator[typing.Tuple[pathlib.PurePath, typing.IO], None, None]:
        """ Get all attachments as open file objects

        :return: A generator producing a tuple of (path, file-object)
        """
        if self._zip_wrapper:
            with self._zip_wrapper as zip_file:
                for name in zip_file.namelist():
                    if not name.endswith('/'):
                        for src in self._other_attachments:
                            if name.startswith(str(src)):
                                with zip_file.open(name) as f:
                                    yield pathlib.PurePosixPath(name), f

                                break

        else:
            for src in self._other_attachments:
                path = self._base / src
                if path.is_file():
                    with path.open('rb') as f:
                        yield src, f

                elif path.is_dir():
                    for sub_path in path.glob('**/*'):
                        if sub_path.is_file():
                            with sub_path.open('rb') as f:
                                yield sub_path.relative_to(self._base), f

    # Attachments

    # noinspection PyShadowingBuiltins
    def _has_attachments(self, id: str = None) -> bool:
        """ Check if bundle has a non-empty attachment

        :param id: `id` of attachment to check
        :return: True if attachment exists and is not empty
        """
        if self._base:
            if self._other_attachments:
                return True

            files = self._all_files() if id is None else self._get_files(id)
            for file in files:
                if file.has_attachment_content():
                    return True

        return False

    # Defaults

    @staticmethod
    def _use_lxml(use_lxml: typing.Optional[bool]):
        if use_lxml is None:
            return has_lxml
        elif use_lxml and not has_lxml:
            raise LxmlMissingError("To use lxml, install the momotor-bundles package "
                                   "with the lxml option: momotor-bundles[lxml]")
        return use_lxml

    # Reading

    @classmethod
    def __get_parser(cls, *, use_lxml: bool, validate_xml: typing.Optional[bool], location_base: str) \
            -> XmlBundleParser:
        if validate_xml is None:
            validate_xml = True

        config = BundleParserConfig(
            fail_on_unknown_properties=validate_xml
        )

        if cls._use_lxml(use_lxml):
            from .parsers.handlers.lxml import LxmlBundleEventHandler as EventHandler
            config.validation_schema_path = SCHEMA_FILE_PATH if validate_xml else None
            config.process_xinclude = True
            config.process_xslt = True

        else:
            from .parsers.handlers.xml import XmlBundleEventHandler as EventHandler

        return XmlBundleParser(
            config=config,
            handler=EventHandler,
            expected_root_qname=cls.get_root_qname()
        )

    @classmethod
    def _from_io(cls, io: typing.BinaryIO, *,
                 use_lxml: bool = None, validate_xml: bool = None,
                 location_base: str = None) -> CT:

        parser = cls.__get_parser(
            use_lxml=use_lxml,
            validate_xml=validate_xml,
            location_base=location_base
        )

        try:
            return parser.parse(io, cls.get_node_type())

        except BundleError:
            raise

        except (ParserError, ValidationError) as e:
            raise BundleFormatError(str(e))

        except Exception as e:
            raise BundleLoadError(str(e))

    @classmethod
    def from_file_factory(cls: typing.Type[BT], path: typing.Union[str, pathlib.Path], *,
                          xml_name: str = None, use_lxml: bool = None, validate_xml: bool = None,
                          location_base: typing.Union[str, pathlib.Path] = None) -> BT:
        """Read bundle from a local file or directory.

        Make sure to call :py:meth:`~momotor.bundles.Bundle.close` either explicitly or using
        :py:func:`contextlib.closing` when done with the bundle to release all resources

        :param path: Either a file or directory.
                     When it is a file, it can be an XML file or a zip file.
                     When it is a directory, that directory should contain a <bundle>.xml file
        :param xml_name: XML file name if not the default (for directory and zip paths)
        :param use_lxml: Force (``True``) or prevent (``False``) use of :py:mod:`lxml` library.
                         If ``None``, auto-detects :py:mod:`lxml` availability
        :param validate_xml: Enable (``True``) or disable (``False``) XML validation.
                             If ``None``, uses default setting, which is to enable validation
        :param location_base: Location used in error messages
        :return: the bundle
        """
        path = pathlib.Path(path)
        xml_type = cls.get_root_tag()
        if zipfile.is_zipfile(path):
            base = ''
            zip_wrapper = ZipWrapper(path=path)
            if not xml_name:
                xml_name = cls.get_default_xml_name()

            try:
                with zip_wrapper as zip_file, zip_file.open(xml_name) as zip_io:
                    root = cls._from_io(zip_io, use_lxml=use_lxml, validate_xml=validate_xml,
                                        location_base=f"{location_base or path}:{xml_name}")

            except KeyError:
                raise InvalidBundle("A {} bundle should contain a {} file in the root".format(xml_type, xml_name))

        else:
            zip_wrapper = None
            if path.is_dir():
                if not xml_name:
                    xml_name = cls.get_default_xml_name()

                base, path = path, path / xml_name
                if not path.exists():
                    raise InvalidBundle("A {} bundle should contain a {} file in the root".format(xml_type, xml_name))
            else:
                base = path.parent

            with open(path, 'rb') as io_:
                root = cls._from_io(io_, use_lxml=use_lxml, validate_xml=validate_xml,
                                    location_base=str(location_base or path))

        # noinspection PyProtectedMember
        return cls(base, zip_wrapper)._create_from_node(root)

    @classmethod
    def from_bytes_factory(cls: typing.Type[BT], data: typing.Union[bytes, memoryview], *,
                           xml_name: str = None, use_lxml: bool = None, validate_xml: bool = None,
                           location_base: typing.Union[str, pathlib.Path] = None) -> BT:
        """Read bundle from memory, either a :py:class:`bytes` or :py:class:`memoryview` object.

        Make sure to call :py:meth:`~momotor.bundles.Bundle.close` either explicitly or using
        :py:func:`contextlib.closing` when done with the bundle to release all resources

        :param data: Bundle data
        :param xml_name: XML file name if not the default
        :param use_lxml: Force (``True``) or prevent (``False``) use of :py:mod:`lxml` library.
                         If ``None``, auto-detects :py:mod:`lxml` availability
        :param validate_xml: Enable (``True``) or disable (``False``) XML validation.
                             If ``None``, uses default setting, which is to enable validation
        :param location_base: Location used in error messages
        :return: the bundle
        """
        xml_type = cls.get_root_tag()
        if not xml_name:
            xml_name = cls.get_default_xml_name()

        data_io = BytesIO(data)
        if zipfile.is_zipfile(data_io):
            zip_wrapper = ZipWrapper(content=data)
            try:
                with zip_wrapper as zip_file, zip_file.open(xml_name) as xml_io:
                    root = cls._from_io(xml_io, use_lxml=use_lxml, validate_xml=validate_xml,
                                        location_base=f"{location_base or '<zip file>'}/{xml_name}")

            except KeyError:
                raise InvalidBundle("A {} bundle should contain a {} file in the root".format(xml_type, xml_name))

        else:
            zip_wrapper = None
            data_io.seek(0)
            root = cls._from_io(data_io, use_lxml=use_lxml, validate_xml=validate_xml,
                                location_base=str(location_base) if location_base else None)

        # noinspection PyProtectedMember
        return cls(None, zip_wrapper)._create_from_node(root)

    # Writing

    def __get_serializer(self, *, use_lxml: bool = None, pretty_xml: bool = False, encoding='utf-8') \
            -> XmlBundleSerializer:

        if self._use_lxml(use_lxml):
            from .serializers.writers.lxml import LxmlBundleEventWriter as EventWriter
        else:
            from .serializers.writers.xml import XmlBundleEventWriter as EventWriter

        return XmlBundleSerializer(
            pretty_print=pretty_xml,
            encoding=encoding,
            writer=EventWriter,
        )

    def _to_xml(self, *, use_lxml: bool = None, pretty_xml: bool = False, encoding='utf-8') -> bytes:
        """ Export the bundle to an XML document

        :param use_lxml: Force (``True``) or prevent (``False``) use of :py:mod:`lxml` library.
                         If ``None``, auto-detects :py:mod:`lxml` availability
        :param pretty_xml: Better readable xml document
        :return: utf-8 encoded XML document
        """
        return self.__get_serializer(
            use_lxml=use_lxml,
            pretty_xml=pretty_xml,
            encoding=encoding
        ).render(
            self._construct_node(),
            ns_map={
                None: __NAMESPACE__
            }
        ).encode(encoding)

    # noinspection PyShadowingBuiltins
    def to_buffer(self, buffer: typing.BinaryIO, *,
                  xml_name: str = None,
                  compression: int = zipfile.ZIP_DEFLATED, compresslevel: int = None,
                  zip: bool = False, use_lxml: bool = None, pretty_xml: bool = False) -> BundleFormat:
        """ Export the bundle to a :py:class:`~typing.BinaryIO` buffer and close it.

        If `zip` is False and the bundle does not contain any attachments, will generate a plain XML bundle, otherwise
        it will generate a zip compressed bundle with the bundle XML file located in the root of the zip file and
        named `xml_name`

        :param buffer: buffer to export into
        :param xml_name: name of the xml document (only used when generating a zipped bundle)
        :param compression: compression mode, see :py:class:`zipfile.ZipFile` for possible values.
            (Defaults to `ZIP_DEFLATE`, only used when generating a zipped bundle)
        :param compresslevel: compression level, see :py:class:`zipfile.ZipFile` for possible values.
            (Python 3.7+ only, ignored on Python 3.6, only used when generating a zipped bundle)
        :param zip: Force zip format
        :param use_lxml: Force (``True``) or prevent (``False``) use of :py:mod:`lxml` library.
                         If ``None``, auto-detects :py:mod:`lxml` availability
        :param pretty_xml: Better readable xml document
        :return: created format, either :py:class:`~momotor.bundles.const.BundleFormat`\ ``.XML``
            or :py:class:`~momotor.bundles.const.BundleFormat`\ ``.ZIP``
        """

        with contextlib.closing(self):
            if not self._has_attachments() and not zip:
                buffer.write(self._to_xml(use_lxml=use_lxml, pretty_xml=pretty_xml))
                return BundleFormat.XML

            compression_args = {
                'compression': compression
            }
            if PY37:
                compression_args['compresslevel'] = compresslevel

            with zipfile.ZipFile(buffer, mode='w', **compression_args) as zip_file:
                for file in self._all_files():
                    if file.src:
                        size, date_time = file.file_info()

                        zinfo = zipfile.ZipInfo(str(file.src), date_time)
                        zinfo.compress_type = compression
                        if PY37:
                            zinfo._compresslevel = compresslevel
                        zinfo.file_size = size

                        with file.open() as src, zip_file.open(zinfo, 'w') as dest:
                            shutil.copyfileobj(src, dest)

                for src_path, src in self._all_attachments():
                    with zip_file.open(str(src_path), 'w') as dest:
                        shutil.copyfileobj(src, dest)

                if not xml_name:
                    xml_name = self.get_default_xml_name()

                # noinspection PyTypeChecker
                zip_file.writestr(xml_name, self._to_xml(use_lxml=use_lxml, pretty_xml=pretty_xml))

            return BundleFormat.ZIP

    # noinspection PyShadowingBuiltins
    def to_file(self, fd_or_path: typing.Union[int, str, pathlib.Path], *,
                xml_name: str = None,
                compression: int = zipfile.ZIP_DEFLATED, compresslevel: int = None,
                zip: bool = False, use_lxml: bool = None, pretty_xml: bool = False) -> BundleFormat:
        """
        Export the bundle to a file and close it.

        If `zip` is False and the bundle does not contain any attachments, will generate a plain XML bundle, otherwise
        it will generate a zip compressed bundle with the bundle XML file located in the root of the zip file and
        named `xml_name`

        :param fd_or_path: either an open file descriptor, or a path. The file descriptor will be closed
        :param xml_name: name of the xml document (only used when generating a zipped bundle)
        :param compression: compression mode, see :py:class:`zipfile.ZipFile` for possible values.
            (Defaults to `ZIP_DEFLATE`, only used when generating a zipped bundle)
        :param compresslevel: compression level, see :py:class:`zipfile.ZipFile` for possible values.
            (Python 3.7+ only, ignored on Python 3.6, only used when generating a zipped bundle)
        :param zip: Force zip format
        :param use_lxml: Force (``True``) or prevent (``False``) use of :py:mod:`lxml` library.
                         If ``None``, auto-detects :py:mod:`lxml` availability
        :param pretty_xml: Better readable xml document
        :return: created format, either :py:class:`~momotor.bundles.const.BundleFormat`\ ``.XML``
            or :py:class:`~momotor.bundles.const.BundleFormat`\ ``.ZIP``
        """

        if isinstance(fd_or_path, int):
            opener = io_open(fd_or_path, 'w+b')
        else:
            opener = pathlib.Path(fd_or_path).open('w+b')

        with opener as f:
            return self.to_buffer(f, xml_name=xml_name, compression=compression, compresslevel=compresslevel,
                                  zip=zip, use_lxml=use_lxml, pretty_xml=pretty_xml)

    def to_directory(self, path: pathlib.Path, *,
                     xml_name: str = None, dir_mode: int = 0o700,
                     use_lxml: bool = None, pretty_xml: bool = False) -> None:
        """
        Export the bundle to a directory.

        Writes the XML file `xml_name` to the given `path`, and all the bundle's attachments in the right
        location relative to the XML file.

        :param path: path of the directory. Will be created if it does not exist
        :param xml_name: name of the xml document
        :param dir_mode: the mode bits (defaults to 0o700, making the directory only accessible to the current user)
        :param use_lxml: Force (``True``) or prevent (``False``) use of :py:mod:`lxml` library.
                         If ``None``, auto-detects :py:mod:`lxml` availability
        :param pretty_xml: Better readable xml document
        """
        # TODO mkdir path

        with contextlib.closing(self):
            for file in self._all_files():
                if file.src:
                    dest_file = path / file.src
                    dest_file.parent.mkdir(dir_mode, parents=True, exist_ok=True)
                    with file.open() as src, dest_file.open('wb') as dest:
                        shutil.copyfileobj(src, dest)

            for src_path, src in self._all_attachments():
                dest_file = path / src_path
                dest_file.parent.mkdir(dir_mode, parents=True, exist_ok=True)
                with dest_file.open('wb') as dest:
                    shutil.copyfileobj(src, dest)

            if not xml_name:
                xml_name = self.get_default_xml_name()

            (path / xml_name).write_bytes(
                self._to_xml(use_lxml=use_lxml, pretty_xml=pretty_xml)
            )
