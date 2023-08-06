from datetime import datetime

from django.core.management.base import BaseCommand

from ad_import.load_data import LoadUsers

now = datetime.now()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('directory', nargs='+', type=str)

    def handle(self, *args, **options):
        directory = options['directory'][0]
        load = LoadUsers()
        load.connect(directory)
        for query in load.queries:
            load.load(query)

        inactive = load.get_inactive()
        inactive.delete()
