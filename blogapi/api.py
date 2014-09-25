import json
import ast

from tastypie.resources import Resource, ModelResource
from django.http.response import HttpResponse
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.cache import SimpleCache
from tastypie import http
from tastypie.serializers import Serializer
from django.conf.urls import url
from tastypie.utils import trailing_slash
from pygeocoder import Geocoder

from mezzanine.blog.models import BlogPost


class BaseCorsResource(Resource):
    """
    Class implementing CORS support for tastypie
    """

    def create_response(self, *args, **kwargs):
        """
        Create the response for a resource. Note this will only
        be called on a GET request, or on a POST request if 
        always_return_data is True
        """
        response = super(BaseCorsResource, self).create_response(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    def post_list(self, request, **kwargs):
        """
        In case of POST make sure we return the Access-Control-Allow Origin
        regardless of returning data
        """
        response = super(BaseCorsResource, self).post_list(request, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Expose-Headers'] = 'Location'
        return response

    def method_check(self, request, allowed=None):
        """
        Check for an OPTIONS request. If so return the Allow- headers
        """
        if allowed is None:
            allowed = []

        request_method = request.method.lower()
        allows = ','.join(map(lambda s: s.upper(), allowed))

        if request_method == 'options':
            response = HttpResponse(allows)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Access-Control-Allow-Methods'] = "GET, PUT, POST, PATCH"
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        if not request_method in allowed:
            response = http.HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        return request_method


class AllBlogSlugResource(BaseCorsResource, ModelResource):
    class Meta:
        queryset = BlogPost.objects.published()
        print queryset
        resource_name = "url"
        fields = ['keywords_string', 'slug', 'title']
        allowed_methods = ['get']
        serializer = Serializer()
        cache = SimpleCache(timeout=10)


class BlogResource(BaseCorsResource, ModelResource):
    class Meta:
        queryset = BlogPost.objects.published()
        resource_name = "blog"
        fields = ['keywords_string', 'slug', 'title', 'content', 'description']
        allowed_methods = ['get']
        serializer = Serializer()
        cache = SimpleCache(timeout=10)


class GeoResource(ModelResource):
    class Meta:
        queryset = BlogPost.objects.published()
        resource_name = 'geo'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        location = ast.literal_eval(json.dumps(dict(request.GET)["location"]))
        objects = {
            "location": (Geocoder.geocode(location).__str__()),
            "coordinates": Geocoder.geocode(location)[0].coordinates
        }

        self.log_throttled_access(request)
        return self.create_response(request, objects)