<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "MEEM Admin"
admin.site.site_title = "MEEM Admin"
admin.site.index_title = "Run the marketplace"

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("shops/", include("shops.urls")),
    path("catalog/", include("catalog.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("payments/", include("payments.urls")),
    path("impact/", include("donations.urls")),
    path("", include("core.urls")),
]
=======
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("", include("accounts.urls")),
    path("tours/", include("tours.urls")),
    path("", include("bookings.urls")),
    path("partner/", include("partners.urls")),
]

>>>>>>> 45224bb2107e9c064747289981fd5709c63dc9c9
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
