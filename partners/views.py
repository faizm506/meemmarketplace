from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.shortcuts import redirect, render
from bookings.models import Booking
from .forms import TourForm, SlotForm
def partner_only(view):
    @login_required
    def wrapped(request, *a, **kw):
        if not request.user.is_partner:
            raise PermissionDenied
        return view(request, *a, **kw)
    return wrapped
@partner_only
def dashboard(request):
    u = request.user
    bookings = Booking.objects.filter(slot__tour__partner=u, status="confirmed").select_related("slot__tour", "user")
    slot_form = SlotForm(request.POST or None, partner=u, prefix="s")
    if request.method == "POST" and slot_form.is_valid():
        s = slot_form.save(commit=False); s.remaining = s.capacity; s.save()
        messages.success(request, "Slot added."); return redirect("partner_dashboard")
    return render(request, "partner_dashboard.html", {
        "tours": u.tours.all(), "bookings": bookings[:20], "slot_form": slot_form,
        "earnings": bookings.aggregate(t=Sum("total"))["t"] or 0, "count": bookings.count()})
@partner_only
def new_tour(request):
    form = TourForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        t = form.save(commit=False); t.partner = request.user; t.save()
        messages.success(request, "Tour created."); return redirect("partner_dashboard")
    return render(request, "tour_form.html", {"form": form})
from django.shortcuts import get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from bookings.models import Hotel
from tours.models import Tour
@xframe_options_exempt
def widget(request, code):
    hotel = get_object_or_404(Hotel, code=code.upper())
    return render(request, "widget.html", {"hotel": hotel, "tours": Tour.objects.filter(is_active=True)[:8]})
