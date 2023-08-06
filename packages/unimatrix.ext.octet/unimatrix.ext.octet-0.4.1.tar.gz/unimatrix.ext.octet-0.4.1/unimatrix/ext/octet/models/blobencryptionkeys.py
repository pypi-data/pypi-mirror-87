"""Declares :class:`BlobEncryptionKey`."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class BlobEncryptionKey(models.Model):
    """Persists an encryption key for blobs, encrypted with the master key."""

    #: The ciphertext of the encryption key.
    ct = models.BinaryField(
        verbose_name=_("Ciphertext"),
        blank=False,
        null=False,
        db_column='ct'
    )

    #: Annotations set by the encryption backend.
    annotations = models.JSONField(
        verbose_name=_("Annotations"),
        blank=False,
        null=False,
        default=dict,
        db_column='annotations'
    )

    __module__ = 'unimatrix.ext.octet.models'

    class Meta: # pylint: disable=C0115,R0903
        app_label = 'octet'
        db_table = 'blobencryptionkeys'
        default_permissions = []
        ordering = ['-pk']
        verbose_name = _("Blob Encryption Key")
        verbose_name_plural = _("Blob Encryption Keys")
