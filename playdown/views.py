from django.http import HttpResponse
from django.views.generic import View

from mezzanine.core.templatetags.mezzanine_tags import richtext_filters


class MarkupPreview(View):
    """
    Renders markdown content to HTML for preview purposes.
    """

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        text = self.request.POST.get('text', u"")
        return HttpResponse(richtext_filters(text), content_type='text/html')
