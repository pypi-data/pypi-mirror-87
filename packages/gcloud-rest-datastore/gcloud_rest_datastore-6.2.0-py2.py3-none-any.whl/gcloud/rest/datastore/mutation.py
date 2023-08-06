from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from builtins import object
from typing import Any
from typing import Dict
from typing import Optional

from gcloud.rest.datastore.key import Key


# https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects/commit#Mutation
class Mutation(object):
    # TODO: Use this Mutation class instead of datastore.make_mutation
    pass


# https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects/commit#MutationResult
class MutationResult(object):
    key_kind = Key

    def __init__(self, key               , version     ,
                 conflict_detected      )        :
        self.key = key
        self.version = version
        self.conflict_detected = conflict_detected

    def __eq__(self, other     )        :
        if not isinstance(other, MutationResult):
            return False

        return bool(self.key == other.key and self.version == other.version)

    def __repr__(self)       :
        return str(self.to_repr())

    @classmethod
    def from_repr(cls, data                )                    :
        if 'key' in data:
            key                = cls.key_kind.from_repr(data['key'])
        else:
            key = None
        version      = data['version']
        conflict_detected       = data.get('conflictDetected', False)
        return cls(key, version, conflict_detected)

    def to_repr(self)                  :
        data = {
            'version': self.version,
            'conflictDetected': self.conflict_detected
        }
        if self.key:
            data['key'] = self.key.to_repr()
        return data
