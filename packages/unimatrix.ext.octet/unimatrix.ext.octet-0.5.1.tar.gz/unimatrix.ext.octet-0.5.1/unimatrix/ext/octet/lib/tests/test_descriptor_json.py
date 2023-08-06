# pylint: skip-file
import json
import os
import tempfile
import unittest

import unimatrix.lib.test

from ..backends.local import StorageBackend


@unimatrix.lib.test.integration
class DescriptorJsonTestCase(unittest.TestCase):
    """Tests if the :class:`~unimatrix.ext.octet.lib.descriptor.Descriptor`
    is compatible with :func:`json.load` and :func:`json.dump`.
    """

    def setUp(self):
        self.backend = StorageBackend(base_path=tempfile.gettempdir())

    def test_json_dump_w(self):
        dst = bytes.hex(os.urandom(16))
        with self.backend.open(dst, 'w') as f:
            json.dump({'foo': 'bar'}, f)

        with self.backend.open(dst) as f:
            data = f.read()
            obj = json.loads(data)
            self.assertIsInstance(obj, dict)
            self.assertIn('foo', obj)
            self.assertEqual(obj.get('foo'), 'bar')

    def test_json_dump_w_load(self):
        dst = bytes.hex(os.urandom(16))
        with self.backend.open(dst, 'w') as f:
            json.dump({'foo': 'bar'}, f)

        with self.backend.open(dst) as f:
            obj = json.load(f)
            self.assertIsInstance(obj, dict)
            self.assertIn('foo', obj)
            self.assertEqual(obj.get('foo'), 'bar')
