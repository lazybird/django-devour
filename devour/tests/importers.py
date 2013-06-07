from adaptor import fields
from adaptor.model import CsvModel

from devour.tests.models import Account


class AccountCSVModel(CsvModel):
    first_name = fields.CharField()
    last_name = fields.CharField()

    class Meta:
        delimiter = ","
        dbModel = Account
        silent_failure = False
