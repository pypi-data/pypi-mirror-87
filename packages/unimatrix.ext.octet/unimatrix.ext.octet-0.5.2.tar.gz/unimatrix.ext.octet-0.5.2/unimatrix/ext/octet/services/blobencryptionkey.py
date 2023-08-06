"""Declares :class:`BlobEncryptionKeyService`."""
import ioc
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from django.apps import apps


class BlobEncryptionKeyService:
    """Provides an interface to generate and rotate the cryptographic keys used
    to encrypt blobs.
    """
    bit_length = 256

    @property
    def factory(self):
        """Returns a factory object that can create new instances of
        :class:`~unimatrix.ext.octet.models.BlobEncryptionKey`.
        """
        return apps.get_model('octet', 'BlobEncryptionKey').objects

    @ioc.inject('key', 'BlobEncryptionMasterKey')
    def generate(self, key):
        """Generates a new encryption key."""
        if self.factory.exists():
            return False
        ct = key.encrypt(AESGCM.generate_key(bit_length=self.bit_length))
        self.factory.create(ct=bytes(ct), annotations=ct.annotations)
        return True
