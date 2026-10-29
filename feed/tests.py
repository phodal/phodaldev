from datetime import datetime, timezone
from xml.etree import ElementTree

from django.test import SimpleTestCase
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed

from feed.feeds import xml_text


class FeedXMLTests(SimpleTestCase):
    def test_generated_feed_values_are_xml_safe(self):
        timestamp = datetime(2026, 10, 29, tzinfo=timezone.utc)
        controls = ''.join(chr(i) for i in range(32) if i not in (9, 10, 13))
        text = '中文 😀\tline\nnext\r<&'
        original = {'title': text + controls, 'description': text + controls,
                    'link': 'https://example.com/post/', 'pubdate': timestamp,
                    'categories': (text + controls,)}
        cleaned = xml_text(original)
        self.assertEqual(cleaned['title'], text)
        self.assertEqual(cleaned['categories'], (text,))
        self.assertEqual(cleaned['pubdate'], timestamp)
        self.assertEqual(original['title'], text + controls)
        for feed_type in (Rss201rev2Feed, Atom1Feed):
            with self.subTest(feed_type=feed_type.__name__):
                feed = feed_type(title='Blog', link='https://example.com/', description='Blog')
                feed.add_item(**cleaned)
                ElementTree.fromstring(feed.writeString('utf-8'))
