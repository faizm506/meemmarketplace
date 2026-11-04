from datetime import date, time, timedelta
from django.core.management.base import BaseCommand
from accounts.models import User
from tours.models import Category, Tour, Stop, Slot
CATS = [("Morning Heritage Walk", "morning", "sun"), ("Night Walk", "night", "moon"), ("Pol Food Walk", "food", "food"),
        ("Textile Tour", "textile", "thread"), ("Photography Walk", "photo", "camera"), ("Architecture", "architecture", "building")]
TOURS = [
 ("Pols of Old Ahmedabad", "morning", "Wander timber-carved havelis and bird-feeding chabutras inside the walled city's pols.", 2.5, 600, "Kalupur Swaminarayan Temple", 23.0262, 72.5992,
  [("Swaminarayan Temple, Kalupur", "Intricate Burma-teak carving from 1822.", 23.0262, 72.5992), ("Haveli Pol", "Merchant houses with painted ceilings.", 23.0245, 72.5870), ("Jama Masjid", "Built in 1424 by Ahmed Shah I.", 23.0240, 72.5837)]),
 ("Manek Chowk Night Food Walk", "night", "From a jewellers' market by day to a street-food carnival after dark.", 2, 750, "Manek Chowk Main Gate", 23.0236, 72.5865,
  [("Manek Burj", "Sufi saint Manek Nath legend.", 23.0237, 72.5863), ("Chocolate Sandwich Lane", "Local late-night favourites.", 23.0233, 72.5868)]),
 ("Textile Heritage & Block Printing", "textile", "Meet artisans keeping Ahmedabad's calico and block-print legacy alive.", 3, 1200, "Calico Museum Gate", 23.0498, 72.5827,
  [("Calico Museum area", "Centuries of Indian textiles.", 23.0498, 72.5827), ("Block-print Studio", "Hands-on stamping.", 23.0480, 72.5800)]),
 ("Sabarmati Sunrise Photo Walk", "photo", "Golden hour along the river, ghats and Gandhi Ashram.", 2.5, 900, "Gandhi Ashram Entrance", 23.0607, 72.5800,
  [("Gandhi Ashram", "Hriday Kunj and the spinning wheel.", 23.0607, 72.5800), ("Riverfront Promenade", "Sunrise vantage.", 23.0390, 72.5710)]),
 ("Sidi Saiyyed Jali & Mosques", "architecture", "Study stone lattice, stepwells and Indo-Saracenic architecture.", 3, 800, "Sidi Saiyyed Mosque", 23.0276, 72.5806,
  [("Sidi Saiyyed Mosque", "Famous Tree of Life jali.", 23.0276, 72.5806), ("Rani no Hajiro", "Tombs of Ahmed Shah's queens.", 23.0236, 72.5875)]),
 ("Pol Breakfast Trail", "food", "Fafda-jalebi, khichdo and chai in Old City nooks.", 2, 550, "Lal Darwaja", 23.0258, 72.5805,
  [("Lal Darwaja", "Historic bazaar gate.", 23.0258, 72.5805), ("Teen Darwaja", "Ceremonial triple arch.", 23.0245, 72.5818)]),
]
class Command(BaseCommand):
    help = "Load demo Ahmedabad heritage tours"
    def handle(self, *a, **kw):
        partner, _ = User.objects.get_or_create(email="guide@virasat.test", defaults={"role": "partner", "first_name": "Demo Guide"})
        partner.set_password("guide12345"); partner.save()
        cats = {s: Category.objects.get_or_create(slug=s, defaults={"name": n, "icon": e})[0] for n, s, e in CATS}
        for title, cat, desc, dur, price, meet, lat, lng, stops in TOURS:
            t, new = Tour.objects.get_or_create(title=title, defaults=dict(partner=partner, category=cats[cat], description=desc,
                duration_hours=dur, price=price, meeting_point=meet, lat=lat, lng=lng, icon=cats[cat].icon))
            if new:
                for i, (n, s, la, lo) in enumerate(stops, 1):
                    Stop.objects.create(tour=t, order=i, name=n, story=s, lat=la, lng=lo)
                for d in range(1, 15):
                    Slot.objects.create(tour=t, date=date.today() + timedelta(days=d), time=time(19) if cat == "night" else time(7, 30), capacity=12, remaining=12)
        self.stdout.write(self.style.SUCCESS("Seeded. Partner login: guide@virasat.test / guide12345"))
        from bookings.models import Hotel
        Hotel.objects.get_or_create(code="HAVELI", defaults={"name": "Demo Heritage Haveli", "commission_pct": 10})
