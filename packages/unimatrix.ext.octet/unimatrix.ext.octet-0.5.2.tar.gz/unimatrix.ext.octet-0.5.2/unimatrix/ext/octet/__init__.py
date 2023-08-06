# pylint: skip-file
"""Top-level module for the :mod:`unimatrix.ext.octet` module."""
import os


default_app_config = 'unimatrix.ext.octet.apps.ApplicationConfig'


BACKEND_MODULES = {
    'local': 'unimatrix.ext.octet.lib.backends.local',
    'azure': 'unimatrix.ext.octet.lib.backends.azure',
    'gcs': 'unimatrix.ext.octet.lib.backends.gcs',
}


def get_application_storage(env=None):
    """Return the application local storage backend.

    The following environment variables are used to configure the storage
    backend:

    - ``OCTET_BACKEND`` - The storage backend. Must be one of ``local``,
      ``gcs`` or ``azure``.
    - ``OCTET_PREFIX`` - Prefix for the blob paths. For the local storage
        backend, this is a file path.
    """
    import importlib
    env = env or os.environ
    backend = env.get('OCTET_BACKEND')
    base_path = env.get('OCTET_PREFIX') or 'var/blob'
    if backend not in ['local', 'azure', 'gcs']:
        raise ValueError("Unsupported backend %s" % backend)
    module = importlib.import_module(BACKEND_MODULES[backend])
    return module.StorageBackend(base_path)
