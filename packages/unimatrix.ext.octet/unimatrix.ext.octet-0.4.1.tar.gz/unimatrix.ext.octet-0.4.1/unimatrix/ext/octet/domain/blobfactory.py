"""Declares :class:`BlobFactory`."""
import hashlib
import os

import ioc


class BlobFactory:
    """Exposes an interface to create new :term:`Blobs`."""
    max_encrypted_size = 1024**2

    @ioc.inject('encrypter', 'BlobEncryptionBackend')
    def new(self, model, f, content_type, encrypter, encrypt=False):
        """Create a new :term:`Blob`."""
        Blob = model
        params = {
            #'annotations': {},
            'checksum': self.calculate_checksum(f),
            'content_type': content_type,
            'length': self.get_filesize(f.name)
        }

        # TODO: Reading the file to memory is not efficient and the assumption
        # that the size is limited by the caller might not hold true.
        if encrypt:
            from django.apps import apps
            Blob = apps.get_model('octet', 'EncryptedBlob')
            f.seek(0)
            if params['length'] > self.max_encrypted_size:
                raise ValueError("File too large.")
            pt = f.read()
            ct = encrypter.symmetric().encrypt(pt)
            params.update({
                'length': len(bytes(ct)),
                'using_id': encrypter.get_key_id(),
                'annotations': ct.annotations
            })
            with open(f.name, 'wb') as c:
                c.write(bytes(ct))
            f.seek(0)

        return Blob(**params)

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
