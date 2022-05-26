from __future__ import unicode_literals

from django.http import HttpResponse
from django.template import loader

from events.models import Event


def events_list(request):
    events = Event.objects.published()
    context = {"events": events}
    template = loader.get_template("events/event_list.html")
    return HttpResponse(template.render(context, request))
