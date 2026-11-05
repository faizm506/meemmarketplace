from django import forms
from tours.models import Tour, Slot
class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ["title", "category", "description", "duration_hours", "price", "max_group", "languages", "meeting_point", "lat", "lng", "icon"]
class SlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ["tour", "date", "time", "capacity"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"}), "time": forms.TimeInput(attrs={"type": "time"})}
    def __init__(self, *a, partner=None, **kw):
        super().__init__(*a, **kw)
        self.fields["tour"].queryset = Tour.objects.filter(partner=partner)
