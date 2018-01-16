from django.template.response import TemplateResponse
from mezzanine.blog.models import BlogPost
from mezzanine.conf import settings
from mezzanine.utils.views import paginate


def homepage(request, tag=None, year=None, month=None, category=None, template="index.html"):
  settings.use_editable()
  templates = []
  blog_posts = BlogPost.objects.published(for_user=request.user)
  author = None

  prefetch = ("categories", "keywords__keyword")
  blog_posts = blog_posts.select_related("user").prefetch_related(*prefetch)[:3]
  blog_posts = paginate(blog_posts, request.GET.get("page", 1),
                        settings.BLOG_POST_PER_PAGE,
                        settings.MAX_PAGING_LINKS)

  context = {"blog_posts": blog_posts, "year": year, "month": month, "tag": tag, "category": category,
             "author": author}
  templates.append(template)
  return TemplateResponse(request, templates, context)
