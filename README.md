
Django Devour
=============

Django Devour helps importing files into your database - for instance CSV.
It lets you define the logic for the data import in a custom importer module.
It gives you a Django management command that points to your importer module.
It also provides a way to add an import button in the admin.


Installation
------------

Install the package using something like pip and add `devour` to
your `INSTALLED_APPS` setting.

You can run tests for django-devour this way:

    ./manage.py test tests --settings=devour.tests.settings


Importer Module
---------------

The importer is class that defines an import method. For instance,
`AccountCSVHandler` is an importer that defines `import_data(data)`.
It's expected to be called this way:


     AccountCSVHandler.import_data("accounts.csv")


You can use [django-adaptors][adaptors] to build a CSV data importer.
It gives you the `import_data()` method.


Management Command
------------------

The management command expect the file name and the dotted path to the
importer module:

    ./manage.py devour_file <file_name> <importer>
    ./manage.py devour_file accounts.csv accounts.importers.AccountCSVHandler

In the following example, we will define a `Account` Django model that stores
first and last names. The importer will be using [django-adaptors][adaptors] to
build a CSV importer. Point


    # accounts/models.py

    from django.db import models

    class Account(models.Model):
        first_name = models.CharField(max_length=255)
        last_name = models.CharField(max_length=255)

        def __unicode__(self):
            return '%s %s' % (self.first_name, self.last_name)



    # accounts/importers.py

    from adaptor import fields
    from adaptor.model import CsvModel
    from accounts.models import Account

    class AccountCSVHandler(CsvModel):
        first_name = fields.CharField()
        last_name = fields.CharField()

        class Meta:
            delimiter = ","
            dbModel = Account
            silent_failure = False


    # In the shell

    ./manage.py devour_file accounts.csv accounts.importers.AccountCSVHandler


Import From The Admin
---------------------

You can add an upload / import button in your admin page.
This will call the importer that was specified in the ModelAdmin class.

![django-devour admin](https://raw.github.com/lazybird/django-devour/master/docs/images/devour-file-admin.png "django-devour admin")


    # accounts/admin.py

    from django.contrib import admin
    from devour.admin import FileImportAdmin
    from accounts.importers import AccountCSVHandler
    from accounts.models import Account

    class AccountAdmin(FileImportAdmin, admin.ModelAdmin):
        list_display = ('first_name', 'last_name')
        importer = AccountCSVHandler

    admin.site.register(Account, AccountAdmin)


The admin class is expected to have a `importer` attribute that can be either
the importer class or a dotted path to it.

Here for instance, we will have
`importer = 'accounts.importers.AccountCSVHandler'`


Settings
--------

### Import Method Name
By default, we use `import_data` as the import method name.
This can be changed:

    DEVOUR_IMPORT_METHOD_NAME = 'my_custom_import'

With this setting, the `AccountCSVHandler` importer will be called
this way:


     AccountCSVHandler.my_custom_import("accounts.csv")



[adaptors]: http://django-adaptors.readthedocs.org
