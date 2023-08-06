# pylint: skip-file
import hashlib
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .. import Blob
from .. import BlobReference
from .. import metadata


class BlobReferenceRelationshipTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///", echo=True)
        self.session_factory = sessionmaker(bind=self.engine)
        metadata.create_all(self.engine)

        # Insert a fake Blob entity and a BlobReference
        blob = Blob(checksum=hashlib.sha256().hexdigest())
        session = self.session_factory()
        session.add(blob)
        session.flush()

        ref = BlobReference(blob_id=blob.checksum, owner='unittest.TestCase')

        session.add(ref)
        session.commit()

        self.blob_id = blob.checksum

    def test_blob_can_access_references(self):
        session = self.session_factory()
        blob = session.query(Blob).one()

        self.assertEqual(len(blob.references), 1)

    def test_references_can_access_blob(self):
        session = self.session_factory()
        ref = session.query(BlobReference).one()

        self.assertEqual(ref.blob.checksum, self.blob_id)
