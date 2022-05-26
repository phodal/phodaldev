from __future__ import unicode_literals

from django.urls import path

from events import views as events_view

urlpatterns = [
    path("^", events_view.events_list, name="events_list"),
]
