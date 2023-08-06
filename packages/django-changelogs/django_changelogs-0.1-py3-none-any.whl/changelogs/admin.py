from django.contrib import admin
from .models import *


class LogEntryAdmin(admin.ModelAdmin):
    model = LogEntry
    list_display = ['title', 'action', 'version']
    readonly_fields = ['version']

    def get_queryset(self, request):
        return LogEntry.objects.all()

class ChangelogAdmin(admin.ModelAdmin):
    model = Changelog
    actions = ['publish']
    list_display = ['title', 'version', 'published', 'created_at', 'items_count']

    def get_queryset(self, request):
        return Changelog.objects.all().prefetch_related('items')
    
    def items_count(self, instance):
        return instance.items.count()

    def publish(self, request, qs):
        qs.update(published=True)
    publish.short_description = 'Publish selected Changelogs'


admin.site.register(Changelog, ChangelogAdmin)
admin.site.register(LogEntry, LogEntryAdmin)

