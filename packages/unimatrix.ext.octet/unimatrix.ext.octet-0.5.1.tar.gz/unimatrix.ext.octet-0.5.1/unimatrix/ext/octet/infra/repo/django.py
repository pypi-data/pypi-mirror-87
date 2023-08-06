"""Declares :class:`BlobRepository`."""
from django.apps import apps
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist


class DjangoBackend:
    """Provides an interface to persist blobs used as input for jobs (environment,
    arguments, secrets and files).
    """
    capabilities = ['encrypt']
    model_class = 'octet.Blob'
    DoesNotExist = ObjectDoesNotExist

    @property
    def model(self):
        """Returns the model class used by this repository."""
        return apps.get_model(self.model_class)

    @transaction.atomic
    def add(self, *args, **kwargs):
        """Check if a :class:`~unimatrix.ext.octet.models.Blob` instance exists
        for given file-like object `f`. If one does not exist, create it. Return
        an instance of the model specified by :attr:`model_class`.
        """
        return super().add(*args, **kwargs)

    def exists(self, checksum):
        """Return a boolean indicating if a file with the given checksum
        exists.
        """
        return self.model.objects.filter(checksum=checksum).exists()

    def lookup_dao(self, checksum):
        """Django-specific implementation to lookup the Data Access
        Object (DAO).
        """
        return self.model.objects.get(checksum=checksum)

    def persist_dao(self, dao):
        """Django-specific implementation to lookup the Data Access
        Object (DAO).
        """
        return dao.save()
