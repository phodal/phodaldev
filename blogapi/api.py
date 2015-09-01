from tastypie.resources import Resource, ModelResource, ALL, ALL_WITH_RELATIONS
from django.http.response import HttpResponse
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.cache import SimpleCache
from tastypie import http
from tastypie.serializers import Serializer

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
            response['Access-Control-Allow-Methods'] = "GET"
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
        resource_name = "app"
        fields = ['keywords_string', 'slug', 'title', 'id']
        allowed_methods = ['get']
        serializer = Serializer()
        cache = SimpleCache(timeout=100)
        filtering = {
            'slug': ALL_WITH_RELATIONS,
            'title': ALL_WITH_RELATIONS
        }

class BlogResource(BaseCorsResource, ModelResource):
    class Meta:
        queryset = BlogPost.objects.published()
        resource_name = "blog"
        fields = ['keywords_string', 'slug', 'title', 'content', 'description', 'id']
        allowed_methods = ['get']
        serializer = Serializer()
        cache = SimpleCache(timeout=10)
