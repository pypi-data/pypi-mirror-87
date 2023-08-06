from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from django.db.models import Model, QuerySet

from ad_import.ad import ADObject, ActiveDirectory
from ad_import.models import Directory, Query, User


class LoadAd(ABC):
    directory: Directory
    model: Model
    fields = []

    def __init__(self):
        self.ad = ActiveDirectory()

    def connect(self, directory_name: str = None, directory: Directory = None):
        if not directory:
            directory = Directory.objects.get(name=directory_name)

        self.directory = directory
        self.ad.connect(dc=directory.dc,
                        username=directory.username,
                        password=directory.password,
                        base_dn=directory.dn,
                        ldaps=directory.ldaps)

    @staticmethod
    def base_dn(query: Query) -> str:
        if query.base_dn:
            return query.base_dn
        else:
            return query.directory.dn

    def get_object(self, entry: ADObject):
        """
        Get django object for a LDAP entry
        Use SID to check for existing objects in database
        :param entry:
        :return:
        """
        try:
            user = self.model.objects.get(directory=self.directory, objectSid=entry.bytes('objectSid'))
            exist = True
        except self.model.DoesNotExist:
            user = self.model(directory=self.directory)
            exist = False

        return user, exist

    @abstractmethod
    def load(self, query: Query):
        pass

    @property
    def queries(self) -> QuerySet[Query]:
        """
        Get queries from the current directory
        :return: Queries
        """
        return self.directory.queries.filter(target=self.model.__module__)

    def run_query(self, query: Query) -> List[ADObject]:
        base_dn = self.base_dn(query)
        return self.ad.ldap_query(query.query,
                                  base_dn,
                                  single_result=False,
                                  subtree=True,
                                  pagination=True,
                                  attributes=self.fields,
                                  result_class=ADObject)

    @staticmethod
    def is_disabled(entry: ADObject):
        if entry.field('userAccountControl') is None:
            return None

        return entry.numeric('userAccountControl') & 2 == 2  # Check if account is disabled

    def get_inactive(self) -> QuerySet:
        return self.model.objects.filter(
            last_update__date__lt=datetime.today().date(),
            directory=self.directory
        )
