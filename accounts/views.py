<<<<<<< HEAD
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from core import emails
from core.security import throttle

from .forms import LoginForm, SignUpForm


class MeemLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


@throttle("signup", 10, 3600)
def signup(request):
    if request.user.is_authenticated:
        return redirect("core:home")
    if request.method == "POST" and request.POST.get("website"):   # honeypot: real people never fill this hidden field
        return redirect("core:home")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        emails.welcome(user)
        messages.success(request, "Welcome to MEEM. Your account is ready.")
        if user.role == "seller":
            return redirect("shops:create")
        return redirect("core:home")
    return render(request, "accounts/signup.html", {"form": form})
=======
from django.contrib.auth import login
from django.shortcuts import redirect, render
from .forms import SignupForm
def signup(request):
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.email = user.email.lower()
        user.role = form.cleaned_data["role"]
        user.save()
        login(request, user)
        return redirect("partner_dashboard" if user.is_partner else "tour_list")
    return render(request, "registration/signup.html", {"form": form})
>>>>>>> 45224bb2107e9c064747289981fd5709c63dc9c9
