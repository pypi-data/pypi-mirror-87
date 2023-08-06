"""Declares :class:`AsyncDescriptor`."""
from .descriptor import BaseDescriptor


class AsyncDescriptor(BaseDescriptor):
    """Describes a sequence of octets (i.e. a file) persisted somewhere."""

    def is_async(self):
        """Return a boolean indicating if the descriptor is async."""
        return True

    async def close(self):
        """Flush and close the IO object.

        This method has no effect if the file is already closed.
        """
        if not self._closed:
            await self.fd.fsync()
            await self.backend.async_close(self)
            self._closed = True

    async def write(self, buf):
        """Writes string or byte-sequence `buf` to the **local** storage
        buffer.
        """
        if self.mode not in self.write_modes:
            raise io.UnsupportedOperation("not writable")
        await self.fd.write(buf)
        self._dirty = True

    async def __aenter__(self):
        if not (await self.backend.async_exists(self._path))\
        and self._mode not in self.write_modes:
            raise FileNotFoundError("No such file or directory: '%s'" % self._path)
        await self.fd.__aenter__()
        return self

    async def __aexit__(self, cls, exc, traceback):
        await self.close()
