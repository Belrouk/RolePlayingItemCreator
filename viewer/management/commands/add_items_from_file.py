from django.core.management.base import BaseCommand
import pickledb
import ast
from viewer.models import MagicalItem


class Command(BaseCommand):
    help = 'loads in custom magical items for testing'

    def handle(self, *args, **options):
        file_name = "viewer/tests/test_data/MagicalItemDatabase.db"
        db = pickledb.load(file_name, True)

        for item in db.getall():
            item = ast.literal_eval(str(db.get(item)))
            m = MagicalItem()
            m.name = str(item[U'Name'])
            m.slot = str(item[u'Slot'])
            m.rarity = str(item[u'Rarity'])
            m.value = str(item[u'Value'])
            m.attunement = str(item[u'Attunement'])
            m.benefits = str(item[u'Benefits'])
            m.description = str(item[u'Description'])
            m.save()
