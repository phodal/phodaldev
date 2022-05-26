from markdown import markdown

from playdown.plugins.progressiveimage import ProgressiveImageExtension
from playdown.plugins.tables import BlockQuoteExtension


def playdown(content):
    """
    Renders content using markdown extra.
    """
    # return _clean(markdown(content, ['codehilite', 'extra', 'meta']))
    # return _clean(markdown(content, [ProgressiveImageExtension(), 'codehilite', 'extra', 'meta']))
    content = markdown(content, [ProgressiveImageExtension(), 'headerid', 'codehilite', 'extra', 'meta', BlockQuoteExtension()])
    return content
