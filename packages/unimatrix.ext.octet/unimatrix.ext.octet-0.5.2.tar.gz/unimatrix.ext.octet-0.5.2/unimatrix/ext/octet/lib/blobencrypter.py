"""Declares :class:`BlobEncrypter`."""
import ioc
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from unimatrix.ext.crypto.lib import aes
from unimatrix.ext.crypto.ciphertext import CipherText


NOT_INITIALIZED = object()


class BlobEncrypter:
    """Exposes an interface to encrypt blobs."""

    def __init__(self):
        self.__backend = NOT_INITIALIZED
        self.__key_id = None
        self.__keys = {}

    @ioc.inject('master', 'BlobEncryptionMasterKey')
    def decrypt(self, ct, key_id, master):
        """Decrypt `buf` using `key_id`."""
        key_id = key_id or self.__key_id
        if key_id not in self.__keys:
            dao = apps.get_model('octet', 'BlobEncryptionKey')\
                .objects.get(pk=key_id)
            encrypted_key = CipherText(dao.ct)
            encrypted_key.update_annotations(dao.annotations)
            self.__keys[key_id] = aes.Backend(master.decrypt(encrypted_key))\
                .symmetric()
        print("Decrypting with key id %s" % key_id)
        return self.__keys[key_id].decrypt(ct)

    def get_key_id(self):
        """Return an integer identifying the key that :class:`BlobEncrypter`
        currently uses to encrypt.
        """
        return self.__key_id

    @ioc.inject('master', 'BlobEncryptionMasterKey')
    def symmetric(self, master):
        """Return a symmetric key implementation to encrypt and decrypt
        blobs.
        """
        if self.__backend == NOT_INITIALIZED:
            dao = apps.get_model('octet', 'BlobEncryptionKey').objects.first()
            if dao is None:
                raise ImproperlyConfigured(
                    "No encryption keys were generated. Run manage.py blob "
                    "generate-key to ensure that there is a key to encrypt "
                    "blobs."
                )
            ct = CipherText(dao.ct)
            ct.update_annotations(dao.annotations)
            self.__key_id = dao.pk
            self.__backend = aes.Backend(master.decrypt(ct))

        print("Encrypting with key id %s" % self.__key_id)
        return self.__backend.symmetric()
