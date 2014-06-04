from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings
import mezzanine_pagedown.urls
from tastypie.api import Api
from blogapi.api import AllBlogSlugResource, BlogResource

apiv1 = Api(api_name='v1')
apiv1.register(BlogResource())
apiv1.register(AllBlogSlugResource())

admin.autodiscover()

urlpatterns = i18n_patterns("",
    ("^admin/", include(admin.site.urls)),
)

if getattr(settings, "PACKAGE_NAME_FILEBROWSER") in settings.INSTALLED_APPS:
    urlpatterns += i18n_patterns("",
        ("^admin/media-library/", include("%s.urls" %
                                        settings.PACKAGE_NAME_FILEBROWSER)),
    )

urlpatterns += patterns('',
    url("^$", direct_to_template, {"template": "index.html"}, name="home"),
    ("^pagedown/", include(mezzanine_pagedown.urls)),
    (r"^api/", include(apiv1.urls)),
    url("^all/$", direct_to_template, {"template": "pages/all.html"},name="all"),
    ("^", include("mezzanine.urls")),
)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
