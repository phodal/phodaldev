from hashlib import sha256

from django import template
from django.core.cache import cache
from mezzanine.blog.models import BlogPost
from mezzanine.core.models import CONTENT_STATUS_DRAFT
from markdown import markdown

from playdown.plugins.tables import BlockQuoteExtension

register = template.Library()


@register.simple_tag(takes_context=True)
def blog_post_for(context, user):
    if not user:
        return {}

    blog_posts = BlogPost.objects.published().filter(user_id=user.id)[:10]
    return blog_posts


@register.simple_tag(takes_context=True)
def draft_blog_post_for(context, user):
    if not user:
        return {}

    blog_posts = BlogPost.objects.all().filter(user_id=user.id, status=CONTENT_STATUS_DRAFT)
    return blog_posts

@register.simple_tag(takes_context=True)
def markit(context, content):
    cache_key = "markdown:v1:" + sha256(content.encode("utf-8")).hexdigest()
    rendered = cache.get(cache_key)
    if rendered is None:
        rendered = markdown(content, ['headerid', 'codehilite', 'extra', 'meta', BlockQuoteExtension()])
        cache.set(cache_key, rendered, 3600)
    return rendered
