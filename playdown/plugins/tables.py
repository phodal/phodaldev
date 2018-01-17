"""
Tables Extension for Python-Markdown
====================================

Added parsing of tables to Python-Markdown.

See <https://Python-Markdown.github.io/extensions/tables>
for documentation.

Original code Copyright 2009 [Waylan Limberg](http://achinghead.com)

All changes Copyright 2008-2014 The Python Markdown Project

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

"""

from __future__ import absolute_import
from __future__ import unicode_literals
import re

from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree

PIPE_NONE = 0
PIPE_LEFT = 1
PIPE_RIGHT = 2


class BlockQuoteProcessor(BlockProcessor):
  RE = re.compile(r'(^|\n)[ ]{0,3}>[ ]?(.*)')

  def test(self, parent, block):
    return bool(self.RE.search(block))

  def run(self, parent, blocks):
    block = blocks.pop(0)
    m = self.RE.search(block)
    if m:
      before = block[:m.start()]  # Lines before blockquote
      # Pass lines before blockquote in recursively for parsing forst.
      self.parser.parseBlocks(parent, [before])
      # Remove ``> `` from begining of each line.
      block = '\n'.join(
        [self.clean(line) for line in block[m.start():].split('\n')]
      )
    sibling = self.lastChild(parent)
    if sibling is not None and sibling.tag == "blockquote":
      # Previous block was a blockquote so set that as this blocks parent
      quote = sibling
    else:
      # This is a new blockquote. Create a new parent element.
      quote = etree.SubElement(parent, 'blockquote')
    # Recursively parse block with blockquote as parent.
    # change parser state so blockquotes embedded in lists use p tags
    self.parser.state.set('blockquote')
    self.parser.parseChunk(quote, block)
    self.parser.state.reset()

  def clean(self, line):
    """ Remove ``>`` from beginning of a line. """
    m = self.RE.match(line)
    if line.strip() == ">":
      return ""
    elif m:
      return m.group(2)
    else:
      return line


class BlockQuoteExtension(Extension):
  def extendMarkdown(self, md, md_globals):
    md.parser.blockprocessors.add('blockquote',
                                  BlockQuoteProcessor(md.parser),
                                  '<hashheader')


def makeExtension(**kwargs):  # pragma: no cover
  return BlockQuoteExtension(**kwargs)
