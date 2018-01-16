from django.conf.urls import url

from .views import PlayCreate

urlpatterns = [
    url(r'^', PlayCreate.as_view(), name='play'),
]
