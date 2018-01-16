from django.db import models
from django.forms import fields

from mezzanine_pagedown.widgets import PageDownWidget


class MarkdownTextField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {'form_class': RichTextFormField}
        defaults.update(kwargs)
        return super(MarkdownTextField, self).formfield(**defaults)


class MarkdownTextFormField(fields.Field):
    def __init__(self, template=None, *args, **kwargs):
        kwargs.update({'widget': PageDownWidget(template)})
        super(MarkdownTextFormField, self).__init__(*args, **kwargs)
