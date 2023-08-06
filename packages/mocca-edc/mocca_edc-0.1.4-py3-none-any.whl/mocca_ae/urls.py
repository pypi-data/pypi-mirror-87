from django.urls.conf import path
from edc_adverse_event.views import AeHomeView

from .admin_site import mocca_ae_admin

app_name = "mocca_ae"

urlpatterns = [
    path("admin/", mocca_ae_admin.urls),
    path("", AeHomeView.as_view(), name="home_url"),
]
