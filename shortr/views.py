from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import RedirectView, TemplateView

from shortr.models import Link


class HomeView(TemplateView):
    """Home page where users can input a URL to shorten."""

    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        long_url = request.POST.get("long_url")
        if not long_url:
            html_error = render_to_string(
                "shortr/_error_message.html", {"error_message": "Long URL is required."}
            )
            return HttpResponse(html_error, status=400)

        link = Link.objects.create(long_url=long_url)
        short_url = request.build_absolute_uri("/") + link.short_code

        html_response = render_to_string(
            "shortr/_shortened_url_display.html", {"short_url": short_url}
        )
        return HttpResponse(html_response, status=201)


class LinkRedirectView(RedirectView):
    """Redirects to the original URL based on the short code."""

    permanent = False  # Use temporary redirect (302) by default

    def get_redirect_url(self, *args, **kwargs):
        short_code = kwargs["short_code"]
        decoded_ids = settings.DEFAULT_SQID.decode(short_code)

        if not decoded_ids:
            raise Http404("Short code not found or invalid.")

        link_id = decoded_ids[0]
        link = get_object_or_404(Link, id=link_id)
        return link.long_url
