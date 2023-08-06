import typing
from pathlib import PurePosixPath

import momotor.bundles
from momotor.bundles.base import Bundle
from momotor.bundles.binding import Config as ConfigRootType
from momotor.bundles.const import BundleCategory
from momotor.bundles.elements.base import IdMixin
from momotor.bundles.elements.files import File, FilesMixin
from momotor.bundles.elements.options import Option, OptionsMixin

__all__ = ['ConfigBundle']


class ConfigBundle(Bundle[ConfigRootType], IdMixin, OptionsMixin, FilesMixin):
    """ A config bundle. This implements the interface to create and access Momotor configuration files
    """
    # noinspection PyShadowingBuiltins
    def create(self, *,
               id: str = None,
               options: typing.List[Option] = None,
               files: typing.List[File] = None) -> "ConfigBundle":
        """ Set all attributes for this ConfigBundle

        Usage:

        .. code-block:: python

           config = ConfigBundle(...).create(id, options, files)

        :param id: `id` of the bundle (optional)
        :param options: list of options (optional)
        :param files: list of files (optional)
        :return: self
        """
        # TODO meta
        self.id = id
        self.options = options
        self.files = files
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) \
            -> typing.NoReturn:
        """ not implemented """
        raise NotImplementedError

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: ConfigRootType) -> "ConfigBundle":
        self._check_node_type(node)

        return self.create(
            id=node.id,
            options=self._collect_options(node, []),
            files=self._collect_files(node, [])
        )

    def _construct_node(self) -> ConfigRootType:
        # noinspection PyArgumentList
        return self.get_node_type()(
            id=self.id,
            options=self._construct_options_nodes(self.options),
            files=self._construct_files_nodes(self.files),
        )

    @staticmethod
    def get_node_type() -> typing.Type[ConfigRootType]:
        return ConfigRootType

    @staticmethod
    def get_default_xml_name() -> str:
        """ Get the default XML file name

        :return: 'config.xml'
        """
        return 'config.xml'

    @staticmethod
    def get_category() -> BundleCategory:
        """ Get the category for this bundle

        :return: :py:const:`BundleCategory.CONFIG`
        """
        return BundleCategory.CONFIG


# Extend the docstring with the generic documentation of Bundle
ConfigBundle.__doc__ += "\n".join(Bundle.__doc__.split("\n")[1:])
