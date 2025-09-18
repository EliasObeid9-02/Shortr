from django.urls import include, path

urlpatterns = [
    path("", include("shortr.urls")),
]
