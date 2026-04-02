from django.urls import path

from .views import requests_view

urlpatterns = [
    path("requests", requests_view, name="requests"),
]
