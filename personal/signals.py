from django.db.models.signals import post_save
from django.core.signals import request_finished
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from .models import Project
from .models import Subscriber

from django.dispatch import Signal

project_created = Signal(providing_args=['project'])


@receiver(project_created)
def notify_subscribers(sender, project, **kwargs):
    if Subscriber.objects.all().count():
        to_emails = set()
        for i in Subscriber.objects.all():
            to_emails.add(i.email)
        subject = 'I have a new program!'
        from_email = settings.DEFAULT_FROM_EMAIL
        message = 'New program!'
        send_mail(subject, message, from_email, to_emails, html_message=f"""
            <h1>Check it here: <a href="https://dsadian.herokuapp.com/detail/{project.id}/">
            {proeject.name}</a></h1>""")


@receiver(post_save, sender=Project)
def notify_subscriberss(sender, **kwargs):
    it_is_new = False
    if not sender.id:
        it_is_new = True
    print('been here')
    sender.save()
    if it_is_new and Subscriber.objects.all().count():
        to_emails = set()
        for i in Subscriber.objects.all():
            to_emails.add(i.email)
        subject = 'I have a new program!'
        from_email = settings.DEFAULT_FROM_EMAIL
        message = 'New program!'
        send_mail(subject, message, from_email, to_emails, html_message=f"""
            <h1>Check it here: <a href="https://dsadian.herokuapp.com/detail/{sender.id}/">
            {sender.name}</a></h1>""")
