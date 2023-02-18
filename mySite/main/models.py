from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

User._meta.get_field('email')._unique = True

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
    def create_user(self, username, password, email, **extra_fields):
        """
        Create and save a user with the given email and password.
        """

        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

class CustomUser(User):
    address = models.CharField("Адрес", max_length=100, null=False, blank=False, unique=True)
    district = models.CharField("Район", max_length=100, null=False, blank=False)
    allows = models.CharField("Разрешение", max_length=1, null=False, blank=False)

    objects = CustomUserManager()