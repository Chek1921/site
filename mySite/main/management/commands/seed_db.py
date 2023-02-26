from django.core.management.base import BaseCommand, CommandError
from main.models import District


class Command(BaseCommand):
    def add_districts(self):
        districts=["Все","Первый","Второй","Третий"]
        if District.objects.all() != []:
            return
        for district in districts:
            district = District(
                district = district
            )
            district.save()
    

    def handle(self, *args, **options):
        self.add_districts()