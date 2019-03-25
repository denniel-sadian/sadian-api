from django import template
from django.utils import timezone
from django.conf import settings

from ..models import Day

register = template.Library()


@register.simple_tag
def current_year():
    return timezone.datetime.now().year


@register.simple_tag
def current_week_name():
    return timezone.datetime.now().strftime('%A')


@register.simple_tag
def current_day(what):
    day = Day.objects.get(id=timezone.datetime.now().isoweekday())
    if what == 'quote':
        return day.quote
    elif what == 'by':
        return day.whose


@register.simple_tag
def profile_picture():
    return settings.PROFILE_PICTURE
