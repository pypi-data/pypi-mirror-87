# pylint: skip-file
import hashlib
import io
import os
import tempfile

import ioc

from ....lib.blobencrypter import BlobEncrypter
from ....lib.backends.local import LocalDiskBackend
from ..abstractblob import AbstractBlobRepository


class BlobRepositoryTestCase:
    __test__ = False
    backend_class = None

    @ioc.inject('svc', 'BlobEncryptionKeyService')
    def setUp(self, svc):
        self.blobs = AbstractBlobRepository.new(self.backend_class)
        self.backend = LocalDiskBackend(base_path=tempfile.mkdtemp())

        ioc.provide('octet.BlobStorage', self.backend, force=True)
        if 'encrypt' in self.backend.capabilities:
            ioc.provide('BlobEncryptionBackend', BlobEncrypter(), force=True)
            svc.generate()

    def get_context_kwargs(self):
        return {}

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

            with self.blobs.as_context(**self.get_context_kwargs()) as repo:
                repo.add(f, "text/plain")

    def test_read(self):
        pt = os.urandom(16)
        with tempfile.NamedTemporaryFile('w+b') as f:
            f.write(pt)
            f.flush()

            with self.blobs.as_context(**self.get_context_kwargs()) as repo:
                blob = repo.add(f, "text/plain")
                self.assertEqual(repo.read(blob.checksum), pt)

    def test_add_encrypted(self):
        if 'encrypt' not in self.backend.capabilities:
            self.skipTest("Encryption is not supported.")
        pt = os.urandom(16)
        with tempfile.NamedTemporaryFile('w+b') as f:
            f.write(pt)
            f.flush()

            self.blobs.add(f, "text/plain", encrypt=True)

    @ioc.inject('storage', 'octet.BlobStorage')
    @ioc.inject('decrypter', 'BlobEncryptionBackend')
    def test_read_encrypted_in_storage(self, storage, decrypter):
        if 'encrypt' not in self.backend.capabilities:
            self.skipTest("Encryption is not supported.")
        key = decrypter.symmetric()
        pt = os.urandom(16)
        ct = key.encrypt(pt)
        self.assertEqual(key.decrypt(ct), pt)
        self.assertEqual(decrypter.decrypt(ct, None), pt)

    def test_read_encrypted(self):
        if 'encrypt' not in self.backend.capabilities:
            self.skipTest("Encryption is not supported.")
        pt = os.urandom(16)
        with tempfile.NamedTemporaryFile('wb+') as f:
            f.write(pt)
            f.flush()

            blob = self.blobs.add(f, "text/plain", encrypt=True)
            self.assertEqual(self.blobs.read(blob.checksum), pt)
