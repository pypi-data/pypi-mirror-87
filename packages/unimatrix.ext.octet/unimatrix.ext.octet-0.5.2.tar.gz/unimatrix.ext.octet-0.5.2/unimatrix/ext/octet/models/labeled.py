# pylint: disable=E0611
# pragma: no cover
"""Declares :class:`Labeled`."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Labeled(models.Model):
    """Base class for objects that can be labeled."""

    #: Mapping of key/value pairs providing extra context for this specific
    #: :class:`Blob`. All keys and values must be strings.
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

    class Meta: # pylint: disable=C0115,R0903
        abstract = True
        default_permissions = []
