import enum
import time

__all__ = ['BundleCategory', 'BundleFormat', 'DEFAULT_TIME_STAMP']


class BundleFormat(enum.Enum):
    """ Bundle format constants """
    XML = 'xml'
    ZIP = 'zip'


class BundleCategory(enum.Enum):
    """ Bundle category constants """
    RECIPE = 'recipe'
    CONFIG = 'config'
    PRODUCT = 'product'
    RESULTS = 'results'
    TEST_RESULTS = 'test_results'


# Default time stamp, local time midnight January 1st, 1980
DEFAULT_TIME_STAMP = time.localtime(time.mktime((1980, 1, 1, 0, 0, 0, -1, -1, -1)))
