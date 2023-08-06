"""Declares :class:`LocalDiskBackend`."""
import shutil
import os

from aiofile import AIOFile
from aiofile import Reader
from aiofile import Writer

from .base import BaseStorageBackend


class LocalDiskBackend(BaseStorageBackend):
    """A storage backend that uses the local filesystem."""
    capabilities = ['slice', 'slice:async']
    kind = 'local'

    async def async_download(self, path, dst, decryptor=None):
        """This method exists only for API compatibility."""
        src = self.storage_path(path)
        async with AIOFile(src, 'rb') as sf:
            reader = Reader(sf, chunk_size=4096)
            async with AIOFile(dst, 'wb') as tf:
                writer = Writer(tf)
                async for chunk in reader:
                    await writer(chunk)
        return dst

    async def async_exists(self, path):
        """Test whether a path exists.  Returns False for broken symbolic links
        if the storage backend supports them.
        """
        return os.path.exists(self.storage_path(path))

    async def async_push(self, src, path, encryptor=None):
        """Copies local absolute path `src` to remote `path`."""
        dst = self.storage_path(path)
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        async with AIOFile(src, 'rb') as sf:
            reader = Reader(sf, chunk_size=4096)
            async with AIOFile(dst, 'wb') as tf:
                writer = Writer(tf)
                async for chunk in reader:
                    await writer(chunk)

    async def async_slice(self, path, length, offset=0, binary=False):
        """Returns a slice of the blob represented by `path`."""
        return self.slice(path, length, offset, binary)

    def close(self, handler):
        """Flush and close the IO object.

        This method has no effect if the file is already closed.
        """
        handler.fd.close()

    def download(self, path, dst, decryptor):
        """This method exists only for API compatibility."""
        shutil.copy2(self.storage_path(path), dst)
        return dst

    def exists(self, path):
        """Test whether a path exists.  Returns False for broken symbolic links
        if the storage backend supports them.
        """
        return os.path.exists(self.storage_path(path))

    def get_local_fd(self, handler):
        """Opens a local file descriptor."""
        local_path = self.storage_path(handler.path)
        if not os.path.exists(os.path.dirname(local_path)):
            os.makedirs(os.path.dirname(local_path))
        return open(local_path, handler.mode)\
            if not handler.is_async()\
            else AIOFile(local_path, handler.mode)

    def update_labels(self, labels): # pylint: disable=W0107
        """Update dictionary `labels` with the label for a specific
        storage backend.
        """

    def read(self, handler, size=-1):
        """Read at most n characters from handler.

        Read from underlying buffer until we have n characters or we hit EOF.
        If n is negative or omitted, read until EOF.
        """
        return handler.fd.read(size)

    def push(self, src, path, encryptor=None):
        """Copies local absolute path `src` to remote `path`."""
        dst = self.storage_path(path)
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        shutil.copy2(src, dst)

    def slice(self, path, length, offset=0, binary=False):
        """Returns a slice of the blob represented by `path`."""
        self._validate_slice(length, offset)
        mode = 'r'
        if binary:
            mode = 'rb'
        with open(self.storage_path(path), mode) as f:
            if offset:
                f.seek(offset)
            return f.read(length)

    def unlink(self, path):
        """Remove a path."""
        dst = self.storage_path(path)
        if os.path.isdir(dst):
            func = shutil.rmtree
        else:
            func = os.unlink
        func(dst)


StorageBackend = LocalDiskBackend
