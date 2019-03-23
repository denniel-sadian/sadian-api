from django.contrib import admin

from .models import Day


class DayAdmin(admin.ModelAdmin):
    list_display = ('day', 'quote', 'whose')
    actions = ['delete_selected']


admin.site.register(Day, DayAdmin)
