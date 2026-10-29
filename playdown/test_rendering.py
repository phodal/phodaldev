from django.core.cache import cache
from django.test import SimpleTestCase, override_settings

from playdown.templatetags.playdown_tags import markit


@override_settings(CACHES={'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    'LOCATION': 'markdown-rendering-test',
}})
class MarkdownRenderingTests(SimpleTestCase):
    def test_repeated_content_and_edits(self):
        cache.clear()
        first = markit({}, '# Original 中文')
        self.assertIn('Original 中文', first)
        self.assertEqual(markit({}, '# Original 中文'), first)
        changed = markit({}, '# Updated 中文')
        self.assertIn('Updated 中文', changed)
        self.assertNotEqual(changed, first)
        self.assertEqual(markit({}, '# Original 中文'), first)
