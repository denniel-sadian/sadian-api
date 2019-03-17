from django.db import models
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


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

    objects = models.Manager()

    class Meta:
        ordering = ['-pub_date']

    @mark_safe
    def safe_content(self):
        return self.content

    @property
    def comments(self):
        return self.comment_set.all().count()

    def __str__(self):
        return self.headline

    def save(self, *args, **kwargs):
        it_is_new = False
        if not self.id:
            it_is_new = True
        super().save(*args, **kwargs)
        if it_is_new and Subscriber.objects.all().count():
            to_emails = set()
            for i in Subscriber.objects.all():
                to_emails.add(i.email)
            subject = 'New Article to read'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = 'New article to read!'
            send_mail(subject, message, from_email, to_emails, html_message=f"""
                <h1>Read it here: <a href="https://dsadian.herokuapp.com/blog/detail/{self.id}/">
                {self.headline}</a></h1>
            """)


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
