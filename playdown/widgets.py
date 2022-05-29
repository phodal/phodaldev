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
            'mezzanine/css/smoothness/jquery-ui.css')}
        js = ('playdown/pagedown/Markdown.Converter.js',
              'playdown/pagedown/Markdown.Sanitizer.js',
              'playdown/pagedown/Markdown.Editor.js',
              'mezzanine/js/jquery-1.8.3.min.js',
              'mezzanine/js/jquery-ui-1.8.24.min.js',
              'filebrowser/js/filebrowser-popup.js',
              'playdown/js/jquery.ba-throttle-debounce.min.js',
              'playdown/js/jquery.cookie.js')

    # def __init__(self, template=None, *args, **kwargs):
    #     self.template = template or 'playdown/editor.html'
    #     super(PageDownWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, renderer=None, attrs=None):
        if value is None:
            value = ''

        final_attrs = self.build_attrs(self.attrs, attrs, name=name)

        final_id = final_attrs['id'].replace('-', '_')
        del final_attrs['id']

        return mark_safe(render_to_string('playdown/editor.html', {
            'final_attrs': flatatt(final_attrs),
            'field_name': name,
            'id': final_id,
            'value': conditional_escape(force_str(value)),
            'server_side_preview': settings.PAGEDOWN_SERVER_SIDE_PREVIEW,
        }))

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        """
        Helper function for building an attribute dictionary.
        This is combination of the same method from Django<=1.10 and Django1.11+
        """
        attrs = dict(base_attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs


class PlainWidget(forms.Textarea):
    """
    A regular Textarea widget that is compatible with mezzanine richtext.
    """

    class Media:
        pass
