from django.conf.urls import url, include
from rest_framework import routers

from api.blog_api import BlogpostListSet, BlogpostDetailSet, create_blog
from api.views import AllListView

router = routers.DefaultRouter()
router.register(r'blog_list', BlogpostListSet)
router.register(r'blog_detail', BlogpostDetailSet)

router.register(r'all', AllListView, 'all')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^blog/$', create_blog),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]