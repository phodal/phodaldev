from mezzanine import template
from homepage.models import Info

register = template.Library()


@register.as_tag
def about():
    about = Info.objects.get(type="ABOUT")
    print about.content
    return about