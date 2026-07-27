from django.contrib import admin
from django.urls import include, path
from pizzas.views import landing_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("pizzas/", include("pizzas.urls")),
    path("", landing_page, name="landing-page"),
]
