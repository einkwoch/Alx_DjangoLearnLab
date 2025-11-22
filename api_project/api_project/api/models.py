from django.db import models

# Create your models here.
class Person(models.Model):
    title = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    