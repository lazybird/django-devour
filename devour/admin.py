from django.conf.urls import patterns, url
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from devour.utils import run_import


class FileImportAdmin(object):
    change_list_template = "admin/devour/change_list.html"

    def get_urls(self):
        """
        Adds the URL for the import view.
        """
        url_name_prefix = '%(app_name)s_%(model_name)s' % self.url_params
        urls = super(FileImportAdmin, self).get_urls()
        custom_urls = patterns('',
            url(r'^import/$',
                self.admin_site.admin_view(self.import_file), {},
                name='%s_devour' % url_name_prefix
            ))
        return custom_urls + urls

    def import_file(self, request):
        """
        Runs the import task.
        """
        uploaded_file = request.FILES['uploaded_file']
        try:
            run_import(uploaded_file, self.importer)
            msg = _('Successfully processed %s.') % uploaded_file
            self.message_user(request, msg)
        except Exception, e:
            msg = _('Import failed: %s') % e
            self.message_user(request, msg, level=messages.ERROR)
        return redirect(self.change_list_url_name)

    @property
    def change_list_url_name(self):
        """
        Returns the URL name for the change list page.
        """
        return 'admin:%(app_name)s_%(model_name)s_changelist' % self.url_params

    @property
    def url_params(self):
        """
        Returns the model name and the app label for which the import
        task will be run.
        """
        return {
            'app_name': self.model._meta.app_label,
            'model_name': self.model._meta.module_name,
        }
