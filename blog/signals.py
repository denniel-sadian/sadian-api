from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import Signal

from . import models

article_created = Signal(providing_args=['article'])


@receiver(article_created)
def notify_subscribers(sender, article, **kwargs):
    if models.Subscriber.objects.all().count():
        to_emails = set()
        for i in models.Subscriber.objects.all():
            to_emails.add(i.email)
        subject = 'New Article to read'
        from_email = settings.DEFAULT_FROM_EMAIL
        message = 'New article to read!'
        send_mail(subject, message, from_email, to_emails, html_message=f"""
            <h1>Read it here: <a href="https://dsadian.herokuapp.com/blog/detail/{article.id}/">
            {article.headline}</a></h1>""")
