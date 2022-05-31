from markdown import markdown

from playdown.plugins.tables import BlockQuoteExtension


def playdown(content):
    """
    Renders content using markdown extra.
    """
    content = markdown(content, ['headerid', 'codehilite', 'extra', 'meta', BlockQuoteExtension()])
    return content
