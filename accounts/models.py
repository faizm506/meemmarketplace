from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
class UserManager(BaseUserManager):
    use_in_migrations = True
    def _make(self, email, password, **extra):
        if not email:
            raise ValueError("Email required")
        user = self.model(email=self.normalize_email(email).lower(), **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None, **extra):
        extra.setdefault("is_staff", False); extra.setdefault("is_superuser", False)
        return self._make(email, password, **extra)
    def create_superuser(self, email, password=None, **extra):
        extra.update(is_staff=True, is_superuser=True, role="admin")
        return self._make(email, password, **extra)
class User(AbstractUser):
    TOURIST, PARTNER, ADMIN = "tourist", "partner", "admin"
    ROLES = [(TOURIST, "Tourist"), (PARTNER, "Partner"), (ADMIN, "Admin")]
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLES, default=TOURIST)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
    @property
    def is_partner(self):
        return self.role == self.PARTNER
    def __str__(self):
        return self.email
