from django.urls import path
from . import views
urlpatterns = [path("", views.dashboard, name="partner_dashboard"), path("tour/new/", views.new_tour, name="new_tour")]
