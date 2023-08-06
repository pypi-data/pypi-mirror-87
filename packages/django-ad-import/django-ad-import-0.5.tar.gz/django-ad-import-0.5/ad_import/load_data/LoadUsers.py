from pprint import pprint
from typing import Optional

from ad_import.models import User
from . import LoadAd


class LoadUsers(LoadAd):
    fields = ['accountExpires',
              'cn',
              'company',
              'department',
              'departmentNumber',
              'description',
              'displayName',
              'distinguishedName',
              'employeeID',
              'employeeNumber',
              'givenName',
              'homeDirectory',
              'homeDrive',
              'ipPhone',
              'lastLogon',
              'logonCount',
              'mail',
              'manager',
              'middleName',
              'mobile',
              'name',
              'objectGUID',
              'objectSid',
              'physicalDeliveryOfficeName',
              'pwdLastSet',
              'sAMAccountName',
              'scriptPath',
              'sn',
              'telephoneNumber',
              'title',
              'userAccountControl',
              'userPrincipalName',
              'whenChanged',
              'whenCreated',
              ]

    model = User

    def load_user(self, user_data) -> Optional[User]:
        user, exist = self.get_object(user_data)

        if user_data.field('userAccountControl') is None:
            pprint(user_data.object)
            return

        if user_data.numeric('userAccountControl') & 2 == 2:  # Check if account is disabled
            if not exist:
                print('%s is disabled' % user_data.string('displayName'))
                return

        # user.accountExpires = user_data.date('accountExpires')
        user.cn = user_data.string('cn')
        user.company = user_data.string('company')
        user.department = user_data.string('department')
        user.departmentNumber = user_data.string('departmentNumber')
        user.description = user_data.string('description')
        user.displayName = user_data.string('displayName')
        user.distinguishedName = user_data.string('distinguishedName')
        user.employeeID = user_data.string('employeeID')
        user.employeeNumber = user_data.string('employeeNumber')
        user.givenName = user_data.string('givenName')
        user.homeDirectory = user_data.string('homeDirectory')
        user.homeDrive = user_data.string('homeDrive')
        user.ipPhone = user_data.string('ipPhone')
        user.lastLogon = user_data.date('lastLogon')
        user.logonCount = user_data.numeric('logonCount')
        user.mail = user_data.string('mail')
        user.middleName = user_data.string('middleName')
        user.mobile = user_data.string('mobile')
        user.name = user_data.string('name')
        user.objectGUID = user_data.bytes('objectGUID')
        user.objectSid = user_data.bytes('objectSid')
        user.physicalDeliveryOfficeName = user_data.string('physicalDeliveryOfficeName')
        user.pwdLastSet = user_data.date('pwdLastSet')
        user.sAMAccountName = user_data.string('sAMAccountName')
        user.scriptPath = user_data.string('scriptPath')
        user.sn = user_data.string('sn')
        user.telephoneNumber = user_data.string('telephoneNumber')
        user.title = user_data.string('title')
        user.userAccountControl = user_data.numeric('userAccountControl')
        user.userPrincipalName = user_data.string('userPrincipalName')
        user.whenChanged = user_data.date_string('whenChanged')
        user.whenCreated = user_data.date_string('whenCreated')

        if user.disabled() and not exist:
            print('%s is disabled' % user)
            return
        else:
            manager = user_data.string('manager')
            if manager:
                try:
                    user.manager = User.objects.get(directory=self.directory, distinguishedName=manager)
                except User.DoesNotExist:
                    print('Manager %s does not exist' % manager)

            user.save()

        return user

    def load(self, query):
        entries = self.run_query(query)

        for user_data in entries:
            self.load_user(user_data)
