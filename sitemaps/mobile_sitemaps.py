from __future__ import unicode_literals

from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site

from mezzanine.core.models import Displayable
from mezzanine.generic.models import Keyword
from mezzanine.pages.models import Page
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
        blogpost_with_page = list(Displayable.objects.url_map(in_sitemap=True).values())
        category = list(BlogCategory.objects.all())
        return blogpost_with_page + category

    @staticmethod
    def lastmod(obj):
        if isinstance(obj, BlogPost):
            return obj.updated or obj.publish_date

    @staticmethod
    def changefreq(obj):
        if isinstance(obj, BlogPost):
            return "Monthly"
        if isinstance(obj, BlogCategory):
            return "Weekly"
        if isinstance(obj, Page):
            return "Weekly"
        return "Daily"

    @staticmethod
    def priority(obj):
        if isinstance(obj, BlogPost):
            return "0.2"
        if isinstance(obj, BlogCategory):
            return "0.3"
        if isinstance(obj, Page):
            return "0.6"
        return "1.0"

    def get_urls(self, **kwargs):
        """
        Ensure the correct host by injecting the current site.
        """
        kwargs["site"] = Site.objects.get(id=current_site_id())
        return super(DisplayableSitemap, self).get_urls(**kwargs)
