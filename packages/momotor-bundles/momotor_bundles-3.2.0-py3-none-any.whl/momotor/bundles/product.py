import typing
from pathlib import PurePosixPath

import momotor.bundles
from momotor.bundles.base import Bundle
from momotor.bundles.binding import Product as ProductRootType
from momotor.bundles.const import BundleCategory
from momotor.bundles.elements.base import IdMixin
from momotor.bundles.elements.files import File, FilesMixin
from momotor.bundles.elements.options import Option, OptionsMixin
from momotor.bundles.elements.properties import Property, PropertiesMixin

__all__ = ['ProductBundle']


class ProductBundle(Bundle[ProductRootType], IdMixin, OptionsMixin, FilesMixin, PropertiesMixin):
    """ A product bundle. This implements the interface to create and access Momotor product files
    """
    # noinspection PyShadowingBuiltins
    def create(self, *,
               id: str = None,
               options: typing.List[Option] = None,
               files: typing.List[File] = None,
               properties: typing.List[Property] = None) -> "ProductBundle":
        """ Set all attributes for this ProductBundle

        Usage:

        .. code-block:: python

           product = ProductBundle(...).create(id, options, files)

        :param id: `id` of the bundle (optional)
        :param options: list of options (optional)
        :param files: list of files (optional)
        :param properties: list of properties (optional)
        :return: self
        """
        # TODO meta
        self.id = id
        self.options = options
        self.files = files
        self.properties = properties
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) \
            -> typing.NoReturn:
        """ not implemented """
        raise NotImplementedError

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: ProductRootType) -> "ProductBundle":
        self._check_node_type(node)

        return self.create(
            id=node.id,
            options=self._collect_options(node, []),
            files=self._collect_files(node, []),
            properties=self._collect_properties(node),
        )

    def _construct_node(self) -> ProductRootType:
        # noinspection PyArgumentList
        return self.get_node_type()(
            id=self.id,
            options=self._construct_options_nodes(self.options),
            files=self._construct_files_nodes(self.files),
            properties=self._construct_properties_nodes(self.properties),
        )

    @staticmethod
    def get_node_type() -> typing.Type[ProductRootType]:
        return ProductRootType

    @staticmethod
    def get_default_xml_name():
        """ Get the default XML file name

        :return: 'product.xml'
        """
        return 'product.xml'

    @staticmethod
    def get_category():
        """ Get the category for this bundle

        :return: :py:const:`BundleCategory.PRODUCT`
        """
        return BundleCategory.PRODUCT


# Extend the docstring with the generic documentation of Bundle
ProductBundle.__doc__ += "\n".join(Bundle.__doc__.split("\n")[1:])
