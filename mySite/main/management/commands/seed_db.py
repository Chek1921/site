from django.core.management.base import BaseCommand, CommandError
from main.models import District, Bill_name, Bill_rate


class Command(BaseCommand):
    def add_districts(self):
        districts=["Все","Первый","Второй","Третий"]
        if District.objects.all().exists():
            return
        for district in districts:
            district = District(
                district = district
            )
            district.save()

    def add_bills_name(self):
        names=["Газ","Вода","Электроэнергия"]
        units=["Кубометров","Кубометров","кВт*ч"]
        if Bill_name.objects.all().exists():
            return
        for i in range(len(names)):
            bill_name = Bill_name(
                name = names[i],
                unit = units[i],
                default_rate = i+1
            )
            bill_name.save()
    
    def add_bills_rate(self):
        names=["Для газ","Для воды","Для электроэнергии"]
        costs=[20.04,18.23,22,2]
        if Bill_rate.objects.all().exists():
            return
        for i in range(len(names)):
            bill_rate = Bill_rate(
                name = names[i],
                cost = costs[i]
            )
            bill_rate.save()

    def handle(self, *args, **options):
        self.add_districts()
        self.add_bills_name()
        self.add_bills_rate()