from __future__ import unicode_literals

from mezzanine.utils.models import get_user_model
from mezzanine.utils.views import render

from events.models import Event

User = get_user_model()


def events_list(request, template="events/event_list.html"):
    events = Event.objects.published()
    context = {"events": events}
    return render(request, template, context)
