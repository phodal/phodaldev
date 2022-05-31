from django.http import HttpResponse
from django.views.generic import View

from markdown import markdown

from playdown.plugins.tables import BlockQuoteExtension


class MarkupPreview(View):
    """
    Renders markdown content to HTML for preview purposes.
    """

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        text = self.request.POST.get('text', u"")
        content = markdown(text,
                           ['headerid', 'codehilite', 'extra', 'meta',
                            BlockQuoteExtension()])

        return HttpResponse(content, content_type='text/html')
