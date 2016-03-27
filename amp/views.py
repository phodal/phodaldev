from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from mezzanine.blog.models import BlogPost


def amp_blog_post_detail(request, slug, year=None, month=None, day=None,
                     template="blog/amp_blog_post_detail.html",
                     extra_context=None):

    blog_posts = BlogPost.objects.published(
        for_user=request.user).select_related()
    blog_post = get_object_or_404(blog_posts, slug=slug)
    related_posts = blog_post.related_posts.published(for_user=request.user)
    context = {"blog_post": blog_post, "editable_obj": blog_post,
               "related_posts": related_posts, "slug": slug}
    context.update(extra_context or {})
    templates = [u"blog/amp_blog_post_detail_%s.html" % str(slug), template]
    return TemplateResponse(request, templates, context)

