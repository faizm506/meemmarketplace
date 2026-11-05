import base64, hashlib, hmac, json, time, urllib.parse, urllib.request
from datetime import timedelta
from threading import Thread
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from .models import Booking, Payment
def providers():
    p = []
    if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET: p.append("razorpay")
    if settings.STRIPE_SECRET_KEY: p.append("stripe")
    if not p and settings.DEBUG: p.append("demo")
    return p
def _call(url, user, pwd, data=None, as_json=False):
    body = headers = None
    if data is not None:
        body = (json.dumps(data) if as_json else urllib.parse.urlencode(data)).encode()
        headers = {"Content-Type": "application/json" if as_json else "application/x-www-form-urlencoded"}
    req = urllib.request.Request(url, body, headers or {})
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{user}:{pwd}".encode()).decode())
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)
def razorpay_order(b):
    return _call("https://api.razorpay.com/v1/orders", settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET,
                 {"amount": b.total * 100, "currency": "INR", "receipt": b.code}, True)
def stripe_session(b, base):
    return _call("https://api.stripe.com/v1/checkout/sessions", settings.STRIPE_SECRET_KEY, "", {
        "mode": "payment", "client_reference_id": b.code, "success_url": f"{base}/pay/stripe/return/{b.code}/", "cancel_url": f"{base}/checkout/{b.code}/",
        "line_items[0][price_data][currency]": "inr", "line_items[0][price_data][unit_amount]": b.total * 100,
        "line_items[0][price_data][product_data][name]": b.slot.tour.title, "line_items[0][quantity]": 1})
def stripe_session_get(sid):
    return _call(f"https://api.stripe.com/v1/checkout/sessions/{sid}", settings.STRIPE_SECRET_KEY, "")
def _eq(a, b):
    return hmac.compare_digest(a.encode(), b.encode())
def verify_razorpay(order_id, payment_id, sig):
    mac = hmac.new(settings.RAZORPAY_KEY_SECRET.encode(), f"{order_id}|{payment_id}".encode(), hashlib.sha256).hexdigest()
    return bool(settings.RAZORPAY_KEY_SECRET) and _eq(mac, sig or "")
def verify_razorpay_webhook(body, sig):
    s = settings.RAZORPAY_WEBHOOK_SECRET
    return bool(s) and _eq(hmac.new(s.encode(), body, hashlib.sha256).hexdigest(), sig or "")
def verify_stripe_webhook(body, header):
    s = settings.STRIPE_WEBHOOK_SECRET
    try:
        parts = dict(x.split("=", 1) for x in header.split(","))
        if not s or abs(time.time() - int(parts["t"])) > 300: return False
        return _eq(hmac.new(s.encode(), parts["t"].encode() + b"." + body, hashlib.sha256).hexdigest(), parts["v1"])
    except Exception:
        return False
def mark_paid(payment):
    """Idempotent: safe to call from the return URL and the webhook."""
    with transaction.atomic():
        p = Payment.objects.select_for_update().select_related("booking__user", "booking__slot__tour").get(pk=payment.pk)
        if p.status in ("paid", "refund_due"): return p
        b = p.booking
        if b.status == Booking.CANCELLED:
            p.status = "refund_due"; p.save(); return p
        p.status = "paid"; p.save()
        b.status = Booking.CONFIRMED; b.save(update_fields=["status"])
    Thread(target=send_mail, args=(f"Booking confirmed: {b.slot.tour.title}",
        f"Your ticket code is {b.code}. See you on {b.slot.date}!", None, [b.user.email]), kwargs={"fail_silently": True}).start()
    return p
def release_stale(minutes=15):
    from tours.models import Slot
    with transaction.atomic():
        for b in Booking.objects.select_for_update().filter(status=Booking.PENDING, created__lt=timezone.now() - timedelta(minutes=minutes)):
            s = Slot.objects.select_for_update().get(pk=b.slot_id)
            s.remaining = min(s.capacity, s.remaining + b.guests); s.save(update_fields=["remaining"])
            b.status = Booking.CANCELLED; b.save(update_fields=["status"])
