from __future__ import unicode_literals

from django.http import Http404

from feed import feeds


def blog_post_feed(request, format, **kwargs):
    """
    Blog posts feeds - maps format to the correct feed view.
    """
    rss, atom = (feeds.FilteredPostsRSS, feeds.FilteredPostsAtom) if kwargs else (feeds.PostsRSS, feeds.PostsAtom)
    feed_class = {"rss": rss, "atom": atom}.get(format)
    if feed_class is None:
        raise Http404()
    return feed_class(**kwargs)(request)
