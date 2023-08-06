# pylint: skip-file
import os

import ioc
import unimatrix.lib.test
from django.test import TestCase

from ..blobencrypter import BlobEncrypter


class BlobEncrypterTestCase(TestCase):

    @ioc.inject('svc', 'BlobEncryptionKeyService')
    def setUp(self, svc):
        super().setUp()
        svc.generate()
        self.encrypter = BlobEncrypter()
        self.key = self.encrypter.symmetric()

    def test_encrypt_decrypt(self):
        pt = os.urandom(16)
        ct = self.key.encrypt(pt)
        self.assertEqual(
            pt, self.encrypter.decrypt(ct, self.encrypter.get_key_id()))
