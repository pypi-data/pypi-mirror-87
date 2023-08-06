from django.urls import path
from django.views.generic.base import RedirectView

from .admin_site import mocca_export_admin

app_name = "mocca_export"

urlpatterns = [
    path("admin/", mocca_export_admin.urls),
    path("", RedirectView.as_view(url="admin/"), name="home_url"),
]
