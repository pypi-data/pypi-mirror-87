# pylint: skip-file
import os
import unittest

import unimatrix.lib.test

from . import test_local
from ..azure import StorageBackend


@unimatrix.lib.test.system.scope('remote-storage')
@unittest.skipIf(not os.getenv('AZURE_STORAGE_CONNECTION_STRING'),
    "AZURE_STORAGE_CONNECTION_STRING is not defined.")
@unittest.skipIf(not os.getenv('AZURE_STORAGE_CONTAINER_NAME'),
    "AZURE_STORAGE_CONTAINER_NAME is not defined.")
class AzureBlobStorageBackendTestCase(test_local.LocalDiskBackendTestCase):
    backend_class = StorageBackend
    capabilities = []

    def get_backend_kwargs(self):
        return {
            'base_path': os.path.join('tmp', bytes.hex(os.urandom(16)))
        }

    def test_update_labels(self):
        labels = {}
        self.backend.update_labels(labels)
        self.assertIn('azure.microsoft.com/blob-storage-account', labels)
        self.assertIn('azure.microsoft.com/blob-storage-container', labels)
