from __future__ import unicode_literals

from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, re_path
from django.views.i18n import set_language

from MK_dream import settings
from homepage import views as homepage_view
from feed import view as feed_view
from amp import views as amp_views
from playdown.views import MarkupPreview
from sitemaps import views as sitemap
from sitemaps.mobile_sitemaps import DisplayableSitemap as DisplayableMobileSitemap
from sitemaps.sitemaps import DisplayableSitemap

admin.autodiscover()

urlpatterns = i18n_patterns(
  path("admin/", include(admin.site.urls)),
)

sitemaps = {"sitemaps": {"all": DisplayableSitemap}}
mobile_sitemaps = {"sitemaps": {"all": DisplayableMobileSitemap}}

urlpatterns += [
  path("sitemap\.xml", sitemap.sitemap, sitemaps),
  path("sitemap_mobile\.xml", sitemap.mobile, sitemaps),
]

urlpatterns += [
  re_path("^feeds/(?P<format>.*)/$", feed_view.blog_post_feed, name="blog_post_feed"),
  re_path("^blog/feeds/(?P<format>.*)/$", feed_view.blog_post_feed, name="blog_post_feed")
]

urlpatterns += [
  path("events/", include("events.urls")),
]

urlpatterns += [
  path("", homepage_view.homepage, name="home"),
  re_path("^amp/(?P<slug>.*)/$", amp_views.amp_blog_post_detail, name="blog_post_detail"),
  path("", include("mezzanine.urls")),
  path("pagedown/preview", MarkupPreview.as_view(), name='preview'),
]

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
