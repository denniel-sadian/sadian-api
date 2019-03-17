from django.contrib import admin
from .models import Entry, Comment, Subscriber


def delete_all(model_admin, request, queryset):
    if queryset.count() > 0:
        deleted = 0
        for i in queryset:
            i.delete()
            deleted += 1
        model_admin.message_user(
            request, f'{deleted} item{" has" if deleted is 1 else "s have"} '
                     'been deleted.')


delete_all.short_description = 'Delete all selected'


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class EntryAdmin(admin.ModelAdmin):
    list_display = ('headline', 'pub_date', 'can_comment', 'comments', 'get_status_display', 'id')
    search_fields = ('headline', 'content')
    actions = [delete_all]
    inlines = [CommentInline]


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email',)
    actions = [delete_all]


admin.site.add_action(delete_all, 'delete_all')

admin.site.register(Entry, EntryAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
