"""Declares the ``blob`` management command."""
import ioc
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Provides an interface to perform various management tasks related to
    the blob storage.
    """
    help = __doc__

    def add_arguments(self, parser):
        """Set up the command-line interface."""
        subparser = parser.add_subparsers(
            title="Subcommands",
            dest="subcommand",
            required=True
        )

        generate_key = subparser.add_parser('generate-key')
        generate_key.set_defaults(subcommand=self.handle_generate_key)

    def handle(self, subcommand, *args, **kwargs):
        """Main entrypoint for the ``blob`` management command."""
        return subcommand(*args, **kwargs)

    @ioc.inject('svc', 'BlobEncryptionKeyService')
    def handle_generate_key(self, svc, *args, **kwargs):
        """Handles the ``generate-key`` subcommand."""
        created = svc.generate()
        if created:
            self.stdout.write("Blob encryption key generated.")
        else:
            self.stdout.write(
                "No encryption key was generated because there are pre-existing"
                " keys. Use the rotate-key command instead."
            )
