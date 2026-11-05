from django.urls import path
from . import views as v
urlpatterns = [
    path("book/<int:slot_id>/", v.book, name="book"),
    path("checkout/<str:code>/", v.checkout, name="checkout"),
    path("pay/razorpay/verify/", v.razorpay_verify, name="razorpay_verify"),
    path("pay/stripe/return/<str:code>/", v.stripe_return, name="stripe_return"),
    path("webhooks/razorpay/", v.razorpay_webhook), path("webhooks/stripe/", v.stripe_webhook),
    path("my-bookings/", v.my_bookings, name="my_bookings"),
    path("ticket/<str:code>/", v.ticket, name="ticket"),
    path("cancel/<str:code>/", v.cancel, name="cancel"),
    path("review/<str:code>/", v.review, name="review"),
]
