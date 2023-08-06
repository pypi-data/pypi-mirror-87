from django.db import models

from ad_import.models import Directory

IMPORT_TARGETS = [('ad_import.models.workstation', 'Workstation'),
                  ('ad_import.models.server', 'Server'),
                  ('ad_import.models.user', 'User'),
                  ('ad_import.models.group', 'Group')]


class Query(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    directory = models.ForeignKey(Directory, on_delete=models.PROTECT, related_name='queries')
    query = models.CharField(max_length=200)
    base_dn = models.CharField('Base DN', max_length=200, blank=True, null=True)
    type = models.CharField(max_length=15, choices=[('user', 'User'), ('computer', 'Computer'), ('group', 'Group')])
    target = models.CharField(max_length=200, choices=IMPORT_TARGETS)

    def __str__(self):
        return '%s %s' % (self.directory.dn, self.query)

    class Meta:
        verbose_name = 'LDAP query'
        verbose_name_plural = 'LDAP queries'
