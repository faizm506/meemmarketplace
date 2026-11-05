from django.contrib import admin
from .models import Category, Tour, Stop, Slot
class StopInline(admin.TabularInline):
    model = Stop; extra = 1
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "partner", "price", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("title",)
    inlines = [StopInline]
admin.site.register(Category, admin.ModelAdmin)
admin.site.register(Slot)
