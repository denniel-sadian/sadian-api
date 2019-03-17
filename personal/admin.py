from django.contrib import admin
from personal.models import *


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'language_used',
                    'image', 'link', 'date_created')
    search_fields = ('name', 'category', 'language_used')
    actions = ['delete_selected']


class DayAdmin(admin.ModelAdmin):
    list_display = ('day', 'quote', 'whose')
    actions = ['delete_selected']


class AboutMeAdmin(admin.ModelAdmin):
    list_display = ('text',)
    actions = ['delete_selected']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'date_time', 'shorten_content')
    actions = ['delete_selected']


class TimelineAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'left')
    actions = ['delete_selected']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(AboutMe, AboutMeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Timeline, TimelineAdmin)
