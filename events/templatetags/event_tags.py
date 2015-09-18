from django import template
from events.models import Event

register = template.Library()


@register.simple_tag(name='events')
def events():
    future_events = Event.objects.future()[:3]
    return future_events