from django.contrib.auth import views as v
from django.urls import path
from core.ratelimit import rate_limit
from . import views
urlpatterns = [
    path("login/", rate_limit("login", 8, 300)(v.LoginView.as_view()), name="login"),
    path("logout/", v.LogoutView.as_view(), name="logout"),
    path("signup/", rate_limit("signup", 6, 600)(views.signup), name="signup"),
]
