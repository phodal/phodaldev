import itertools

from django.contrib.auth.models import User
from mezzanine.blog.models import BlogPost
from rest_framework import serializers, viewsets
from rest_framework.response import Response

class AllSerializer(serializers.Serializer):
    model = serializers.SerializerMethodField('get_model_name')
    user = serializers.SerializerMethodField('get_username_by_id')
    title = serializers.CharField()
    pk = serializers.CharField()
    slug = serializers.CharField()
    publish_date = serializers.CharField()
    date = serializers.SerializerMethodField('get_special_date')

    @staticmethod
    def get_model_name(model):
        model = str(model.__class__.__name__).lower()
        if model == 'blogpost':
            model = 'blog'
        return model

    @staticmethod
    def get_username_by_id(model):
        user = User.objects.get(id=model.user_id)
        return user.get_full_name()


    @staticmethod
    def get_special_date(model):
        return model.publish_date.strftime('%Y-%m-%d')

class AllListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = AllSerializer

    def get_paginate_by(self):
        if self.request.accepted_renderer.format == 'html':
            return 20
        return 10

    def list(self, request):
        queryset = BlogPost.objects.filter(status=2)[:10]

        search_param = self.request.query_params.get('search', None)
        if search_param is not None:
            blog_queryset = BlogPost.objects.filter(title__contains=search_param)[:5]
            queryset = blog_queryset[:10]

        homepage = self.request.query_params.get('homepage', None)
        if homepage is not None:
            blog_queryset = BlogPost.objects.all()[:5]
            queryset = list(itertools.chain(blog_queryset))

        serializer = AllSerializer(queryset, many=True)
        return Response(serializer.data)