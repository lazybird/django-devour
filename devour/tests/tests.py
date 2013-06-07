from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase

from devour.tests.models import Account


CSV_DATA = (
    'Joe, Smith'
    '\nPierre, Dupont'
)


class DevourTestHelper(object):

    def login_as_admin(self):
        User.objects.create_superuser(
            username='admin',
            password='admin',
            email='email@test.com'
        )
        self.client.login(username='admin', password='admin')


class DevourFileTests(DevourTestHelper, TestCase):

    def setUp(self):
        self.login_as_admin()
        self.account = Account.objects.create(first_name='Bob', last_name='Marley')
        self.change_list_url = reverse('admin:tests_account_changelist')
        self.import_url = reverse('admin:tests_account_devour')
        self.import_file = SimpleUploadedFile('accounts.csv', CSV_DATA)

    def test_change_list_page_has_import_button(self):
        response = self.client.get(self.change_list_url)
        self.assertContains(response, 'import')

    def test_import_file_adds_new_accounts(self):
        count_before = Account.objects.count()
        post_data = {'uploaded_file': self.import_file}
        self.client.post(self.import_url, post_data)
        count_after = Account.objects.count()
        self.assertEqual(count_after, count_before + 2)

    def test_running_management_command_adds_new_accounts(self):
        count_before = Account.objects.count()
        call_command('devour_file',
            self.import_file,
            'devour.tests.importers.AccountCSVModel'
        )
        count_after = Account.objects.count()
        self.assertEqual(count_after, count_before + 2)
