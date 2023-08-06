from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import mocca_screening_admin

app_name = "mocca_screening"

urlpatterns = [
    path("admin/", mocca_screening_admin.urls),
    path("", RedirectView.as_view(url="/mocca_screening/admin/"), name="home_url"),
]
