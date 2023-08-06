"""Declares :class:`AbstractBlobRepository`."""
import abc
import hashlib
import os

import ioc


class AbstractBlobRepository(metaclass=abc.ABCMeta):
    """Provides an interface to persist blobs used as input for jobs (environment,
    arguments, secrets and files).
    """
    storage = ioc.class_property('octet.BlobStorage')
    DoesNotExist = abc.abstractproperty()
    model = abc.abstractproperty()

    @classmethod
    def class_factory(cls, impl_class):
        """Create a new :class:`AbstractBlobRepository` subclass using the
        provided implementation class `impl_class`.
        """
        return type('BlobRepository', (impl_class, cls), {})

    @classmethod
    def new(cls, impl_class, *args, **kwargs):
        """Create a new instance with the specified implementation class."""
        return cls.class_factory(impl_class)(*args, **kwargs)

    def __init__(self):
        self._in_transaction = False

    @ioc.inject('factory', 'BlobFactory')
    def add(self, f, content_type, factory, encrypt=False):
        """Check if a :class:`~unimatrix.ext.octet.models.Blob` instance exists
        for given file-like object `f`. If one does not exist, create it. Return
        an instance of the model specified by :attr:`model_class`.
        """
        f.seek(0)
        checksum = self.calculate_checksum(f)
        created = False
        if not self.exists(checksum):
            blob = factory.new(self.model, f, content_type, encrypt=encrypt)
            created = True
        else:
            blob = self.lookup_dao(checksum)
        if created:
            labels = {}
            self.storage.push(f.name, blob.checksum)
            self.storage.label(labels)
            blob.setlabels(labels)
            self.persist_dao(blob)
            blob.fd = f
            blob.fd.seek(0)
        return blob

    async def async_lookup_dao(self, checksum):
        """ORM-specific implementation to lookup the Data Access
        Object (DAO) asynchronously.
        """
        return self.lookup_dao(checksum)

    @abc.abstractmethod
    def lookup_dao(self, checksum):
        """ORM-specific implementation to lookup the Data Access
        Object (DAO).
        """
        raise NotImplementedError("Subclasses must override this method.")

    @abc.abstractmethod
    def persist_dao(self, dao):
        """ORM-specific implementation to lookup the Data Access
        Object (DAO).
        """
        raise NotImplementedError("Subclasses must override this method.")

    @abc.abstractmethod
    def exists(self, checksum):
        """Return a boolean indicating if a file with the given checksum
        exists.
        """
        raise NotImplementedError("Subclasses must override this method.")

    @ioc.inject('decrypter', 'BlobEncryptionBackend')
    def read(self, checksum, decrypter, decrypt=True):
        """Reads the full content of the :class:`Blob` identified by
        `checksum`.
        """
        blob = self.lookup_dao(checksum)
        with self.storage.open(checksum, 'rb') as f:
            buf = f.read()
            if blob.is_encrypted() and decrypt:
                ct = blob.get_ciphertext(buf)
                buf = decrypter.decrypt(ct, blob.get_key_id())

        return buf

    async def async_slice(self, checksum, length, offset=0):
        """Return a byte-sequence holding the slice specified by `length`
        and `offset`.
        """
        blob = await self.async_lookup_dao(checksum)
        if blob.is_encrypted():
            raise TypeError("Encrypted blobs can not be sliced.")
        return await self.storage.async_slice(checksum, length, offset)

    @staticmethod
    def calculate_checksum(f):
        """Calculate a SHA-256 hash for file-like object `f`."""
        h = hashlib.sha256()
        p = f.tell()
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            h.update(chunk)
        f.seek(p)
        return h.hexdigest()

    @staticmethod
    def get_filesize(fp):
        """Return an unsigned integer indicating the size of file `fp`."""
        return os.path.getsize(fp)

    def as_context(self, *args, **kwargs):
        """Hook that is executed when a transaction is started."""
        repo = type(self)()
        repo.setup_context(*args, **kwargs)
        return repo

    def setup_context(self, *args, **kwargs):
        """Hook to setup the context."""
        pass

    def teardown_context(self, *args, **kwargs):
        """Hook to teardown the context."""
        pass

    def __enter__(self):
        if self._in_transaction:
            raise RuntimeError("Nested transactions are not supported.")
        return self

    def __exit__(self, cls, exc, tb):
        pass
