from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
<<<<<<< HEAD

from .models import User


@admin.register(User)
class MeemUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff", "date_joined")
    list_filter = ("role", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (("MEEM", {"fields": ("role", "phone")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("MEEM", {"fields": ("email", "role", "phone")}),)
=======
from .models import User
@admin.register(User)
class Admin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "first_name", "role", "is_staff")
    fieldsets = ((None, {"fields": ("email", "password")}), ("Info", {"fields": ("first_name", "last_name", "role")}),
                 ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}))
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2", "role")}),)
    search_fields = ("email",)
>>>>>>> 45224bb2107e9c064747289981fd5709c63dc9c9
