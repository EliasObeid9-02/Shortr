from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from shortr.models import Link


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse("shortr:home")

    def test_home_view_get(self):
        """Test that the HomeView renders the correct template on GET request."""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_home_view_post_valid_url(self):
        """Test that HomeView creates a Link and returns a shortened URL on valid POST."""
        long_url = "https://www.example.com"
        response = self.client.post(self.home_url, {"long_url": long_url})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Link.objects.count(), 1)

        link = Link.objects.first()
        self.assertEqual(link.long_url, long_url)

        expected_short_url = (
            self.client.get(self.home_url).wsgi_request.build_absolute_uri("/")
            + link.short_code
        )
        self.assertIn(expected_short_url, response.content.decode())
        self.assertTemplateUsed(response, "shortr/_shortened_url_display.html")

    def test_home_view_post_missing_url(self):
        """Test that HomeView returns an error on POST with missing long_url."""
        response = self.client.post(self.home_url, {"long_url": ""})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Link.objects.count(), 0)
        self.assertIn("Long URL is required.", response.content.decode())
        self.assertTemplateUsed(response, "shortr/_error_message.html")


class LinkRedirectViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.long_url = "https://www.testredirect.com/path"
        self.link = Link.objects.create(long_url=self.long_url)
        self.short_code = self.link.short_code
        self.redirect_url = reverse(
            "shortr:redirect_link", kwargs={"short_code": self.short_code}
        )

    def test_link_redirect_view_valid_short_code(self):
        """Test that LinkRedirectView redirects to the correct long URL."""
        response = self.client.get(self.redirect_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.long_url)

    def test_link_redirect_view_invalid_short_code(self):
        """Test that LinkRedirectView raises Http404 for an invalid short code."""
        invalid_short_code = "invalid"
        invalid_redirect_url = reverse(
            "shortr:redirect_link", kwargs={"short_code": invalid_short_code}
        )

        response = self.client.get(invalid_redirect_url)
        self.assertEqual(response.status_code, 404)

    def test_link_redirect_view_non_existent_short_code(self):
        """Test that LinkRedirectView raises Http404 for a non-existent short code."""
        # Create a short code that doesn't correspond to any existing link ID
        non_existent_id = 999999999  # Assuming this ID won't exist
        non_existent_short_code = settings.DEFAULT_SQID.encode([non_existent_id])
        non_existent_redirect_url = reverse(
            "shortr:redirect_link", kwargs={"short_code": non_existent_short_code}
        )

        response = self.client.get(non_existent_redirect_url)
        self.assertEqual(response.status_code, 404)
