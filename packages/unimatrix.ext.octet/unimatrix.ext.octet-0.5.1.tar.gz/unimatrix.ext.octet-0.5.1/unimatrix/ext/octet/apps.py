# pylint: disable=W0107
"""Declares :class:`ApplicationConfig`."""
import ioc
import unimatrix.ext.crypto as crypto
from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .lib.blobencrypter import BlobEncrypter
from . import const
from . import domain
from . import services as svc


class ApplicationConfig(AppConfig):
    """Configures the :mod:`unimatrix.ext.octet` package."""
    name = 'unimatrix.ext.octet'
    label = 'octet'

    def ready(self):
        """Invoked when the Django app registry has loaded all
        apps.
        """
        ioc.provide('BlobEncryptionKeyService', svc.BlobEncryptionKeyService())
        ioc.provide('BlobFactory', domain.BlobFactory())

        # Setup the master key using the cryptographic backend specified by the
        # BLOB_MASTER_KEY_BACKEND setting.
        if not getattr(settings, 'BLOB_MASTER_KEY_BACKEND', None):
            raise ImproperlyConfigured(
                'BLOB_MASTER_KEY_BACKEND is a required setting.')

        try:
            backend = crypto.backends[settings.BLOB_MASTER_KEY_BACKEND]
        except LookupError:
            raise ImproperlyConfigured(
                f"Backend '{settings.BLOB_MASTER_KEY_BACKEND}' is not defined "
                "in settings.CRYPTO_BACKENDS. Make sure that unimatrix.ext.oct"
                "tet is listed below and after unimatrix.ext.crypto in the Dja"
                "ngo INSTALLED_APPS setting."
            )

        required_capabilities = [
            'encrypt',
            'encrypt:async',
            'decrypt',
            'decrypt:async'
        ]
        if not backend.has_capabilities(required_capabilities):
            raise ImproperlyConfigured("Unsuitable backend.")
        ioc.provide('BlobEncryptionMasterKey', backend.symmetric())

        # Configure the encryption backend for blobs.
        crypto.backends.add(const.CRYPTO_BACKEND_KEY, BlobEncrypter())
        ioc.provide('BlobEncryptionBackend',
            crypto.backends[const.CRYPTO_BACKEND_KEY])
