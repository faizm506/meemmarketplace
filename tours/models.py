from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=12, default="arch")
    class Meta:
        verbose_name_plural = "categories"
    def __str__(self):
        return self.name
class Tour(models.Model):
    partner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tours")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="tours")
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    duration_hours = models.DecimalField(max_digits=3, decimal_places=1, default=2)
    price = models.PositiveIntegerField(help_text="INR per person")
    max_group = models.PositiveSmallIntegerField(default=12)
    languages = models.CharField(max_length=80, default="English, Hindi, Gujarati")
    meeting_point = models.CharField(max_length=140)
    lat = models.FloatField(default=23.0258)
    lng = models.FloatField(default=72.5873)
    icon = models.CharField(max_length=12, default="arch")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created"]
    def save(self, *a, **kw):
        if not self.slug:
            base, n = slugify(self.title)[:120] or "tour", 1
            self.slug = base
            while Tour.objects.filter(slug=self.slug).exists():
                n += 1; self.slug = f"{base}-{n}"
        super().save(*a, **kw)
    def get_absolute_url(self):
        return reverse("tour_detail", args=[self.slug])
    def __str__(self):
        return self.title
class Stop(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="stops")
    order = models.PositiveSmallIntegerField(default=1)
    name = models.CharField(max_length=120)
    story = models.TextField(blank=True)
    lat = models.FloatField()
    lng = models.FloatField()
    class Meta:
        ordering = ["order"]
    def __str__(self):
        return f"{self.tour} · {self.name}"
class Slot(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="slots")
    date = models.DateField()
    time = models.TimeField()
    capacity = models.PositiveSmallIntegerField()
    remaining = models.PositiveSmallIntegerField()
    class Meta:
        ordering = ["date", "time"]
    def save(self, *a, **kw):
        if self.pk is None and self.remaining is None:
            self.remaining = self.capacity
        super().save(*a, **kw)
    def __str__(self):
        return f"{self.tour} {self.date} {self.time}"
