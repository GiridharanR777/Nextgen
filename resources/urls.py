from django.urls import path

from .views import (
    download_resource_view,
    resource_detail_view,
    resource_list_view,
    upload_resource_view,
)

urlpatterns = [
    path("resources", resource_list_view, name="resources"),
    path("upload", upload_resource_view, name="upload"),
    path("resource/<int:pk>", resource_detail_view, name="resource_detail"),
    path("resource/<int:pk>/download", download_resource_view, name="resource_download"),
]
