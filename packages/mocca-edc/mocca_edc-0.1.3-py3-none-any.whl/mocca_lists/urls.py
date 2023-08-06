from django.urls import path
from django.views.generic.base import RedirectView

from .admin_site import mocca_lists_admin

app_name = "mocca_lists"

urlpatterns = [
    path("admin/", mocca_lists_admin.urls),
    path("", RedirectView.as_view(url="admin/"), name="home_url"),
]
