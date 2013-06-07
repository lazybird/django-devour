from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _

from devour.utils import run_import


class Command(BaseCommand):
    args = '<file_name> <importer>'
    help = _('Import a file using the given importer module.')

    def handle(self, *args, **options):
        try:
            import_file, importer_path = args
        except ValueError:
            raise CommandError(
                'This command takes a file or a file name and a dotted '
                'path to the importer module.'
            )
        run_import(import_file, importer_path)
        self.stdout.write(_('File Import Completed'))
