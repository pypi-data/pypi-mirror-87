# pylint: disable=E0611
"""Declares :class:`BlobReference`."""
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from unimatrix.lib import timezone


class BlobReference(models.Model):
    """Maintains a reference to a :class:`Blob`."""
    OWNER_FIELD = None

    id = models.UUIDField(
        verbose_name=_("ID"),
        blank=False,
        null=False,
        default=uuid.uuid4,
        primary_key=True,
        db_column='id'
    )

    #: The :class:`~unimatrix.ext.octet.models.Blob` that is references.
    blob = models.ForeignKey(
        'octet.Blob',
        verbose_name=_("Blob"),
        blank=False,
        null=False,
        related_name='references',
        to_field='checksum',
        on_delete=models.PROTECT,
        db_column='checksum'
    )

    #: The Django model class that created the reference.
    owner = models.CharField(
        max_length=63,
        verbose_name=_("Owner"),
        blank=False,
        null=False,
        db_column='owner'
    )

    #: The date and time at which the reference was made, in milliseconds since
    #: the UNIX epoch.
    referenced = models.BigIntegerField(
        verbose_name=_("Referenced"),
        blank=False,
        null=False,
        default=timezone.now,
        db_column='referenced'
    )

    #: Mapping of key/value pairs providing extra context for this specific
    #: :class:`BlobReference`. All keys and values must be strings.
    labels = models.JSONField(
        verbose_name=_("Labels"),
        blank=False,
        null=False,
        default=dict,
        db_column='labels'
    )

    def setlabels(self, labels):
        """Sets the labels on the :class:`Blob` instance."""
        if isinstance(labels, str):
            labels = json.loads(labels)
        self.labels = labels

    def getlabels(self):
        """Return the labels specified for this :class:`Blob`."""
        labels = self.labels
        if isinstance(labels, str):
            labels = json.loads(labels)
        return labels

    __module__ = 'unimatrix.ext.octet.models'

    class Meta: # pylint: disable=C0115,R0903
        app_label = 'octet'
        db_table = 'blobreferences'
        default_permissions = []
        verbose_name = _("Blob Reference")
        verbose_name_plural = _("Blob References")
