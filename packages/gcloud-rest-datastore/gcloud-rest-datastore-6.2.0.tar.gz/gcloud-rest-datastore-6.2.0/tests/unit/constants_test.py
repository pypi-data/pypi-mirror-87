from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
import gcloud.rest.datastore.constants as constants  # pylint: disable=unused-import


def test_importable():
    assert True
