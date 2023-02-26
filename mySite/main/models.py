from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        
        user = self.model(username = username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.


        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, password, **extra_fields)
    

class District(models.Model):
    district = models.CharField("Район", max_length=100, null=False, blank=False)
    
    def __str__(self):
        return self.district

class Report(models.Model):
    title = models.CharField('Название', max_length=200, null=False, blank=False)
    text = models.TextField('Содержание', null=False, blank=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, default='1')
    address = models.CharField("Адрес", max_length=100, null=False, blank=False)
    vision = models.CharField('Видна ли она админу', max_length=2, default='1')
    a_title = models.CharField('Название ответа', max_length=200, blank=True)
    a_text = models.TextField('Содержание ответа', blank=True)
    time_create = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

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
    time_pay = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.address


class Bill_name(models.Model):
    name = models.CharField("Название", max_length=100, null=False, blank=False)
    unit = models.CharField("Единица измерения", max_length=100, null=False, blank=False)
    default_rate = models.SmallIntegerField("Стандартное значение при создании счетичка", null=False, blank=False)


    def __str__(self):
        return self.name

class Bill_rate(models.Model):
    name = models.CharField("Название тарифа", max_length=100, null=False, blank=False)
    cost = models.FloatField("Тариф", null=False, blank=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, default='1')

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    
    address = models.CharField("Адрес", max_length=100, null=False, blank=False, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, default='1')
    allows = models.CharField("Разрешение", max_length=1, null=False, blank=False, default='1')
    email = models.EmailField("Почта",null=False, blank=False, unique=True)
    want_staff = models.BooleanField("Хочет быть админом", default=False)

    objects = CustomUserManager()
    REQUIRED_FIELDS = []
