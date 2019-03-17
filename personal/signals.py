from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from .models import Project
from .models import Subscriber


@receiver(pre_save, sender=Project)
def notify_subscribers(sender, **kwargs):
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
