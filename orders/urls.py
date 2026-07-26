from django.contrib import admin
from django.urls import include, path
from ordering_system.views import landing_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("orders/", include("ordering_system.urls")),
    path("", landing_page, name="landing-page"),
]
