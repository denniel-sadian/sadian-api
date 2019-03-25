from django.db import models


class Day(models.Model):
    day = models.CharField(max_length=255)
    quote = models.TextField()
    whose = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return self.day
