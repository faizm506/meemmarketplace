import secrets
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
def make_code():
    return secrets.token_hex(4).upper()
class Hotel(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    commission_pct = models.PositiveSmallIntegerField(default=10)
    def __str__(self):
        return self.name
class Booking(models.Model):
    PENDING, CONFIRMED, CANCELLED = "pending", "confirmed", "cancelled"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    slot = models.ForeignKey("tours.Slot", on_delete=models.PROTECT, related_name="bookings")
    guests = models.PositiveSmallIntegerField()
    total = models.PositiveIntegerField()
    status = models.CharField(max_length=10, default=PENDING)
    code = models.CharField(max_length=12, unique=True, default=make_code)
    ref = models.ForeignKey(Hotel, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created"]
    @property
    def commission(self):
        return self.total * self.ref.commission_pct // 100 if self.ref else 0
    def __str__(self):
        return self.code
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")
    provider = models.CharField(max_length=10)
    provider_ref = models.CharField(max_length=120, blank=True, db_index=True)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=12, default="created")  # created/paid/refund_due/refunded
    created = models.DateTimeField(auto_now_add=True)
class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    tour = models.ForeignKey("tours.Tour", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(max_length=1000, blank=True)
    photo = models.ImageField(upload_to="reviews/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created"]
