from django.conf.urls import url, include
from rest_framework import routers
from api.blog_api import BlogpostListSet, BlogpostDetailSet, create_blog
from api.event_api import EventSet, create_event

router = routers.DefaultRouter()
router.register(r'blog_list', BlogpostListSet)
router.register(r'blog_detail', BlogpostDetailSet)
router.register(r'event', EventSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^blog/$', create_blog),
    url(r'^create/$', create_event),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]