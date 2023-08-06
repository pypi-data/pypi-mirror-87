"""Declares :class:`Descriptor`."""
import io


class BaseDescriptor:
    """The base class for all descriptor implementations."""
    write_modes = ['w', 'wt', 'wb']
    read_modes = ['r', 'rt', 'rb']

    @property
    def mode(self):
        """Return the mode in which the descriptor was created."""
        return self._mode

    @property
    def path(self):
        """Return the path relative to the storage backend base path."""
        return self._path

    @property
    def backend(self):
        """Return the :class:`BaseStorageBackend` used by this descriptor."""
        return self._backend

    @property
    def fd(self): # pylint: disable=invalid-name
        """Returns the local file descriptor."""
        if self._fd is None:
            self._fd = self.backend.get_local_fd(self)
        return self._fd

    def __init__(self, backend, path, mode, *args, **kwargs): # pylint: disable=unused-argument
        self._backend = backend
        self._closed = False
        self._dirty = False
        self._fd = None
        self._mode = mode
        self._path = path
        self._pointer = 0

    def is_async(self):
        """Return a boolean indicating if the descriptor is async."""
        return False

    def is_binary(self):
        """Return a boolean indicating if were opened for binary reading
        or writing.
        """
        return self.mode in ['rb', 'wb']

    def is_closed(self):
        """Return a boolean indicating if the file descriptor is closed."""
        return self._closed

    def is_dirty(self):
        """Return a boolean indicating if the descriptor is dirty."""
        return self._dirty


class Descriptor(BaseDescriptor):
    """Describes a sequence of octets (i.e. a file) persisted somewhere."""

    def close(self):
        """Flush and close the IO object.

        This method has no effect if the file is already closed.
        """
        if not self._closed:
            self.fd.flush()
            self.backend.close(self)
            self.fd.close()
            self._closed = True

    def read(self, size=-1):
        """Read at most n characters from stream.

        Read from underlying buffer until we have n characters or we hit EOF.
        If n is negative or omitted, read until EOF.
        """
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        return self.backend.read(self, size)

    def seek(self, cookie, whence=0):
        """Change stream position.

        Change the stream position to the given byte offset. The offset is
        interpreted relative to the position indicated by whence.  Values
        for whence are:

        * 0 -- start of stream (the default); offset should be zero or positive
        * 1 -- current stream position; offset may be negative
        * 2 -- end of stream; offset is usually negative

        Return the new absolute position.
        """
        raise NotImplementedError("Subclasses must override this method.")

    def write(self, buf):
        """Writes string or byte-sequence `buf` to the **local** storage
        buffer.
        """
        if self.mode not in self.write_modes:
            raise io.UnsupportedOperation("not writable")
        self.fd.write(buf)
        self._dirty = True

    def __enter__(self):
        return self

    def __exit__(self, cls, exc, traceback):
        self.close()

    def __str__(self): # pragma: no cover
        return "<%s: %s>" % (type(self).__name__, self._path)
