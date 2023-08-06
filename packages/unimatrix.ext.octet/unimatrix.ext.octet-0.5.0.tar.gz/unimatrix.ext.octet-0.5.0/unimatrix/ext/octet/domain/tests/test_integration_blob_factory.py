# pylint: skip-file
import os
import tempfile

import ioc
import unimatrix.lib.test
from django.test import TestCase

from ...models import Blob
from ..blobfactory import BlobFactory


class BlobFactoryTestCase(TestCase):

    @ioc.inject('svc', 'BlobEncryptionKeyService')
    def setUp(self, svc):
        self.factory = BlobFactory()
        self.model = Blob
        svc.generate()

    def test_new_plaintext(self):
        pt = b'Hello world!'
        with tempfile.NamedTemporaryFile('w+b') as f:
            f.write(pt)
            blob = self.factory.new(self.model, f, "text/plain")
            f.seek(0)
            self.assertEqual(pt, f.read())

    def test_new_plaintext_encrypt(self):
        pt = b'Hello world!'
        with tempfile.NamedTemporaryFile('w+b') as f:
            f.write(pt)
            blob = self.factory.new(self.model, f, "text/plain", encrypt=True)
            f.seek(0)
            self.assertNotEqual(pt, f.read())

    @ioc.inject('decrypter', 'BlobEncryptionBackend')
    def test_can_decrypt(self, decrypter):
        pt = os.urandom(16)
        with tempfile.NamedTemporaryFile('w+b') as f:
            f.write(pt)
            blob = self.factory.new(self.model, f, "text/plain", encrypt=True)
            f.seek(0)
            self.assertNotEqual(pt, f.read())

            f.seek(0)
            ct = blob.get_ciphertext(f.read())
            self.assertEqual(pt, decrypter.decrypt(ct, None))
