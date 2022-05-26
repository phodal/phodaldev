from django import forms
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.utils.html import conditional_escape
from django.forms.utils import flatatt

from mezzanine.conf import settings


class PageDownWidget(forms.Textarea):
    """
    Widget providing Markdown editor using PageDown JavaScript, and live
    preview.
    Live preview can be generated client-side using PageDown, or
    server-side using python-markdown.
    """

    class Media:
        css = {'all': (
            'playdown/css/pagedown.css',
            'mezzanine/css/smoothness/jquery-ui.min.css',)}
        js = ('playdown/pagedown/Markdown.Converter.js',
              'playdown/pagedown/Markdown.Sanitizer.js',
              'playdown/pagedown/Markdown.Editor.js',
              'mezzanine/js/%s' % settings.JQUERY_FILENAME,
              'mezzanine/js/%s' % settings.JQUERY_UI_FILENAME,
              'filebrowser/js/filebrowser-popup.js',
              'playdown/js/jquery.ba-throttle-debounce.min.js',
              'playdown/js/jquery.cookie.js')

    def __init__(self, template=None, *args, **kwargs):
        self.template = template or 'playdown/editor.html'
        super(PageDownWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, renderer=None, attrs=None):
        if value is None:
            value = ''

        final_attrs = self.build_attrs(attrs)

        return mark_safe(render_to_string(self.template, {
            'final_attrs': flatatt(final_attrs),
            'value': conditional_escape(force_str(value)),
            'server_side_preview': settings.PAGEDOWN_SERVER_SIDE_PREVIEW,
        }))


class PlainWidget(forms.Textarea):
    """
    A regular Textarea widget that is compatible with mezzanine richtext.
    """

    class Media:
        pass
