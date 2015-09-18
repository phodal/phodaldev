from mezzanine import template
from events.models import Event

register = template.Library()


@register.as_tag
def events():
    future_events = Event.objects.future()[:3]
    return future_events