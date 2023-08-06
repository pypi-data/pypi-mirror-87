"""Declares :class:`SQLAlchemyBackend`."""
from sqlalchemy.orm.exc import NoResultFound

from unimatrix.ext.octet.orm import Blob


class SQLAlchemyBackend:
    """Provides an interface to persist blobs used as input for jobs (environment,
    arguments, secrets and files), using SQLAlchemy as the persistent data
    storage layer.
    """
    capabilities = []
    model = Blob
    DoesNotExist = NoResultFound

    def exists(self, checksum):
        """Return a boolean indicating if a file with the given checksum
        exists.
        """
        return self.session.query(
            self.session.query(self.model)
                .filter(self.model.checksum==checksum)
                .exists()
        ).scalar()

    def lookup_dao(self, checksum):
        """SQLAlchemy-specific implementation to lookup the Data Access
        Object (DAO).
        """
        return self.session.query(self.model)\
            .filter(self.model.checksum==checksum)\
            .one()

    def persist_dao(self, dao):
        """SQLAlchemy-specific implementation to lookup the Data Access
        Object (DAO).
        """
        self.session.add(dao)
        self.session.flush()

    def setup_context(self, session, *args, **kwargs):
        """Hook to setup the context."""
        self.session = session
