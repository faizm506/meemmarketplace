from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
class SignupForm(UserCreationForm):
    role = forms.ChoiceField(choices=[("tourist", "I'm a traveller"), ("partner", "I'm a guide / partner")])
    class Meta:
        model = User
        fields = ("email", "first_name", "role")
