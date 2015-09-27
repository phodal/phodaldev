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

@register.inclusion_tag("admin_ads.html", takes_context=True)
def admin_ads(context):
    """
    Dashboard widget for displaying recent comments.
    """
    ads = Ad.objects.all()
    context["ads"] = ads
    return context
