from __future__ import unicode_literals

from django.http import Http404
import feeds


def blog_post_feed(request, format, **kwargs):
    """
    Blog posts feeds - maps format to the correct feed view.
    """
    try:
        return {"rss": feeds.PostsRSS, "atom": feeds.PostsAtom}[format](**kwargs)(request)
    except KeyError:
        raise Http404()