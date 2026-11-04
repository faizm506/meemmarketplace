# Virasat Walks – Ahmedabad heritage walk marketplace (Django 5 + SQLite)

    python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py seed            # demo tours + partner guide@virasat.test / guide12345
    python manage.py createsuperuser
    python manage.py runserver       # http://127.0.0.1:8000

Test: `python manage.py test`. Rename the site with env `SITE_NAME`.
Production: set `DJANGO_DEBUG=0`, `DJANGO_SECRET_KEY`, `ALLOWED_HOSTS` (enables HTTPS/HSTS/secure cookies).
Next steps: Razorpay/Stripe payments, reviews, i18n strings, PWA, dark mode, 2FA, Celery emails.

## v2 additions
- Payments: set `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_WEBHOOK_SECRET` and/or `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`.
  Webhook URLs: `/webhooks/razorpay/` (event payment.captured) and `/webhooks/stripe/` (checkout.session.completed).
  With no keys and DEBUG=1, a demo "Pay" button appears. Refunds are flagged `refund_due`; issue them in the gateway dashboard.
- Reviews with photo upload (re-encoded, 3 MB cap), hotel referral `?ref=CODE` + embed `/widget/HAVELI/` (iframe), commission shown in admin.
- Dark mode toggle, installable PWA (`/manifest.webmanifest`, `/sw.js`), EN/HI/GU switcher, rate limits, CSP and security headers.
