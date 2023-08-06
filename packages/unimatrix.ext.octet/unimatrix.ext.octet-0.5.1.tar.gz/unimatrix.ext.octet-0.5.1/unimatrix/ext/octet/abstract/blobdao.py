"""Declares :class:`BlobDAO`."""
import json


class BlobDAO:
    """The base class for all :term:`Blob` Data Access Object (DAO)
    implementations.
    """

    def is_encrypted(self):
        """Return a boolean indicating if the :class:`Blob` is encrypted."""
        try:
            return self.ciphertext is not None
        except (self.ObjectDoesNotExist, AttributeError):
            return False

    def get_ciphertext(self, buf):
        """Return a :class:`~unimatrix.ext.crypto.CipherText` instance
        with the parameters used when encrypting this :class:`Blob`.
        """
        if not self.is_encrypted():
            raise TypeError("Blob is not encrypted.")
        return self.ciphertext.get_ciphertext(buf)

    def get_key_id(self):
        """Return an integer identifying the :class:`BlobEncryptionKey` that
        was used to encrypt this :class:`Blob`, or ``None`` if it is not
        encrypted.
        """
        return self.ciphertext.using_id if self.is_encrypted() else None

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
