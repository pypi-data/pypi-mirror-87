"""Declares the base class for all relations in the :mod:`unimatrix.ext.octet`
package.
"""
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


#: The :attr:`metadata` attribute of the ORM package is exposed for implemting
#: applications to manage their migrations with Alembic.
metadata = Base.metadata
