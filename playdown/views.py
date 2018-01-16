from time import time

from django.contrib.auth.models import AnonymousUser
from django.contrib.messages import info
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt
from django.views.generic import FormView
from mezzanine.blog.models import BlogPost
from mezzanine.core.models import CONTENT_STATUS_DRAFT
from mezzanine.core.templatetags.mezzanine_tags import richtext_filters
from slugify import slugify

from playdown.forms import PlayForm


class PlayCreate(FormView):
    """
    Renders markdown content to HTML for preview purposes.
    """
    form_class = PlayForm
    template_name = 'blog/new.html'
    http_method_names = ['get', 'post', 'put']

    def form_valid(self, form):
        form.save(commit=True)
        return super(PlayForm, self).form_valid(form)

    def get(self, request):
        user = request.user
        if user is None or isinstance(user, AnonymousUser):
            info(request, '用户未登录')
            return redirect("/accounts/login")

        has_blogpost_permission = request.user.has_perm('add_blogpost')  # False
        if not has_blogpost_permission:
            info(request, '当前用户暂无创建玩法权限')

        return TemplateResponse(request, 'blog/new.html')

    def post(self, request, *args, **kwargs):
        if not (request.user.is_authenticated() and request.user.has_perm('blog.add_blogpost')):
            info(request, '权限不足')
            return redirect("/play/new")

        title = self.request.POST.get('title', u"")
        content = self.request.POST.get('content', u"")
        slug = "play-" + slugify(title) + "-".join(str(time()).split("."))[8:]
        blogpost = BlogPost.objects.create(title=title, slug=slug,
                                content=content, user=self.request.user, status=CONTENT_STATUS_DRAFT)

        info(request, '文章进入审核状态中')
        return redirect("/play/" + blogpost.slug)


class PlayEdit(FormView):
    def get_context_data(self, **kwargs):
        context = super(PlayEdit, self).get_context_data(**kwargs)
        if self.object:
            print(self.object)

        return context

    def get(self, request, slug, extra_context=None):

        blog_posts = BlogPost.objects.published(for_user=request.user).select_related()
        blog_post = get_object_or_404(blog_posts, slug=slug)
        context = {"blog_post": blog_post}
        context.update(extra_context or {})
        return TemplateResponse(request, 'blog/new.html', context)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if not (request.user.is_authenticated() and request.user.has_perm('blog.change_blogpost')):
            info(request, '权限不足')
            return redirect("/play/new")

        title = self.request.POST.get('title', u"")
        content = self.request.POST.get('content', u"")
        slug = self.request.POST.get('slug', u"")

        blog_posts = BlogPost.objects.published(for_user=request.user).select_related()
        blog_post = get_object_or_404(blog_posts, slug=slug)
        blog_post.title = title
        blog_post.content = content
        blog_post.save()

        info(request, '文章进入审核状态中')
        return redirect("/play/" + slug)