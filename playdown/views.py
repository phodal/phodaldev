from django.http import HttpResponse
from django.views.generic import View

from playdown.templatetags.playdown_tags import markit
from markdown import markdown

from playdown.plugins.progressiveimage import ProgressiveImageExtension
from playdown.plugins.tables import BlockQuoteExtension


class MarkupPreview(View):
    """
    Renders markdown content to HTML for preview purposes.
    """

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        text = self.request.POST.get('text', u"")
        content = markdown(text,
                           [ProgressiveImageExtension(), 'headerid', 'codehilite', 'extra', 'meta',
                            BlockQuoteExtension()])

        return HttpResponse(content, content_type='text/html')
