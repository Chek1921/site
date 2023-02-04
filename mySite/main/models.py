from django.db import models

# Create your models here.

class Reports(models.Model):
    title = models.CharField('Название', max_length=200)
    text = models.TextField('Содержание')

    def __str__(self):
        return self.title