# Unimatrix Octet

Provides an abstraction layer of basic file operations for local and
cloud storage.


## TLDR

- Run `make bash` to spawn a terminal providing a configured runtime environment
  to debug, test and run the package.
- Run `make lint` to check code style and quality.
- Run `make test` to run the tests.
- Run `make clean` to cleanup artifacts.
- Run `make runserver` to start a demo/debug server.
- Run `make bump-(major|minor|patch|prerelease|build)` to increase the major, minor,
  patch, prerelease or build version respectively.

## Installation

### Before you begin

Before you can install the `unimatrix.ext.octet` package, you need to ensure
that the required dependencies are provided in your operating system environment:

1. Ensure that a supported Python version is installed (3.5, 3.6, 3.7, 3.8, 3.9).
2. Ensure that the following command-line tools are available:
   - `awk`, `cp`, `mv`, `rm`, `sha1sum`, `sha256sum`, and `sed`; available on POSIX systems.
   - `curl`
   - `git`
   - `make`
3. Install `pip` using cURL:

   ```bash
   curl https://bootstrap.pypa.io/get-pip.py | /usr/bin/env python3
   ```

4. Install or update the required packages and libraries on your operating system:

   - Debian/Ubuntu:

     ```
     apt-get install -y libffi-dev openssl-dev
     ```

   - Alpine Linux:

     ```
     apk add libffi-dev libressl-dev
     ```

   - Fedora/Red Hat Enterprise Linux/CentOS

     ```
     dnf install libffi-devel openssl-devel
     ```

    *You can skip this step if you plan to always use the package or application
    inside a Docker container.*

  Additional packages may need to be installed for specific use cases.

For additional details on the configuration of your operating system environment,
refer to the technical documentation.

### System-wide installation

Run the following command in a terminal to install the `unimatrix.ext.octet`
package:

```
pip install unimatrix.ext.octet
```

## Usage - Basic Example

Provide an example of basic usage.

```python
import tempfile

from unimatrix.ext.octet.lib.backends.local import LocalDiskBackend

backend = LocalDiskBackend(base_path=tempfile.gettempdir())
with open('hello.txt', 'w') as f:
    f.write("Hello world!")
```

For more advanced examples refer to the [Unimatrix Octet Technical Documentation](https://unimatrixone.gitlab.io/libraries/python-unimatrix/octet).

## Resources

- [Unimatrix Octet Technical Documentation](https://unimatrixone.gitlab.io/libraries/python-unimatrix/octet)
- [azure.storage.blob.BlobClient.download_blob](https://docs.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.blobclient?view=azure-python#download-blob)

## License

Proprietary

## Author information

This Python package was created by **Cochise Ruhulessin** for the
[Unimatrix One](https://cloud.unimatrixone.io) project.

- [Send me an email](mailto:cochise.ruhulessin@unimatrixone.io)
- [GitLab](https://gitlab.com/unimatrixone)
- [GitHub](https://github.com/cochiseruhulessin)
- [LinkedIn](https://www.linkedin.com/in/cochise-ruhulessin-0b48358a/)
- [Twitter](https://twitter.com/magicalcochise)
