import bleach
from bleach import clean
from markdown import markdown
from mezzanine.conf import settings
from playdown.plugins.progressiveimage import ProgressiveImageExtension
from playdown.plugins.tables import TableExtension


def _clean(html):
    tags =  bleach.ALLOWED_TAGS + settings.RICHTEXT_ALLOWED_TAGS
    attrs = settings.RICHTEXT_ALLOWED_ATTRIBUTES
    styles = settings.RICHTEXT_ALLOWED_STYLES
    return clean(html, tags=tags, attributes=attrs, strip=True,
                 strip_comments=False, styles=styles)


def playdown(content):
    """
    Renders content using markdown extra.
    """
    # return _clean(markdown(content, ['codehilite', 'extra', 'meta']))
    # return _clean(markdown(content, [ProgressiveImageExtension(), 'codehilite', 'extra', 'meta']))
    return markdown(content, [ProgressiveImageExtension(), 'headerid', 'codehilite', 'extra', 'meta', TableExtension()])
