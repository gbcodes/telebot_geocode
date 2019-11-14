from django.db import models, connections


class Area(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Result(models.Model):

    request = models.CharField(max_length=50)
    result = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)

