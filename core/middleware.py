<<<<<<< HEAD
from django.conf import settings

CSP = "; ".join([
    "default-src 'self'",
    "base-uri 'self'",
    "object-src 'none'",
    "frame-ancestors 'none'",
    "form-action 'self'",
    "img-src 'self' data: https://*.razorpay.com",
    "font-src 'self' data: https://fonts.gstatic.com",
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "script-src 'self' https://checkout.razorpay.com",
    "connect-src 'self' https://api.razorpay.com https://lumberjack.razorpay.com",
    "frame-src https://api.razorpay.com https://checkout.razorpay.com",
])


class SecurityHeadersMiddleware:
    """Adds the headers that close common browser-side attack paths (XSS, clickjacking, sniffing, data leaks)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.headers.setdefault("Content-Security-Policy", CSP + ("" if settings.DEBUG else "; upgrade-insecure-requests"))
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=(self), usb=(), interest-cohort=()")
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Cross-Origin-Resource-Policy", "same-origin")
        # Pages for signed-in people (orders, dashboards, cart) must never sit in a shared or back-button cache.
        if getattr(request, "user", None) is not None and request.user.is_authenticated and not request.path.startswith(("/static/", "/media/")):
            response.headers["Cache-Control"] = "private, no-store"
        return response
=======
class SecurityHeaders:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        r = self.get_response(request)
        embed = getattr(r, "xframe_options_exempt", False)
        r["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com https://unpkg.com https://checkout.razorpay.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://unpkg.com; "
            "font-src https://fonts.gstatic.com; img-src 'self' data: blob: https://unpkg.com https://*.basemaps.cartocdn.com https://tile.openstreetmap.org; "
            "frame-src https://api.razorpay.com https://checkout.razorpay.com; connect-src 'self' https://lumberjack.razorpay.com; "
            "form-action 'self' https://checkout.stripe.com; base-uri 'self'; object-src 'none'; "
            + ("frame-ancestors *" if embed else "frame-ancestors 'none'"))
        r["Referrer-Policy"] = "strict-origin-when-cross-origin"
        r["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        r["X-Content-Type-Options"] = "nosniff"
        return r
>>>>>>> 45224bb2107e9c064747289981fd5709c63dc9c9
