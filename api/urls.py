from django.conf.urls import url, include
from rest_framework import routers
from api.blog_api import BlogpostListSet, BlogpostDetailSet, create_blog
from api.event_api import EventSet, create_event
from rest_framework_jwt.views import obtain_jwt_token

router = routers.DefaultRouter()
router.register(r'blog_list', BlogpostListSet)
router.register(r'blog_detail', BlogpostDetailSet)
router.register(r'event', EventSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^blog/$', create_blog),
    url(r'^create/$', create_event),
    url(r'^api-auth/', obtain_jwt_token)
]
