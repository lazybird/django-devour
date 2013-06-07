from django.conf import settings
from django.utils.importlib import import_module

from devour import settings as devour_settings


def load_module(path):
    """
    Loads and returns the module from the given dotted path.
    For instance, dynamically loading `stores.importers.StoreCSVModel`,
    is equivalent to this statement: `from stores.importers import
    StoreCSVModel`.
    """
    package, module = path.rsplit('.', 1)
    return getattr(import_module(package), module)


def run_import(import_file, importer):
    """
    Runs the import method for the given importer. The importer is expected
    to be a dotted path or the python class.
    """
    if isinstance(importer, basestring):
        importer_class = load_module(importer)
    else:
        importer_class = importer
    method_name = getattr(settings,
        'DEVOUR_IMPORT_METHOD_NAME',
        devour_settings.DEVOUR_IMPORT_METHOD_NAME
    )
    import_method = getattr(importer_class, method_name)
    output = import_method(import_file)
    return output
