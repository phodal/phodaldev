from __future__ import unicode_literals

import re

from markdown import Extension
from markdown import util
from markdown.blockprocessors import BlockProcessor
from markdown.inlinepatterns import IMAGE_REFERENCE_RE, dequote, handleAttributes, LinkPattern, IMAGE_LINK_RE, \
    ReferencePattern
from markdown.util import etree
from mezzanine.conf import settings


class FigureCaptionProcessor(BlockProcessor):
    IMAGE_REFERENCE_RE_COMPILE = re.compile(IMAGE_REFERENCE_RE)

    def test(self, parent, block):
        is_image = bool(self.IMAGE_REFERENCE_RE_COMPILE.search(block))

        if is_image:
            return True
        else:
            return False

    def run(self, parent, blocks):
        raw_block = blocks.pop(0)
        caption_text = self.IMAGE_REFERENCE_RE_COMPILE.search(raw_block).group(1)

        figure = etree.SubElement(parent, 'figure')
        figure.set('class', 'progressive')

        figure.text = raw_block

        # detail = etree.SubElement(figure, 'a')
        # detail.set("data-rel", "prettyPhoto")
        # detail.set("data-animate", "fadeInUp")
        # detail.text = '查看原图'

        if caption_text != 'enter image description here':
            figcaption_elem = etree.SubElement(figure, 'figcaption')
            figcaption_elem.text = caption_text


class ProgressiveImage(ReferencePattern):
    def __init__(self, pattern, markdown_instance=None):
        super().__init__(pattern, markdown_instance)
        self.pattern = pattern
        self.safe_mode = False
        if markdown_instance:
            self.markdown = markdown_instance

    def makeTag(self, href, title, text):
        from mezzanine.core.templatetags.mezzanine_tags import thumbnail

        el = util.etree.Element("img")

        small_thumbnail_href = settings.MEDIA_URL + thumbnail(href, 30, 0)
        el.set("src", small_thumbnail_href)
        if title:
            el.set("title", title)

        if self.markdown.enable_attributes:
            text = handleAttributes(text, el)

        el.set("alt", self.unescape(text))
        el.set('class', 'img-responsive blog-detail-featured-image progressive__img progressive--not-loaded')
        el.set("data-progressive", self.sanitize_url(href))

        return el


class ProgressiveImageExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add('figure', FigureCaptionProcessor(md.parser), '<ulist')

        ProgressivePattern = ProgressiveImage(IMAGE_REFERENCE_RE, md)
        ProgressivePattern.md = md
        md.inlinePatterns.add('progressiveImage', ProgressivePattern, "<image_reference")


def makeExtension(*args, **kwargs):
    return ProgressiveImageExtension(*args, **kwargs)
