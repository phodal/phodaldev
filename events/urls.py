from __future__ import unicode_literals

from django.conf.urls import include, url
from events import views as events_view

urlpatterns = [
    url("^", events_view.events_list, name="events_list"),
]
