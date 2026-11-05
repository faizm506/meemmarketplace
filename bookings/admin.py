from django.contrib import admin
from .models import Booking, Payment, Review, Hotel
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("code", "user", "slot", "total", "status", "ref", "commission")
    list_filter = ("status", "ref")
admin.site.register(Payment, admin.ModelAdmin)
admin.site.register(Review, admin.ModelAdmin)
admin.site.register(Hotel, admin.ModelAdmin)
