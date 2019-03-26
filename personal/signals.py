from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import Signal
from django.urls import reverse_lazy

from blog.models import Subscriber

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
            <h1>Check it here:
            <a href="https://denniel.herokuapp.com{reverse_lazy('personal:index', kwargs={'pk': project.id})}/">
            {project.name}</a></h1>""")
