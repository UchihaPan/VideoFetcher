from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class wall(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.title, self.id)


class Videos(models.Model):
    wall = models.ForeignKey(wall, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    youtube = models.CharField(max_length=200)
    url = models.URLField(max_length=255)

    def __str__(self):
        return '{} {}'.format(self.title, self.id)
