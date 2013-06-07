from django.contrib import admin

from devour.admin import FileImportAdmin
from devour.tests.models import Account
from devour.tests.importers import AccountCSVModel


class AccountAdmin(FileImportAdmin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    importer = AccountCSVModel


admin.site.register(Account, AccountAdmin)
