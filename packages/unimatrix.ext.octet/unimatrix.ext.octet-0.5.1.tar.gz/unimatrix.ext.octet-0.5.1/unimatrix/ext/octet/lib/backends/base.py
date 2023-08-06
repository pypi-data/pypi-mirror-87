"""Declares :class:`BaseStorageBackend`."""
import abc
import os
import tempfile

from aiofile import AIOFile

from ..asyncdescriptor import AsyncDescriptor
from ..descriptor import Descriptor


class BaseStorageBackend(metaclass=abc.ABCMeta):
    """The base class for all storage backends.

    Args:
        base_path (str): the base path from where the storage backend
            reads and writes files.

    .. warning::
        The constructor should not be overridden.
    """
    capabilities = []
    descriptor_class = Descriptor
    async_descriptor_class = AsyncDescriptor
    kind = abc.abstractproperty()
    write_modes = ['w', 'wt', 'wb']
    read_modes = ['r', 'rt', 'rb']

    @property
    def base_path(self):
        """Return the base path of the storage backend."""
        return self.__base_path

    def __init__(self, base_path):
        self.__base_path = base_path

    async def async_close(self, handler):
        """Flush and close the IO object.

        This method has no effect if the file is already closed.
        """
        if handler.is_dirty():
            await self.async_push(handler.fd.name, handler.path)
        await handler.fd.__aexit__()

    async def async_download(self, path, dst, decryptor):
        """Downloads file from `path` to `dst` on the local filesystem."""
        raise NotImplementedError("Subclasses must override this method.")

    async def async_exists(self, path):
        """Test whether a path exists.  Returns False for broken symbolic links
        if the storage backend supports them.
        """
        raise NotImplementedError("Subclasses must override this method.")

    def async_open(self, path, mode='rt', *args, **kwargs): # pylint: disable=W1113
        """Open the given `path` in the given `mode`."""
        return self.async_descriptor_class(self, path, mode, *args, **kwargs)

    async def async_push(self, src, path, encryptor=None):
        """Copies local absolute path `src` to remote `path`."""
        raise NotImplementedError("Subclasses must override this method.")

    async def async_slice(self, path, length, offset=0, binary=False):
        """Returns a slice of the blob represented by `path`."""
        raise NotImplementedError("Subclasses must override this method.")

    async def async_pull(self, path, dst=None, decryptor=None):
        """Pulls a file from the given `path` in the storage backend to local
        filepath `dst`. If `dst` is ``None``, then a temporary filepath is
        generated.
        """
        if dst is None:
            _, dst = tempfile.mkstemp()
        return await self.async_download(path, dst, decryptor)

    def close(self, handler):
        """Flush and close the IO object.

        This method has no effect if the file is already closed.
        """
        raise NotImplementedError("Subclasses must override this method.")

    def download(self, path, dst, decryptor):
        """Downloads file from `path` to `dst` on the local filesystem."""
        raise NotImplementedError("Subclasses must override this method.")

    def exists(self, path):
        """Test whether a path exists.  Returns False for broken symbolic links
        if the storage backend supports them.
        """
        raise NotImplementedError("Subclasses must override this method.")

    def get_local_fd(self, handler):
        """Opens a local file descriptor."""
        raise NotImplementedError("Subclasses must override this method.")

    def has_capability(self, cap):
        """Return a boolean indicating if the storage backend has capability
        `cap`.
        """
        return cap in self.capabilities

    def label(self, labels):
        """Update dictionary `labels` with the label for a specific
        storage backend.
        """
        labels['backend'] = self.kind
        labels['base-path'] = self.base_path
        return self.update_labels(labels)

    @abc.abstractmethod
    def update_labels(self, labels):
        """Update dictionary `labels` with the label for a specific
        storage backend.
        """
        raise NotImplementedError("Subclasses must override this method.")

    def open(self, path, mode='rt', *args, **kwargs): # pylint: disable=W1113
        """Open the given `path` in the given `mode`."""
        if not self.exists(path) and mode not in self.write_modes:
            raise FileNotFoundError("No such file or directory: '%s'" % path)
        return self.descriptor_class(self, path, mode, *args, **kwargs)

    def pull(self, path, dst=None, decryptor=None):
        """Pulls a file from the given `path` in the storage backend to local
        filepath `dst`. If `dst` is ``None``, then a temporary filepath is
        generated.
        """
        if dst is None:
            _, dst = tempfile.mkstemp()
        return self.download(path, dst, decryptor)

    def push(self, src, path, encryptor=None):
        """Copies local absolute path `src` to remote `path`."""
        raise NotImplementedError("Subclasses must override this method.")

    def read(self, handler, size=-1):
        """Read at most n characters from handler.

        Read from underlying buffer until we have n characters or we hit EOF.
        If n is negative or omitted, read until EOF.
        """
        raise NotImplementedError("Subclasses must override this method.")

    def slice(self, path, length, offset=0, binary=False):
        """Returns a slice of the blob represented by `path`."""
        raise NotImplementedError("Subclasses must override this method.")

    def storage_path(self, *components):
        """Returns the absolute path in the storage of `path`."""
        return os.path.join(self.base_path or '', *components)

    def unlink(self, path):
        """Remove a path."""
        raise NotImplementedError("Subclasses must override this method.")

    def _validate_slice(self, length, offset):
        if offset < 0:
            raise ValueError("The `offset` parameter must be 0 or greater.")
        if length <= 0:
            raise ValueError("The `length` parameter must be 1 or greater.")


class RemoteStorageBackendMixin: # pylint: disable=R0903
    """Overrides :class:`BaseStorageBackend` methods for use with remote
    storage backends.
    """

    def get_local_fd(self, handler): # pylint: disable=R0201
        """Opens a local file descriptor."""
        _, src = tempfile.mkstemp()
        return open(src, handler.mode)\
            if not handler.is_async()\
            else AIOFile(src, handler.mode)
