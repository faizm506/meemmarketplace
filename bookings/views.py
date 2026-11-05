import json
from datetime import date
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from core.ratelimit import rate_limit
from tours.models import Slot
from . import payments as pay
from .forms import ReviewForm
from .models import Booking, Hotel, Payment
@login_required
@require_POST
@rate_limit("book", 12, 60)
def book(request, slot_id):
    pay.release_stale()
    try:
        guests = int(request.POST.get("guests", "1"))
    except ValueError:
        guests = 0
    with transaction.atomic():
        slot = get_object_or_404(Slot.objects.select_for_update().select_related("tour"), pk=slot_id)
        if guests < 1 or guests > slot.remaining:
            messages.error(request, f"Only {slot.remaining} spot(s) left for that slot.")
            return redirect(slot.tour.get_absolute_url())
        slot.remaining -= guests
        slot.save(update_fields=["remaining"])
        hotel = Hotel.objects.filter(code=request.session.get("ref", "").upper()).first()
        b = Booking.objects.create(user=request.user, slot=slot, guests=guests, total=guests * slot.tour.price, ref=hotel)
    return redirect("checkout", code=b.code)
@login_required
@rate_limit("checkout", 20, 60)
def checkout(request, code):
    b = get_object_or_404(Booking.objects.select_related("slot__tour"), code=code, user=request.user)
    if b.status != Booking.PENDING:
        return redirect("ticket", code=code)
    avail = pay.providers()
    if request.method == "POST":
        prov = request.POST.get("provider")
        if prov not in avail:
            return HttpResponseBadRequest("Unknown payment method")
        try:
            if prov == "demo":
                pay.mark_paid(Payment.objects.create(booking=b, provider="demo", amount=b.total))
                messages.success(request, "Demo payment successful. Booking confirmed!")
                return redirect("ticket", code=code)
            if prov == "razorpay":
                o = pay.razorpay_order(b)
                Payment.objects.create(booking=b, provider="razorpay", provider_ref=o["id"], amount=b.total)
                return render(request, "razorpay.html", {"b": b, "order_id": o["id"], "key": settings.RAZORPAY_KEY_ID, "amount": b.total * 100})
            s = pay.stripe_session(b, request.build_absolute_uri("/").rstrip("/"))
            Payment.objects.create(booking=b, provider="stripe", provider_ref=s["id"], amount=b.total)
            return redirect(s["url"])
        except Exception:
            messages.error(request, "Could not reach the payment gateway. Please try again.")
    return render(request, "checkout.html", {"b": b, "providers": avail})
@login_required
@require_POST
def razorpay_verify(request):
    p = Payment.objects.filter(provider="razorpay", provider_ref=request.POST.get("razorpay_order_id", ""), booking__user=request.user).first()
    if p and pay.verify_razorpay(p.provider_ref, request.POST.get("razorpay_payment_id", ""), request.POST.get("razorpay_signature")):
        pay.mark_paid(p); messages.success(request, "Payment received. Booking confirmed!")
        return redirect("ticket", code=p.booking.code)
    messages.error(request, "Payment could not be verified.")
    return redirect("my_bookings")
@login_required
def stripe_return(request, code):
    p = Payment.objects.filter(provider="stripe", booking__code=code, booking__user=request.user).order_by("-id").first()
    try:
        if p and pay.stripe_session_get(p.provider_ref).get("payment_status") == "paid":
            pay.mark_paid(p); messages.success(request, "Payment received. Booking confirmed!")
        else:
            messages.info(request, "Payment is processing. We'll confirm shortly.")
    except Exception:
        messages.info(request, "Payment is processing. We'll confirm shortly.")
    return redirect("ticket", code=code)
@csrf_exempt
@require_POST
def razorpay_webhook(request):
    if not pay.verify_razorpay_webhook(request.body, request.headers.get("X-Razorpay-Signature")):
        return HttpResponse(status=400)
    try:
        ev = json.loads(request.body)
        oid = ev["payload"]["payment"]["entity"]["order_id"]
        p = Payment.objects.filter(provider="razorpay", provider_ref=oid).first()
        if p and ev.get("event") in ("payment.captured", "order.paid"):
            pay.mark_paid(p)
    except (KeyError, ValueError):
        return HttpResponse(status=400)
    return HttpResponse("ok")
@csrf_exempt
@require_POST
def stripe_webhook(request):
    if not pay.verify_stripe_webhook(request.body, request.headers.get("Stripe-Signature", "")):
        return HttpResponse(status=400)
    try:
        ev = json.loads(request.body); obj = ev["data"]["object"]
        if ev["type"] == "checkout.session.completed" and obj.get("payment_status") == "paid":
            p = Payment.objects.filter(provider="stripe", provider_ref=obj["id"]).first()
            if p: pay.mark_paid(p)
    except (KeyError, ValueError):
        return HttpResponse(status=400)
    return HttpResponse("ok")
@login_required
def my_bookings(request):
    pay.release_stale()
    return render(request, "my_bookings.html", {"bookings": request.user.bookings.select_related("slot__tour"), "today": date.today()})
@login_required
def ticket(request, code):
    return render(request, "ticket.html", {"b": get_object_or_404(Booking.objects.select_related("slot__tour"), code=code, user=request.user)})
@login_required
@require_POST
def cancel(request, code):
    with transaction.atomic():
        b = get_object_or_404(Booking.objects.select_for_update(), code=code, user=request.user)
        if b.status in (Booking.PENDING, Booking.CONFIRMED):
            s = Slot.objects.select_for_update().get(pk=b.slot_id)
            s.remaining = min(s.capacity, s.remaining + b.guests); s.save(update_fields=["remaining"])
            b.payments.filter(status="paid").update(status="refund_due")
            b.status = Booking.CANCELLED; b.save(update_fields=["status"])
    messages.info(request, "Booking cancelled. Any payment will be refunded per policy.")
    return redirect("my_bookings")
@login_required
@rate_limit("review", 6, 300)
def review(request, code):
    b = get_object_or_404(Booking.objects.select_related("slot__tour"), code=code, user=request.user, status=Booking.CONFIRMED)
    if b.slot.date > date.today() or hasattr(b, "review"):
        messages.info(request, "You can review a walk once, after it has taken place.")
        return redirect("my_bookings")
    form = ReviewForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        r = form.save(commit=False); r.booking, r.tour, r.user = b, b.slot.tour, request.user; r.save()
        messages.success(request, "Thanks for your review!")
        return redirect(b.slot.tour.get_absolute_url())
    return render(request, "review_form.html", {"form": form, "b": b})
