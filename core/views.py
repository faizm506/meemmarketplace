import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from tours.models import Tour, Category
def home(request):
    return render(request, "home.html", {
        "featured": Tour.objects.filter(is_active=True).select_related("category")[:6],
        "categories": Category.objects.all(), "tour_count": Tour.objects.filter(is_active=True).count()})
def routes(request):
    from .routes import ROUTES
    return render(request, "routes.html", {"routes": ROUTES})
def health(request):
    return JsonResponse({"status": "ok"})
def set_lang(request, code):
    if code in ("en", "hi", "gu"):
        request.session["lang"] = code
    nxt = request.META.get("HTTP_REFERER", "/")
    return redirect(nxt if url_has_allowed_host_and_scheme(nxt, {request.get_host()}) else "/")
def manifest(request):
    return HttpResponse(json.dumps({"name": "Virasat Walks", "short_name": "Virasat", "start_url": "/", "display": "standalone",
        "background_color": "#FBF8F3", "theme_color": "#1B2A49",
        "icons": [{"src": "/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"}]}), content_type="application/manifest+json")
def icon(request):
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" fill="#1B2A49"/><path d="M136 392V232a120 120 0 0 1 240 0v160M196 392V272a60 60 0 0 1 120 0v120M100 392h312" fill="none" stroke="#E3A72F" stroke-width="22" stroke-linecap="round"/></svg>'
    return HttpResponse(svg, content_type="image/svg+xml")
SW = """const C='virasat-v1';
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(clients.claim()));
self.addEventListener('fetch',e=>{const r=e.request,u=new URL(r.url);if(r.method!=='GET'||u.origin!==location.origin||r.mode!=='navigate')return;
e.respondWith(fetch(r).then(res=>{if(/^\\/(ticket|my-bookings)\\//.test(u.pathname)||u.pathname==='/'){const c=res.clone();caches.open(C).then(x=>x.put(r,c))}return res})
.catch(()=>caches.match(r).then(m=>m||new Response('<h1>Offline</h1><p>Saved tickets open from My bookings once visited.</p>',{headers:{'Content-Type':'text/html'}}))))});"""
def sw(request):
    r = HttpResponse(SW, content_type="application/javascript"); r["Service-Worker-Allowed"] = "/"; return r
