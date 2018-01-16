from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.utils.html import conditional_escape
from django.utils.encoding import force_text
from django import VERSION as DJANGO_VERSION
if DJANGO_VERSION < (1, 8):
    from django.forms.util import flatatt
else:
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
                'mezzanine_pagedown/css/pagedown.css',
                'mezzanine/css/smoothness/jquery-ui-1.9.1.custom.min.css',)}
        js = ('mezzanine_pagedown/pagedown/Markdown.Converter.js',
              'mezzanine_pagedown/pagedown/Markdown.Sanitizer.js',
              'mezzanine_pagedown/pagedown/Markdown.Editor.js',
              'mezzanine/js/%s' % settings.JQUERY_FILENAME,
              'mezzanine/js/%s' % settings.JQUERY_UI_FILENAME,
              'filebrowser/js/filebrowser-popup.js',
              'mezzanine_pagedown/js/jquery.ba-throttle-debounce.min.js',
              'mezzanine_pagedown/js/jquery.cookie.js')

    def __init__(self, template=None, *args, **kwargs):
        self.template = template or 'mezzanine_pagedown/editor.html'

        super(PageDownWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs={}):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        final_id = final_attrs['id'].replace('-', '_')
        del final_attrs['id']
        return mark_safe(render_to_string(self.template, {
            'final_attrs': flatatt(final_attrs),
            'value': conditional_escape(force_text(value)),
            'id': final_id,
            'server_side_preview': settings.PAGEDOWN_SERVER_SIDE_PREVIEW,
        }))

class PlainWidget(forms.Textarea):
    """
    A regular Textarea widget that is compatible with mezzanine richtext.
    """

    class Media:
        pass
