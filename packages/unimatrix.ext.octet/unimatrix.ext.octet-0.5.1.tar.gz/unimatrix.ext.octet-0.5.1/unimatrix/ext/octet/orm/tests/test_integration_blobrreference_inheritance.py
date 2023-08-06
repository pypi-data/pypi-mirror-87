# pylint: skip-file
import hashlib
import unittest

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker

from .. import Base
from .. import Blob
from .. import BlobReference
from .. import metadata


class BlobReferenceInheritanceTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///", echo=True)
        self.session_factory = sessionmaker(bind=self.engine)
        metadata.create_all(self.engine)

        # Insert a fake Blob entity.
        session = self.session_factory()
        self.blob = blob = Blob(checksum=hashlib.sha256().hexdigest())
        session.add(blob)
        session.commit()

    def test_ddl(self):
        # This test should simple pass.
        pass

    def test_insert_referencing_model(self):
        session = self.session_factory()
        session.add(
            ReferencingModel(
                owner='unittest.TestCase',
                blob_id=self.blob.id
            )
        )
        session.commit()

        bas = session.query(BlobReference).first()
        ref = session.query(ReferencingModel).first()

        self.assertEqual(bas.id, ref.id)
        self.assertEqual(bas.blob_id, ref.blob_id)


class ReferencingModel(BlobReference):
    id = Column(
        ForeignKey(BlobReference.id),
        primary_key=True,
        name='id'
    )

    __tablename__ = 'referencingmodel'
    __mapper_args__ = {
        'polymorphic_identity': __tablename__
    }
