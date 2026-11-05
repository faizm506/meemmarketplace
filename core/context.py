from django.conf import settings
def site(request):
    lang = request.session.get("lang", "en") if hasattr(request, "session") else "en"
    return {"SITE_NAME": settings.SITE_NAME, "LANG": lang, "LANGS": [("en", "EN"), ("hi", "हि"), ("gu", "ગુ")]}
