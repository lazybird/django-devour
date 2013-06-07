from django.db import models


class Account(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)
