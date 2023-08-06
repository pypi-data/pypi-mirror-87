# pylint: skip-file
import unittest

import ioc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ....domain import BlobFactory
from ....orm import metadata
from .blobrepositorybase import BlobRepositoryTestCase
from ..sqlalchemy import SQLAlchemyBackend


class BlobRepositoryTestCase(BlobRepositoryTestCase, unittest.TestCase):
    __test__ = True
    backend_class = SQLAlchemyBackend

    def setUp(self):
        ioc.teardown()
        super().setUp()
        self.engine = create_engine("sqlite:///", echo=True)
        self.session_factory = sessionmaker(bind=self.engine)

        metadata.create_all(self.engine)
        ioc.provide('BlobFactory', BlobFactory())

    def get_context_kwargs(self):
        return {'session': self.session_factory()}
