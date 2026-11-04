import hashlib, hmac, json, time
from datetime import date, time as dtime, timedelta
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.cache import cache
from accounts.models import User
from tours.models import Category, Tour, Slot
from .models import Booking, Payment
class Base(TestCase):
    def setUp(self):
        cache.clear()
        p = User.objects.create_user("p@x.com", "pw12345678", role="partner")
        c = Category.objects.create(name="Walk", slug="walk")
        t = Tour.objects.create(partner=p, category=c, title="T", description="d", price=500, meeting_point="m")
        self.slot = Slot.objects.create(tour=t, date=date.today() + timedelta(days=1), time=dtime(8), capacity=4, remaining=4)
        self.u = User.objects.create_user("u@x.com", "pw12345678"); self.client.force_login(self.u)
    def pending(self):
        self.client.post(reverse("book", args=[self.slot.pk]), {"guests": 2})
        return Booking.objects.get()
class BookingTests(Base):
    def test_hold_and_no_overbook(self):
        self.pending(); self.slot.refresh_from_db(); self.assertEqual(self.slot.remaining, 2)
        self.client.post(reverse("book", args=[self.slot.pk]), {"guests": 3})
        self.slot.refresh_from_db(); self.assertEqual(self.slot.remaining, 2)
    def test_cancel_restores(self):
        b = self.pending(); self.client.post(reverse("cancel", args=[b.code]))
        self.slot.refresh_from_db(); self.assertEqual(self.slot.remaining, 4)
    def test_other_user_cannot_see_ticket(self):
        b = self.pending(); self.client.force_login(User.objects.create_user("o@x.com", "pw12345678"))
        self.assertEqual(self.client.get(reverse("ticket", args=[b.code])).status_code, 404)
    def test_partner_only_dashboard(self):
        self.assertEqual(self.client.get(reverse("partner_dashboard")).status_code, 403)
class PaymentTests(Base):
    @override_settings(RAZORPAY_KEY_SECRET="k", RAZORPAY_WEBHOOK_SECRET="w")
    def test_razorpay_webhook_idempotent(self):
        b = self.pending(); Payment.objects.create(booking=b, provider="razorpay", provider_ref="order_1", amount=b.total)
        body = json.dumps({"event": "payment.captured", "payload": {"payment": {"entity": {"order_id": "order_1"}}}}).encode()
        bad = self.client.post("/webhooks/razorpay/", body, content_type="application/json", HTTP_X_RAZORPAY_SIGNATURE="nope")
        self.assertEqual(bad.status_code, 400)
        sig = hmac.new(b"w", body, hashlib.sha256).hexdigest()
        for _ in range(2):
            self.assertEqual(self.client.post("/webhooks/razorpay/", body, content_type="application/json", HTTP_X_RAZORPAY_SIGNATURE=sig).status_code, 200)
        b.refresh_from_db(); self.assertEqual(b.status, "confirmed")
    @override_settings(STRIPE_WEBHOOK_SECRET="whsec")
    def test_stripe_webhook(self):
        b = self.pending(); Payment.objects.create(booking=b, provider="stripe", provider_ref="cs_1", amount=b.total)
        body = json.dumps({"type": "checkout.session.completed", "data": {"object": {"id": "cs_1", "payment_status": "paid"}}}).encode()
        t = str(int(time.time())); sig = hmac.new(b"whsec", t.encode() + b"." + body, hashlib.sha256).hexdigest()
        r = self.client.post("/webhooks/stripe/", body, content_type="application/json", HTTP_STRIPE_SIGNATURE=f"t={t},v1={sig}")
        self.assertEqual(r.status_code, 200); b.refresh_from_db(); self.assertEqual(b.status, "confirmed")
    @override_settings(RAZORPAY_KEY_SECRET="k")
    def test_razorpay_verify_rejects_bad_signature(self):
        b = self.pending(); Payment.objects.create(booking=b, provider="razorpay", provider_ref="o2", amount=b.total)
        self.client.post(reverse("razorpay_verify"), {"razorpay_order_id": "o2", "razorpay_payment_id": "p", "razorpay_signature": "x"})
        b.refresh_from_db(); self.assertEqual(b.status, "pending")
class RateLimitTest(Base):
    def test_login_rate_limited(self):
        self.client.logout()
        codes = [self.client.post("/login/", {"username": "a@b.c", "password": "x"}).status_code for _ in range(10)]
        self.assertIn(429, codes)
