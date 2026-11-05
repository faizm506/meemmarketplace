from django.urls import path
<<<<<<< HEAD

from . import views

app_name = "core"
urlpatterns = [
    path("", views.home, name="home"),
    path("waitlist/", views.waitlist, name="waitlist"),
    path("terms/", views.policy("core/terms.html"), name="terms"),
    path("privacy/", views.policy("core/privacy.html"), name="privacy"),
    path("refunds/", views.policy("core/refunds.html"), name="refunds"),
    path("seller-agreement/", views.policy("core/seller_agreement.html"), name="seller_agreement"),
=======
from . import views
from partners.views import widget
urlpatterns = [
    path("", views.home, name="home"), path("health/", views.health, name="health"),
    path("routes/", views.routes, name="routes"),
    path("lang/<str:code>/", views.set_lang, name="set_lang"),
    path("manifest.webmanifest", views.manifest), path("sw.js", views.sw), path("icon.svg", views.icon),
    path("widget/<slug:code>/", widget, name="widget"),
>>>>>>> 45224bb2107e9c064747289981fd5709c63dc9c9
]
