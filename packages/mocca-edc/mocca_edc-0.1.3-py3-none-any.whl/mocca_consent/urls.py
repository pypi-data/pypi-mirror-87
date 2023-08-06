from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import mocca_consent_admin

app_name = "mocca_consent"

urlpatterns = [
    path("admin/", mocca_consent_admin.urls),
    path("", RedirectView.as_view(url="admin/"), name="home_url"),
]
