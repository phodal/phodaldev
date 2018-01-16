import warnings
from functools import wraps

from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils import six

def x_robots_tag(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        response['X-Robots-Tag'] = 'noindex, noodp, noarchive'
        return response
    return inner

@x_robots_tag
def mobile(request, sitemaps, section=None,
           template_name='sitemap.xml', content_type='application/xml',
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
