"""Declares :class:`EncryptedBlob`."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from unimatrix.ext.crypto.ciphertext import CipherText

from .blobs import Blob


class EncryptedBlob(Blob):
    """A :class:`Blob` that is encrypted."""

    #: A reference to the encrypted :class:`~unimatrix.ext.octet.models.Blob`.
    blob = models.OneToOneField(
        Blob,
        verbose_name=_("Blob"),
        parent_link=True,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        primary_key=True,
        related_name='ciphertext',
        db_column='blob_id'
    )

    #: Specifies the encryption key that was used to encrypt the blob.
    using = models.ForeignKey(
        'octet.BlobEncryptionKey',
        verbose_name=_("Using"),
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        related_name='blobs',
        db_column='key_id'
    )

    annotations = models.JSONField(
        verbose_name=_("Annotations"),
        blank=False,
        null=False,
        default=dict,
        db_column='annotations'
    )

    def get_ciphertext(self, buf):
        """Return a :class:`~unimatrix.ext.crypto.CipherText` instance
        with the parameters used when encrypting this :class:`Blob`.
        """
        return CipherText(buf, self.annotations)

    __module__ = 'unimatrix.ext.octet.models'

    class Meta: # pylint: disable=C0115,R0903
        app_label = 'octet'
        db_table = 'encryptedblobs'
        default_permissions = []
        verbose_name = _("Encrypted Blob")
        verbose_name_plural = _("Encrypted Blobs")
