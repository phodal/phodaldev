from django.db import models
from mezzanine.core.fields import RichTextField


class Info(models.Model):
    TYPE = (
        ('PWD', 'Program Write Design'),
        ('MORE', 'More Info'),
        ('ABOUT', 'ABOUT'),
        ('OTHER', 'Other'),
    )
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=5, choices=TYPE)
    url = models.CharField(max_length=50)
    slogan = models.CharField(max_length=100)
    content = RichTextField("Content")