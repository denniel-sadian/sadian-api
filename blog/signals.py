from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import Signal
from django.urls import reverse_lazy

from . import models

article_created = Signal(providing_args=['article'])
subscriber_created = Signal(providing_args=['email'])
comment_created = Signal(
    providing_args=['comments', 'who_commented', 'entry'])


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
            <h1>Read it here: <a href="https://denniel.herokuapp.com{reverse_lazy('blog:detail', kwargs={'pk', article.id})}">
            {article.headline}</a></h1>""")


@receiver(subscriber_created)
def thank_subscriber(sender, email, **kwargs):
    subject = 'Thanks!'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [email]
    contact_message = "Thank you for subscribing, you'll never regret it."
    send_mail(subject, contact_message, from_email, to_email)


@receiver(subscriber_created)
def notify_me(sender, email, **kwargs):
    subject = 'Subscription!'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [from_email]
    contact_message = f'{email} subcribed to your website!'
    send_mail(subject, contact_message, from_email, to_email)


@receiver(comment_created)
def notify_me_and_those_who_commented(sender, comments, who_commented, entry, **kwargs):
    to_emails = {settings.DEFAULT_FROM_EMAIL, }
    for i in comments:
        if i.email != who_commented:
            to_emails.add(i.email)
    subject = 'Sombody commented'
    from_email = settings.DEFAULT_FROM_EMAIL
    contact_message = f"{who_commented} commented!"
    send_mail(subject, contact_message, from_email, to_emails, html_message=f"""
        <h1>{who_commented} commented as well</h1><br/>
        <p>In this article:
        <a href="https://denniel.herokuapp.com{reverse_lazy('blog:detail', kwargs={'pk', entry.id})}">
        {entry.headline}</a></p>""")
