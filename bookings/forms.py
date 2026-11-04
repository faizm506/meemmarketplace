import uuid
from io import BytesIO
from django import forms
from django.core.files.base import ContentFile
from PIL import Image
from .models import Review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text", "photo"]
        widgets = {"rating": forms.Select(choices=[(i, f"{i} / 5") for i in range(5, 0, -1)])}
    def clean_photo(self):
        f = self.cleaned_data.get("photo")
        if not f or not hasattr(f, "read"):
            return f
        if f.size > 3 * 1024 * 1024:
            raise forms.ValidationError("Image must be under 3 MB.")
        try:
            Image.open(f).verify(); f.seek(0)
            im = Image.open(f).convert("RGB"); im.thumbnail((1600, 1600))
        except Exception:
            raise forms.ValidationError("Please upload a valid image.")
        buf = BytesIO(); im.save(buf, "JPEG", quality=85)   # re-encode strips metadata/payloads
        return ContentFile(buf.getvalue(), name=f"{uuid.uuid4().hex}.jpg")
