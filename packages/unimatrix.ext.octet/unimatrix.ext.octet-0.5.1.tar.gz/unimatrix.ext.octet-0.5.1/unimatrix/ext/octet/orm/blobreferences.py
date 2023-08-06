"""Declares :class:`BlobReference`."""
import uuid

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy.orm import relationship
from unimatrix.lib import timezone

from .base import Base
from .blobs import Blob
from .uuidtype import GUID


class BlobReference(Base):
    """Maintains a reference to a :class:`Blob`."""
    OWNER_FIELD = None
    __module__ = 'unimatrix.ext.octet.orm'
    __tablename__ = 'blobreferences'
    blob = relationship("Blob", back_populates='references')

    id = Column(
        GUID,
        nullable=False,
        default=uuid.uuid4,
        primary_key=True,
        name='id'
    )

    blob_id = Column(
        ForeignKey(Blob.checksum),
        nullable=False,
        name='blob_id'
    )

    owner = Column(
        String(63),
        nullable=False,
        name='owner'
    )

    referenced = Column(
        BigInteger,
        nullable=False,
        default=timezone.now,
        name='referenced'
    )

    labels = Column(
        JSON,
        nullable=False,
        default=dict,
        name='labels'
    )

    __mapper_args__ = {
        'polymorphic_identity': __tablename__
    }
