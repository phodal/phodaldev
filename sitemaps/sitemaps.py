from __future__ import unicode_literals

from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site

from mezzanine.core.models import Displayable
from mezzanine.pages.models import Page, RichTextPage
from mezzanine.utils.sites import current_site_id

from mezzanine.blog.models import BlogPost, BlogCategory


class DisplayableSitemap(Sitemap):
    """
    Sitemap class for Django's sitemaps framework that returns
    all published items for models that subclass ``Displayable``.
    """

    def items(self):
        """
        Return all published items for models that subclass
        ``Displayable``, excluding those that point to external sites.
        """
        return list(Displayable.objects.url_map(in_sitemap=True).values())

    def lastmod(self, obj):
        if isinstance(obj, BlogPost):
            return obj.updated or obj.publish_date

    def changefreq(self, obj):
        if isinstance(obj, BlogPost):
            return "Monthly"
        if isinstance(obj, BlogCategory):
            return "Weekly"
        if isinstance(obj, Page):
            return "Weekly"
        return "Daily"

    def priority(self, obj):
        if isinstance(obj, BlogPost):
            return "0.2"
        if isinstance(obj, BlogCategory):
            return "0.3"
        if isinstance(obj, RichTextPage):
            return "0.6"
        return "1.0"

    def get_urls(self, **kwargs):
        """
        Ensure the correct host by injecting the current site.
        """
        kwargs["site"] = Site.objects.get(id=current_site_id())
        return super(DisplayableSitemap, self).get_urls(**kwargs)
