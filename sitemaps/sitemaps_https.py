from __future__ import unicode_literals

from .sitemaps import DisplayableSitemap


class DisplayableHTTPSSitemap(DisplayableSitemap):
    """
    Sitemap class for Django's sitemaps framework that returns
    all published items for models that subclass ``Displayable``.
    """

    protocol = 'https'