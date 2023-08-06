# pylint: skip-file
import hashlib
import io
import os
import tempfile

import ioc
import unimatrix.lib.test
from django.test import TestCase
from unimatrix.ext.crypto.ciphertext import CipherText

from unimatrix.ext.octet.lib.blobencrypter import BlobEncrypter
from unimatrix.ext.octet.models import Blob
from ..abstractblob import AbstractBlobRepository
from ..django import DjangoBackend
from ....lib.backends.local import LocalDiskBackend


@unimatrix.lib.test.integration
class BlobRepositoryTestCase(TestCase):

    @ioc.inject('svc', 'BlobEncryptionKeyService')
    def setUp(self, svc):
        self.blobs = AbstractBlobRepository.new(DjangoBackend)
        self.backend = LocalDiskBackend(base_path=tempfile.mkdtemp())

        ioc.provide('octet.BlobStorage', self.backend, force=True)
        ioc.provide('BlobEncryptionBackend', BlobEncrypter(), force=True)
        svc.generate()

    def test_calculate_checksum(self):
        h = hashlib.sha256()
        h.update(b'Hello world!')
        c1 = h.hexdigest()
        c2 = self.blobs.calculate_checksum(io.BytesIO(b"Hello world!"))
        self.assertEqual(c1, c2)

    def test_add(self):
        with tempfile.NamedTemporaryFile('w+b') as f:
            f.write(b"Hello world!")
            f.flush()

            self.blobs.add(f, "text/plain")

    def test_read(self):
        pt = os.urandom(16)
        with tempfile.NamedTemporaryFile('w+b') as f:
            f.write(pt)
            f.flush()

            blob = self.blobs.add(f, "text/plain")
            self.assertEqual(self.blobs.read(blob.checksum), pt)

    def test_add_encrypted(self):
        pt = os.urandom(16)
        with tempfile.NamedTemporaryFile('w+b') as f:
            f.write(pt)
            f.flush()

            self.blobs.add(f, "text/plain", encrypt=True)

    @ioc.inject('storage', 'octet.BlobStorage')
    @ioc.inject('decrypter', 'BlobEncryptionBackend')
    def test_read_encrypted_in_storage(self, storage, decrypter):
        key = decrypter.symmetric()
        pt = os.urandom(16)
        ct = key.encrypt(pt)
        self.assertEqual(key.decrypt(ct), pt)
        self.assertEqual(decrypter.decrypt(ct, None), pt)

    def test_read_encrypted(self):
        pt = os.urandom(16)
        with tempfile.NamedTemporaryFile('wb+') as f:
            f.write(pt)
            f.flush()

            blob = self.blobs.add(f, "text/plain", encrypt=True)
            self.assertEqual(self.blobs.read(blob.checksum), pt)
