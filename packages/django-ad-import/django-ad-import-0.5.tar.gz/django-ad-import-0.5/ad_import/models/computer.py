from django.db import models

from .directory import Directory


class Computer(models.Model):
    cn = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField('beskrivelse', max_length=255, blank=True, null=True)
    distinguishedName = models.CharField('DN', max_length=300, blank=True, null=True)
    lastLogon = models.DateTimeField('siste pålogging', null=True, blank=True)
    logonCount = models.IntegerField('Antall pålogginger', null=True)
    name = models.CharField('navn', max_length=255, blank=True, null=True)
    objectGUID = models.CharField(max_length=255, blank=True, null=True)
    objectSid = models.CharField(max_length=255, blank=True, null=True)
    operatingSystem = models.CharField('Operativsystem', max_length=255, blank=True, null=True)
    operatingSystemHotfix = models.CharField(max_length=255, blank=True, null=True)
    operatingSystemServicePack = models.CharField(max_length=255, blank=True, null=True)
    operatingSystemVersion = models.CharField(max_length=255, blank=True, null=True)
    pwdLastSet = models.DateTimeField('passord sist endret', null=True)
    userAccountControl = models.IntegerField(null=True)
    whenChanged = models.DateTimeField('sist endret', null=True)
    whenCreated = models.DateTimeField('opprettet', null=True)

    directory = models.ForeignKey(Directory, on_delete=models.PROTECT)
    last_update = models.DateTimeField('sist oppdatert', auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '%s' % self.name

    def disabled(self):
        return self.userAccountControl & 2 == 2
