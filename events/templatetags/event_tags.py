from mezzanine import template
from events.models import Event, Ad

register = template.Library()


@register.as_tag
def events():
    future_events = Event.objects.future()[:3]
    return future_events


@register.as_tag
def ads():
    current_ad = Ad.objects.future()[:1]
    return current_ad
