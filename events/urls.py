from __future__ import unicode_literals

from django.urls import re_path

from events import views as events_view

urlpatterns = [
    re_path("", events_view.events_list, name="events_list"),
]
