from django.conf import settings
from django.test import TestCase

from shortr.models import Link


class LinkModelTest(TestCase):
    def test_short_code_generation(self):
        """Test that the short_code is generated correctly."""
        link = Link.objects.create(long_url="https://example.com")
        expected_code = settings.DEFAULT_SQID.encode([link.id])
        self.assertEqual(link.short_code, expected_code)

    def test_short_code_determinism(self):
        """Test that the short_code is deterministic for a given ID."""
        link = Link.objects.create(long_url="https://another.com")
        first_code = link.short_code
        second_code = link.short_code
        self.assertEqual(first_code, second_code)

    def test_retrieve_link_by_short_code(self):
        """Test that a Link object can be retrieved using its short_code."""
        original_link = Link.objects.create(long_url="https://test.com/path")
        short_code = original_link.short_code

        # Simulate decoding in a view
        decoded_ids = settings.DEFAULT_SQID.decode(short_code)
        self.assertTrue(decoded_ids)
        retrieved_id = decoded_ids[0]

        retrieved_link = Link.objects.get(id=retrieved_id)
        self.assertEqual(original_link, retrieved_link)
        self.assertEqual(original_link.long_url, retrieved_link.long_url)
