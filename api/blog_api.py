from django.contrib.auth.models import User
from mezzanine.blog.models import BlogPost
from rest_framework import serializers, viewsets
from rest_framework import filters
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import detail_route, api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import status


class BlogpostListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('title', 'slug', 'id')


class BlogpostListSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.filter(status=2)[:20]
    serializer_class = BlogpostListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'slug')

    @detail_route(renderer_classes=(renderers.StaticHTMLRenderer,))
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

class BlogpostDetailSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SerializerMethodField('get_username_by_id')
    date = serializers.SerializerMethodField('get_special_date')

    @staticmethod
    def get_username_by_id(model):
        user = User.objects.get(id=model.user_id)
        return user.get_full_name()

    @staticmethod
    def get_special_date(model):
        return model.publish_date.strftime('%Y-%m-%d')

    class Meta:
        model = BlogPost
        fields = ('title', 'slug', 'description', 'content', 'id', 'date', 'user')


class BlogpostDetailSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.filter(status=2)
    search_fields = ('title', 'slug')

    def list(self, request):
        queryset = BlogPost.objects.filter(status=2)[:10]

        search_param = self.request.query_params.get('search', None)
        if search_param is not None:
            queryset = BlogPost.objects.filter(title__contains=search_param, status=2)[:10]

        search_param = self.request.query_params.get('search_slug', None)
        if search_param is not None:
            queryset = BlogPost.objects.filter(slug__contains=search_param, status=2)[:10]

        serializer = BlogpostDetailSerializer(queryset, many=True)
        return Response(serializer.data)

class BlogpostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes((IsAuthenticated,))
def create_blog(request):

    serializer = BlogpostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)