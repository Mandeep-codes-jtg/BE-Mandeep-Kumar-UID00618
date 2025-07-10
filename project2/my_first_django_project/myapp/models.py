from django.db import models

class Book(models.Model):
    # Define your fields here
    title = models.CharField(max_length=100)
    pages = models.IntegerField(default=0)



