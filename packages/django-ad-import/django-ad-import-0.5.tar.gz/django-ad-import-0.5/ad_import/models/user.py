from django.db import models

from . import Directory


class User(models.Model):
    accountExpires = models.DateTimeField('konto utløper', null=True)
    cn = models.CharField('fullt navn', max_length=255, blank=True, null=True)
    company = models.CharField('firma', max_length=255, blank=True, null=True)
    department = models.CharField('avdeling', max_length=255, blank=True, null=True)
    departmentNumber = models.CharField('avdelingsnummer', max_length=255, blank=True, null=True)
    description = models.CharField('beskrivelse', max_length=255, blank=True, null=True)
    displayName = models.CharField('visningsnavn', max_length=255, blank=True, null=True)
    distinguishedName = models.CharField('DN', max_length=300, blank=True, null=True)
    employeeID = models.CharField(max_length=255, blank=True, null=True)
    employeeNumber = models.CharField(max_length=255, blank=True, null=True)
    givenName = models.CharField('fornavn', max_length=255, blank=True, null=True)
    homeDirectory = models.CharField(max_length=255, blank=True, null=True)
    homeDrive = models.CharField(max_length=255, blank=True, null=True)
    ipPhone = models.CharField('IP-telefon', max_length=255, blank=True, null=True)
    lastLogon = models.DateTimeField('siste pålogging', null=True, blank=True)
    logonCount = models.IntegerField('Antall pålogginger', null=True)
    mail = models.EmailField('Epostadresse', null=True)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Leder', null=True)
    middleName = models.CharField('mellomnavn', max_length=255, blank=True, null=True)
    mobile = models.CharField('mobil', max_length=255, blank=True, null=True)
    name = models.CharField('Navn', max_length=255, blank=True, null=True)
    objectGUID = models.CharField(max_length=255, blank=True, null=True)
    objectSid = models.CharField(max_length=255, blank=True, null=True)
    physicalDeliveryOfficeName = models.CharField('Lokasjon', max_length=255, blank=True, null=True)
    pwdLastSet = models.DateTimeField('passord sist endret', null=True)
    sAMAccountName = models.CharField('brukernavn', max_length=255, blank=True, null=True)
    scriptPath = models.CharField(max_length=255, blank=True, null=True)
    sn = models.CharField('etternavn', max_length=255, blank=True, null=True)
    telephoneNumber = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    userAccountControl = models.IntegerField(null=True)
    userPrincipalName = models.CharField(max_length=255, blank=True, null=True)
    whenChanged = models.DateTimeField('sist endret', null=True)
    whenCreated = models.DateTimeField('opprettet', null=True)

    directory = models.ForeignKey(Directory, on_delete=models.PROTECT, related_name='users')
    last_update = models.DateTimeField('sist oppdatert', auto_now=True)

    def __str__(self):
        return '%s' % self.displayName

    def disabled(self):
        return self.userAccountControl & 2 == 2