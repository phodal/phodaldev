from tastypie.resources import ModelResource
from mezzanine.blog.models import BlogPost, BlogCategory


class AllBlogSlugResource(ModelResource):
    class Meta:
        queryset = BlogPost.objects.published()
        resource_name = "url"
        fields = ['keywords_string', 'slug', 'title']
        allowed_methods = ['get']


class BlogResource(ModelResource):
    class Meta:
        queryset = BlogPost.objects.published()
        resource_name = "blog"
        fields = ['keywords_string', 'slug', 'title', 'content', 'description']
        allowed_methods = ['get']
