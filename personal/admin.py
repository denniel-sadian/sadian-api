from django.contrib import admin
from personal.models import *


def rearrange_timelines(model_admin, request, queryset):
    if queryset.count() > 0:
        left = False
        for i in queryset.order_by('date'):
            if left:
                left = False
            else:
                left = True
            i.left = left
            i.save()
        model_admin.message_user(
            request, 'They have been rearranged.')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'language_used',
                    'image', 'link', 'date_created')
    search_fields = ('name', 'category', 'language_used')
    actions = ['delete_selected']


class AboutMeAdmin(admin.ModelAdmin):
    list_display = ('text',)
    actions = ['delete_selected']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'date_time', 'shorten_content')
    actions = ['delete_selected']


class TimelineAdmin(admin.ModelAdmin):
    list_display = ('date', 'title', 'left')
    actions = ['delete_selected', rearrange_timelines]


admin.site.register(Project, ProjectAdmin)
admin.site.register(AboutMe, AboutMeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Timeline, TimelineAdmin)
