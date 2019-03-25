from django import template
from django.template.loader import get_template

from ..models import Project

register = template.Library()


@register.inclusion_tag(get_template('personal/project_categories.html'))
def categories(current_category):
    categories = []
    for project in Project.objects.all():
        if project.category not in categories:
            categories.append(project.category)
    return {'categories': categories, 'category': current_category}
