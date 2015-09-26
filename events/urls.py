from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns("events.views",
    url("^", "events_list", name="events_list"),
)
