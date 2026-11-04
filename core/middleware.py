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
