from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        user = self.model(username = username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password,**extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("allows", '3')

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        return self.create_user(username, password, **extra_fields)
    

class District(models.Model):
    district = models.CharField("Район", max_length=100, null=False, blank=False, unique=True)
    
    def __str__(self):
        return self.district

class ChangeDistict(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    district = models.ForeignKey('District', on_delete=models.CASCADE, default='1')

    def __str__(self):
        return self.user

class Payment(models.Model):
    address = models.CharField("Адрес", max_length=100, null=False, blank=False)
    district = models.CharField("Район", max_length=100, null=False, blank=False)
    name = models.CharField("Имя", max_length=100, null=False, blank=False)
    rate_name = models.CharField("Название тарифа", max_length=100, null=False, blank=False)
    rate_cost = models.FloatField('Стоимость тарифа ',  null=False, blank=False)
    current_count = models.FloatField('Нынешнее значение счетчика',  null=False, blank=False)
    cost = models.FloatField('Для оплаты')
    time_create = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.address + ' : ' + self.name + ' : ' + str(self.time_create)

class Report(models.Model):
    title = models.CharField('Название', max_length=200, null=False, blank=False)
    text = models.TextField('Содержание', null=False, blank=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, default='1')
    address = models.CharField("Адрес", max_length=100, null=False, blank=False)
    vision = models.CharField('Видна ли она админу', max_length=2, default='1')
    a_title = models.CharField('Название ответа', max_length=200, blank=True)
    a_text = models.TextField('Содержание ответа', blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    time_create = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        print(self.vision)
        if self.vision == '2':
            print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
            channel_layer = get_channel_layer()
            username = CustomUser.objects.get(address = self.address).username
            async_to_sync(channel_layer.group_send)(
                'online',
                {
                    'type': 'user_commented',
                    'message': 'На вашу жалобу с названием "' + self.title + '" ответили',
                    'username': username,
                }
            )
        super(Report, self).save(*args, **kwargs)

class New(models.Model):
    title = models.CharField('Название', max_length=200, null=False, blank=False)
    text = models.TextField('Содержание', null=False, blank=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, default='1')
    time_create = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.title

class Bill(models.Model):
    name = models.ForeignKey('Bill_name', on_delete=models.CASCADE)
    last_count = models.FloatField('Последнее оплаченное значение счетчика', null=False, blank=False)
    current_count = models.FloatField('Нынешнее значение счетчика',  null=False, blank=False)
    address = models.CharField("Адрес", max_length=100, null=False, blank=False)
    rate = models.ForeignKey('Bill_rate', on_delete=models.PROTECT)
    cost = models.FloatField('Для оплаты')
    time_pay = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.current_count = round(self.current_count, 2)
        self.cost = round((self.current_count - self.last_count) * self.rate.cost, 2)
        super(Bill, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.address


class Bill_name(models.Model):
    name = models.CharField("Название", max_length=100, null=False, blank=False, unique=True)
    unit = models.CharField("Единица измерения", max_length=100, null=False, blank=False)
    default_rate = models.SmallIntegerField("Стандартное значение при создании счетичка", null=False, blank=False)

    def __str__(self):
        return self.name

class Bill_rate(models.Model):
    name = models.CharField("Название тарифа", max_length=100, null=False, blank=False)
    cost = models.FloatField("Тариф", null=False, blank=False)
    district = models.ForeignKey('District', on_delete=models.CASCADE, default='1')
    bill_name = models.ForeignKey('Bill_name', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __rate__(self):
        return self.cost

class CustomUser(AbstractUser):
    
    address = models.CharField("Адрес", max_length=100, null=False, blank=False, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, default='1')
    allows = models.CharField("Разрешение", max_length=1, null=False, blank=False, default='1')
    email = models.EmailField("Почта",null=False, blank=False, unique=True)
    want_staff = models.BooleanField("Хочет быть админом", default=False)

    objects = CustomUserManager()
    REQUIRED_FIELDS = []