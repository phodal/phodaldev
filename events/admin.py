from django.contrib import admin
from events.models import Event, Ad


class EventAdmin(admin.ModelAdmin):
    list_display = ('content', 'date', 'location', 'pub_date', 'is_active', 'is_published')
    list_filter = ('is_active',)


class AdAdmin(admin.ModelAdmin):
    list_display = ('content', 'date', 'pub_date', 'is_active', 'is_published')
    list_filter = ('is_active',)

admin.site.register(Event, EventAdmin)
admin.site.register(Ad, AdAdmin)
