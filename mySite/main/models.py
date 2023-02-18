from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

class Reports(models.Model):
    title = models.CharField('Название', max_length=200)
    text = models.TextField('Содержание')
    vision = models.CharField('Видна ли она админу', max_length=2)

    def __str__(self):
        return self.title

class Bill(models.Model):
    title = models.CharField('Название', max_length=200)
    counter = models.CharField('Счетчик', max_length=200)
    whos = models.CharField('Чей', max_length=200)

    def __str__(self):
        return self.title

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
    

class CustomUser(AbstractUser):

    address = models.CharField("Адрес", max_length=100, null=False, blank=False, unique=True)
    district = models.CharField("Район", max_length=100, null=False, blank=False)
    allows = models.CharField("Разрешение", max_length=1, null=False, blank=False, default='1')
    email = models.EmailField("Почта",null=False, blank=False, unique=True)

    objects = CustomUserManager()
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email