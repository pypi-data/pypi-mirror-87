from datetime import datetime

from ad_import.utils.ad_utils import parse_date


class ADObject:
    def __init__(self, user):
        self.object = user[1]
        self.dn = user[0]

    def field(self, field: str):
        if field in self.object:
            return self.object[field][0]

    def string(self, field) -> str:
        try:
            data = self.field(field)
            if data:
                return data.decode('utf-8')
        except UnicodeDecodeError as e:
            print('Error decoding field %s' % field)
            raise e

    def numeric(self, field) -> int:
        try:
            data = self.field(field)
            if data:
                return int(data)
        except ValueError as e:
            print('Error decoding field %s' % field)
            raise e

    def bytes(self, field) -> int:
        if field in self.object:
            return int.from_bytes(self.field(field), 'big')

    def hex(self, field) -> int:
        if field in self.object:
            return int(self.field(field), 16)

    def date(self, field) -> datetime:
        data = self.numeric(field)
        if data:
            return parse_date(data)

    def date_string(self, field) -> datetime:
        data = self.string(field)
        # 2020 09 09 08:56:44.0Z
        if data:
            return datetime.strptime(data, '%Y%m%d%H%M%S.0Z')
