from django.urls import path

from .views import HomeView, LinkRedirectView

app_name = "shortr"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("<str:short_code>/", LinkRedirectView.as_view(), name="redirect_link"),
]
