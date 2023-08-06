# pylint: skip-file
import asyncio
import io
import os
import tempfile
import unittest

import unimatrix.lib.test

from ..local import LocalDiskBackend


class LocalDiskBackendTestCase(unittest.TestCase):
    backend_class = LocalDiskBackend
    capabilities = ['unlink']

    @classmethod
    def setUpClass(cls):
        try:
            cls.loop = asyncio.get_event_loop()
        except RuntimeError:
            cls.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(cls.loop)

    @classmethod
    def tearDownClass(cls):
        cls.loop.close()

    def setUp(self):
        self.backend = self.get_backend()

    def get_backend(self):
        return self.backend_class(**self.get_backend_kwargs())

    def get_backend_kwargs(self):
        return {
            'base_path': tempfile.mkdtemp()
        }

    def test_context_closes_file(self):
        src = 'foo'
        with self.backend.open(src, 'w') as f:
            f.write("Hello world!")
        self.assertTrue(self.backend.exists(src))
        with self.backend.open(src) as f:
            pass
        self.assertTrue(f.is_closed())

    def test_push_to_nonexisting_directory(self):
        dst = '%s/%s' % (bytes.hex(os.urandom(8)), bytes.hex(os.urandom(8)))
        with tempfile.NamedTemporaryFile() as f:
            f.write(b"Hello world!")
            f.flush()

            self.backend.push(f.name, dst)

    def test_write_file_with_context(self):
        src = 'foo'
        with self.backend.open(src, 'w') as f:
            f.write("Hello world!")

        with self.backend.open(src) as fd:
            self.assertEqual(fd.read(), "Hello world!")

    def test_write_file_with_fd(self):
        src = 'foo'
        fd = self.backend.open(src, 'w')
        fd.write("Hello world!")
        fd.close()

        with self.backend.open(src) as fd:
            self.assertEqual(fd.read(), "Hello world!")

    def test_reading_non_existing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            self.backend.open(bytes.hex(os.urandom(16)))

    def test_write_to_reading_file_raises(self):
        src = 'foo'
        with self.backend.open(src, 'w') as f:
            f.write("foo")
        fd = self.backend.open(src)
        with self.assertRaises(io.UnsupportedOperation):
            fd.write("Hello world!")

    def test_read_from_closed_file_raises(self):
        src = 'foo'
        with self.backend.open(src, 'w') as f:
            f.write("foo")
        fd = self.backend.open(src)
        fd.close()
        with self.assertRaises(ValueError):
            fd.read()

    def test_pull_without_dst(self):
        path = '%s/%s' % (bytes.hex(os.urandom(8)), bytes.hex(os.urandom(8)))
        with self.backend.open(path, 'w') as f:
            f.write("Hello world!")

        self.assertTrue(self.backend.exists(path))
        tmp = self.backend.pull(path)

        with open(tmp) as f:
            self.assertEqual("Hello world!", f.read())

    def test_push(self):
        with tempfile.NamedTemporaryFile() as f:
            f.write(b"Hello world!")
            f.flush()

            fn = bytes.hex(os.urandom(16))
            self.backend.push(f.name, fn)

        self.assertTrue(self.backend.exists(fn))
        with self.backend.open(fn) as f:
            self.assertEqual("Hello world!", f.read())

    def test_read_rb_returns_bytes(self):
        src = 'foo'
        with self.backend.open(src, 'w') as f:
            f.write("Hello world!")

        with self.backend.open(src, 'rb') as fd:
            self.assertIsInstance(fd.read(), bytes)

    def test_read_r_returns_string(self):
        src = 'foo'
        with self.backend.open(src, 'w') as f:
            f.write("Hello world!")

        with self.backend.open(src, 'r') as fd:
            self.assertIsInstance(fd.read(), str)

    def test_read_rt_returns_string(self):
        src = 'foo'
        with self.backend.open(src, 'w') as f:
            f.write("Hello world!")

        with self.backend.open(src, 'rt') as fd:
            self.assertIsInstance(fd.read(), str)

    def test_unlink_file(self):
        if 'unlink' not in self.capabilities:
            raise unittest.SkipTest("unlink not supported for backend.")
        src = 'foo'
        with self.backend.open(src, 'w') as f:
            f.write("Hello world!")

        self.assertTrue(self.backend.exists(src))
        self.backend.unlink(src)
        self.assertTrue(not self.backend.exists(src))

    def test_unlink_dir(self):
        if 'unlink' not in self.capabilities:
            raise unittest.SkipTest("unlink not supported for backend.")
        src = 'foo/bar/baz/taz'
        with self.backend.open(src, 'w') as f:
            f.write("Hello world!")

        self.assertTrue(self.backend.exists(src))
        self.backend.unlink('foo/bar/baz')
        self.assertTrue(not self.backend.exists(src))

    def test_overwrite(self):
        """Overwriting an existing key must not raise exceptions."""
        src = 'foo/bar/baz/taz'
        with self.backend.open(src, 'w') as f:
            f.write("Hello world!")
        with self.backend.open(src, 'w') as f:
            f.write("Hello world!")

    def test_slice_no_offset(self):
        src = 'foo/bar/baz/taz'
        with self.backend.open(src, 'w') as f:
            f.write("Hello world!")
        self.assertEqual(self.backend.slice(src, 5), "Hello")

    def test_slice_no_offset_binary(self):
        src = 'foo/bar/baz/taz'
        with self.backend.open(src, 'wb') as f:
            f.write(b"Hello world!")
        self.assertEqual(self.backend.slice(src, 5, binary=True), b"Hello")

    def test_slice_raises_value_error_on_offset_lt_zero(self):
        src = 'foo/bar/baz/taz'
        with self.assertRaises(ValueError):
            self.backend.slice(src, length=1, offset=-1)

    def test_slice_raises_value_error_on_length_lte_zero(self):
        src = 'foo/bar/baz/taz'
        with self.assertRaises(ValueError):
            self.backend.slice(src, length=0)

    def test_async_rw(self):
        src = 'foo/bar/baz/taz'
        async def afunc():
            async with self.backend.async_open(src, 'w') as f:
                self.assertFalse(f.is_dirty())
                await f.write("Hello world!")
                self.assertTrue(f.is_dirty())
            self.assertTrue(await self.backend.async_exists(src))

        asyncio.run(afunc())

    def test_async_push_pull(self):
        src = 'foo/bar/baz/taz'
        blob = "Hello world!"
        async def afunc():
            with tempfile.NamedTemporaryFile('w') as f:
                f.write(blob)
                f.flush()

                await self.backend.async_push(f.name, src)
                self.assertTrue(await self.backend.async_exists(src))
                tmp = await self.backend.async_pull(src)
                self.assertEqual(open(tmp).read(), blob)

        asyncio.run(afunc())

    def test_async_slice_no_offset(self):
        if not self.backend.has_capability('slice:async'):
            self.skipTest("Backend does not support asynchronous slicing.")
        src = 'foo/bar/baz/taz'
        async def afunc():
            with self.backend.open(src, 'w') as f:
                f.write("Hello world!")
            self.assertEqual(await self.backend.async_slice(src, 5), "Hello")

        asyncio.run(afunc())

    def test_async_slice_no_offset_binary(self):
        if not self.backend.has_capability('slice:async'):
            self.skipTest("Backend does not support asynchronous slicing.")
        src = 'foo/bar/baz/taz'
        async def afunc():
            with self.backend.open(src, 'w') as f:
                f.write("Hello world!")
            self.assertEqual(
                await self.backend.async_slice(src, 5, binary=True), b"Hello"
            )

        asyncio.run(afunc())

    def test_async_offset_after_eof_returns_empty_string(self):
        if not self.backend.has_capability('slice:async'):
            self.skipTest("Backend does not support asynchronous slicing.")
        src = 'foo/bar/baz/taz'
        async def afunc():
            with self.backend.open(src, 'w') as f:
                f.write("Hello world!")
            self.assertEqual(await self.backend.async_slice(src, 5, offset=12), "")

        asyncio.run(afunc())

    def test_async_slice_raises_value_error_on_offset_lt_zero(self):
        if not self.backend.has_capability('slice:async'):
            self.skipTest("Backend does not support asynchronous slicing.")
        src = 'foo/bar/baz/taz'
        async def afunc():
            with self.assertRaises(ValueError):
                await self.backend.async_slice(src, length=1, offset=-1)

        asyncio.run(afunc())

    def test_async_slice_raises_value_error_on_length_lte_zero(self):
        if not self.backend.has_capability('slice:async'):
            self.skipTest("Backend does not support asynchronous slicing.")
        src = 'foo/bar/baz/taz'
        async def afunc():
            with self.assertRaises(ValueError):
                await self.backend.async_slice(src, length=0)

        asyncio.run(afunc())
