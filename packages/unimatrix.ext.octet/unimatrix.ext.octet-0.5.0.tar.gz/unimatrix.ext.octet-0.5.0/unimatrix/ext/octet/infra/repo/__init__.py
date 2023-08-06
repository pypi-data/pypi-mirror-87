# pylint: skip-file
from .abstractblob import AbstractBlobRepository
from .django import DjangoBackend
from .sqlalchemy import SQLAlchemyBackend


BlobRepository = AbstractBlobRepository.class_factory(DjangoBackend)
