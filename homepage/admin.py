from django.contrib import admin
from homepage.models import Info


class InfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'url', 'slogan', 'type')

admin.site.register(Info, InfoAdmin)
