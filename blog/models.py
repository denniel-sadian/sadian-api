from django.db import models
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .signals import article_created


class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.email


class Entry(models.Model):
    STATUS = (
        ('PB', 'Published'),
        ('DR', 'Draft'),
        ('WD', 'Withdrawn')
    )
    headline = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    status = models.CharField(max_length=255, choices=STATUS)
    can_comment = models.BooleanField()
    image = models.URLField(blank=True)
    content = models.TextField()
    preview_content = models.TextField()
    views = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        ordering = ['-pub_date']
    
    def __str__(self):
        return self.headline

    @mark_safe
    def safe_content(self):
        return self.content

    @property
    def comments(self):
        return self.comment_set.all().count()
    
    def increment_views(self):
        self.views += 1
        self.save()

    def save(self, *args, **kwargs):
        first_time = False
        if not self.id:
            first_time = True
        super().save(*args, **kwargs)
        if first_time:
            article_created.send(sender=self.__class__, article=self)


class Comment(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    when = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    objects = models.Manager()

    class Meta:
        ordering = ['when']

    def __str__(self):
        return self.full_name
