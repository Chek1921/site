from django.core.management.base import BaseCommand, CommandError
from main.models import CustomUser, District, Bill, Bill_name, Bill_rate


class Command(BaseCommand):
    def add_users(self):
        for i in range(40):
            user = CustomUser(
                username = 'login'+str(i),
                email = 'email'+str(i)+"@qqq.qq",                
                password = 'Qwe123123',
                district = District.objects.get(id = 2),
                address = 'ул. Ермекова '+str(i)+' дом '+str(i+10),
                allows = '1',
            )
            bill = Bill(
                name = Bill_name.objects.get(id=1),
                last_count = 100,
                current_count = 110,
                address = user.address,
                rate = Bill_rate.objects.get(id = Bill_name.objects.get(id=1).default_rate),
                cost = 0,
            )

            user.save()
            bill.save()
    

    def handle(self, *args, **options):
        self.add_users()