"""Declares :class:`Blob`."""
from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy.orm.exc import NoResultFound
from unimatrix.lib import timezone

from ..abstract import BlobDAO
from .base import Base


class Blob(Base, BlobDAO):
    """Maintains information about blobs used by an application."""
    __tablename__ = 'blobs'
    __module__ = 'unimatrix.ext.octet.orm'
    ObjectDoesNotExist = NoResultFound

    #: A surrogate primary key.
    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        nullable=False,
        primary_key=True,
        name='id'
    )

    #: SHA-256 hash of the blob content. If the :class:`Blob` is encrypted,
    #: the hash of the plain text.
    checksum = Column(
        String(63),
        nullable=False,
        unique=True,
        name='checksum'
    )

    #: Date and time at which the :class:`Blob` was created, in milliseconds
    #: since the UNIX epoch.
    created = Column(
        BigInteger,
        nullable=False,
        default=timezone.now,
        name='created'
    )

    #: If known, the content type of the :class:`Blob`.
    content_type = Column(
        String(63),
        nullable=False,
        default="application/octet-stream",
        name='content_type'
    )

    #: The size of the blob, in bytes."
    length = Column(
        BigInteger,
        nullable=False,
        default=0,
        name='length'
    )

    #: Mapping of key/value pairs providing extra context for this specific
    #: :class:`Blob`. All keys and values must be strings.
    labels = Column(
        JSON,
        nullable=False,
        default=dict,
        name='labels'
    )
