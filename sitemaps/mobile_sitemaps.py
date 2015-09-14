from __future__ import unicode_literals
import warnings

from django.contrib.sitemaps.views import x_robots_tag
from django.contrib.sites.models import get_current_site
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template.response import TemplateResponse
import six
from .sitemaps import DisplayableSitemap


class DisplayableSitemap(DisplayableSitemap):
    """
    Sitemap class for Django's sitemaps framework that returns
    all published items for models that subclass ``Displayable``.
    """

    @x_robots_tag
    def sitemap(request, sitemaps, section=None,
                template_name='sitemap_mobile.xml', content_type='application/xml',
                mimetype=None):

        if mimetype:
            warnings.warn("The mimetype keyword argument is deprecated, use "
                "content_type instead", DeprecationWarning, stacklevel=2)
            content_type = mimetype

        req_protocol = 'https' if request.is_secure() else 'http'
        req_site = get_current_site(request)

        if section is not None:
            if section not in sitemaps:
                raise Http404("No sitemap available for section: %r" % section)
            maps = [sitemaps[section]]
        else:
            maps = list(six.itervalues(sitemaps))
        page = request.GET.get("p", 1)

        urls = []
        for site in maps:
            try:
                if callable(site):
                    site = site()
                urls.extend(site.get_urls(page=page, site=req_site,
                                          protocol=req_protocol))
            except EmptyPage:
                raise Http404("Page %s empty" % page)
            except PageNotAnInteger:
                raise Http404("No page '%s'" % page)
        return TemplateResponse(request, template_name, {'urlset': urls},
                                content_type=content_type)
