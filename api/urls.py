from django.conf.urls import url, include
from rest_framework import routers

from api.blog_api import BlogPostListSet, BlogPostDetailSet
from api.views import AllListView

router = routers.DefaultRouter()
router.register(r'blog_list', BlogPostListSet)
router.register(r'blog_detail', BlogPostDetailSet)

router.register(r'all', AllListView, 'all')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]