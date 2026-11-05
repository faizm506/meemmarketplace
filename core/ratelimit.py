from functools import wraps
from django.core.cache import cache
from django.http import HttpResponse
def rate_limit(name, limit=10, window=60):
    def deco(view):
        @wraps(view)
        def w(request, *a, **kw):
            if request.method == "POST":
                key = f"rl:{name}:{request.META.get('REMOTE_ADDR', '?')}"
                cache.add(key, 0, window)
                if cache.incr(key) > limit:
                    return HttpResponse("Too many requests. Please wait a moment.", status=429)
            return view(request, *a, **kw)
        return w
    return deco
