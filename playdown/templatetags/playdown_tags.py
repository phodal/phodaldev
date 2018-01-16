from django import template
from mezzanine.blog.models import BlogPost
from mezzanine.core.models import CONTENT_STATUS_DRAFT
from qa.models import Question

register = template.Library()


@register.simple_tag(takes_context=True)
def blog_post_for(context, user):
    if not user:
        return {}

    blog_posts = BlogPost.objects.published().filter(user_id=user.id)[:10]
    return blog_posts


@register.simple_tag(takes_context=True)
def draft_blog_post_for(context, user):
    if not user:
        return {}

    blog_posts = BlogPost.objects.all().filter(user_id=user.id, status=CONTENT_STATUS_DRAFT)
    return blog_posts

@register.simple_tag(takes_context=True)
def question_for(context, user):
    if not user:
        return {}

    questions = Question.objects.all().filter(user_id=user.id)
    return questions
