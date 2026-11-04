from django.urls import path
from . import views
from partners.views import widget
urlpatterns = [
    path("", views.home, name="home"), path("health/", views.health, name="health"),
    path("routes/", views.routes, name="routes"),
    path("lang/<str:code>/", views.set_lang, name="set_lang"),
    path("manifest.webmanifest", views.manifest), path("sw.js", views.sw), path("icon.svg", views.icon),
    path("widget/<slug:code>/", widget, name="widget"),
]
