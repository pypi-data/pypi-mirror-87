# pylint: skip-file
import json
import unittest

import unimatrix.lib.test

from ..blobs import Blob


@unimatrix.lib.test.unit
class BlobTestCase(unittest.TestCase):

    def test_set_labels_from_dict(self):
        blob = Blob()
        labels = {'foo': "1"}
        blob.setlabels(labels)
        self.assertIn('foo', blob.labels)
        self.assertEqual(blob.labels['foo'], "1")

    def test_get_labels_from_string(self):
        blob = Blob()
        blob.labels = {"foo": "1"}
        labels = blob.getlabels()
        self.assertIn('foo', labels)
        self.assertEqual(labels['foo'], "1")

    def test_set_labels_from_string(self):
        blob = Blob()
        blob.setlabels(json.dumps({"foo": "1"}))
        self.assertIn('foo', blob.labels)
        self.assertEqual(blob.labels['foo'], "1")

    def test_get_labels_from_string(self):
        blob = Blob()
        blob.labels = json.dumps({"foo": "1"})
        labels = blob.getlabels()
        self.assertIn('foo', labels)
        self.assertEqual(labels['foo'], "1")
