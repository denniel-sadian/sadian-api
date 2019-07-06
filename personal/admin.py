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
                    'image', 'link', 'date_created', 'views')
    search_fields = ('name', 'category', 'language_used')


class AboutMeAdmin(admin.ModelAdmin):
    list_display = ('text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'date_time', 'shorten_content')


class TimelineAdmin(admin.ModelAdmin):
    list_display = ('date', 'title', 'left')
    actions = [rearrange_timelines]


admin.site.register(Project, ProjectAdmin)
admin.site.register(AboutMe, AboutMeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Timeline, TimelineAdmin)
