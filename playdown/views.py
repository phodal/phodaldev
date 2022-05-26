from django.http import HttpResponse
from django.views.generic import View

from playdown.templatetags.playdown_tags import markit


class MarkupPreview(View):
    """
    Renders markdown content to HTML for preview purposes.
    """

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        text = self.request.POST.get('text', u"")
        return HttpResponse(markit(text), content_type='text/html')
