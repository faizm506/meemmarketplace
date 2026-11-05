from datetime import date
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, render
from bookings.models import Review
from .models import Tour, Category
def tour_list(request):
    qs = Tour.objects.filter(is_active=True).select_related("category")
    q, cat, mx = request.GET.get("q", "").strip(), request.GET.get("category", ""), request.GET.get("max_price", "")
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(meeting_point__icontains=q))
    if cat:
        qs = qs.filter(category__slug=cat)
    if mx.isdigit():
        qs = qs.filter(price__lte=int(mx))
    return render(request, "tour_list.html", {"tours": qs, "categories": Category.objects.all(), "q": q, "cat": cat, "mx": mx})
def tour_detail(request, slug):
    tour = get_object_or_404(Tour.objects.select_related("category", "partner"), slug=slug, is_active=True)
    if request.GET.get("ref"):
        request.session["ref"] = request.GET["ref"][:20]
    reviews = Review.objects.filter(tour=tour).select_related("user")[:10]
    return render(request, "tour_detail.html", {"tour": tour, "stops": tour.stops.all(), "reviews": reviews,
        "avg": Review.objects.filter(tour=tour).aggregate(a=Avg("rating"))["a"],
        "slots": tour.slots.filter(date__gte=date.today(), remaining__gt=0)[:12]})
