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
