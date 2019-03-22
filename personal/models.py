from django.db import models
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from django.conf import settings

from blog.models import Subscriber
from .signals import project_created


class Project(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    language_used = models.CharField("language(s) used", max_length=255)
    image = models.URLField()
    date_created = models.DateField()
    link = models.URLField(blank=True)
    description = models.TextField()

    objects = models.Manager()

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return self.name

    @property
    def short_description(self):
        return self.description[:80]+'...'
    
    def save(self, *args, **kwargs):
        if not self.id:
            project_created.send(sender=self.__class__, project=self)
        super().save(*args, **kwargs)


class AboutMe(models.Model):
    text = models.TextField()

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'paragraphs about me'

    def safe_text(self):
        return mark_safe(self.text)


class Day(models.Model):
    day = models.CharField(max_length=255)
    quote = models.TextField()
    whose = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return self.day


class Comment(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    date_time = models.DateTimeField()
    content = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.full_name

    def shorten_content(self):
        if len(str(self.content)) < 100:
            return self.content
        return self.content[:100]+'...'


class Timeline(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=255)
    image = models.URLField(blank=True)
    desc = models.TextField("description")
    left = models.BooleanField(default=True)

    objects = models.Manager()
