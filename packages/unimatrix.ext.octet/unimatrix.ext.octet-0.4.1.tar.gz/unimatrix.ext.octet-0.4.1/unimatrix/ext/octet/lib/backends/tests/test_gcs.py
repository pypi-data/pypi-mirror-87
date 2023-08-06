# pylint: skip-file
import os
import unittest

import unimatrix.lib.test

from . import test_local
from ..gcs import StorageBackend


@unimatrix.lib.test.system.scope('remote-storage')
@unittest.skipIf(not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
    "GOOGLE_APPLICATION_CREDENTIALS not defined")
@unittest.skipIf(not os.getenv('GOOGLE_CLOUD_PROJECT'),
    "GOOGLE_CLOUD_PROJECT not defined")
@unittest.skipIf(not os.getenv('GOOGLE_GCS_BUCKET'),
    "GOOGLE_GCS_BUCKET not defined")
class GoogleCloudStorageBackendTestCase(test_local.LocalDiskBackendTestCase):
    backend_class = StorageBackend
    capabilities = ['unlink']

    def get_backend_kwargs(self):
        return {
            'base_path': os.path.join('tmp', bytes.hex(os.urandom(16)))
        }

    def test_update_labels(self):
        labels = {}
        self.backend.update_labels(labels)
        self.assertIn('cloud.google.com/project', labels)
        self.assertIn('storage.googleapis.com/bucket', labels)
