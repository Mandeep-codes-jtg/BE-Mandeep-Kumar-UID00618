from django.db import models
from django.core.validators import MinLengthValidator


class Book(models.Model):
    """
    This is model for Book. We use this schema to store
    title and pages information for a book.

    Needed fields:
        - title 
        - pages
    """
    # Define your fields here
    title = models.CharField(max_length=100,validators=[MinLengthValidator(3)])
    pages = models.IntegerField(default=0)
