from django import template
from django.utils.html import format_html
register = template.Library()
P = {
 "arch": "M4 21V10a8 8 0 0 1 16 0v11M8 21v-8a4 4 0 0 1 8 0v8M2 21h20",
 "sun": "M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10zM12 1v3M12 20v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M1 12h3M20 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1",
 "moon": "M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z",
 "food": "M6 2v8a3 3 0 0 0 6 0V2M9 2v20M18 2c-2 2-3 5-3 8h3v12",
 "thread": "M4 4h16v16H4zM4 12h16M12 4v16M8 4v16M16 4v16",
 "camera": "M3 8h4l2-3h6l2 3h4v12H3zM12 17a4 4 0 1 0 0-8 4 4 0 0 0 0 8z",
 "building": "M3 21h18M5 21V8l7-5 7 5v13M9 21v-6h6v6",
 "clock": "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 6v6l4 2",
 "pin": "M12 22s7-6.5 7-12a7 7 0 1 0-14 0c0 5.5 7 12 7 12zM12 12a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z",
 "users": "M17 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2M10 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM21 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8",
 "calendar": "M3 5h18v16H3zM3 10h18M8 2v6M16 2v6",
 "home": "M3 11l9-8 9 8M5 10v11h14V10",
 "compass": "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM16 8l-2 6-6 2 2-6z",
 "ticket": "M3 8a2 2 0 0 0 0 8v3h18v-3a2 2 0 0 1 0-8V5H3zM13 5v14",
 "user": "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z",
 "star": "M12 2l3 6.9 7.5.6-5.7 4.9 1.8 7.3L12 17.8 5.4 21.7l1.8-7.3L1.5 9.5 9 8.9z",
 "shield": "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z",
}
@register.simple_tag
def icon(name, cls="w-5 h-5"):
    fill = "currentColor" if name == "star_f" else "none"
    d = P.get("star" if name == "star_f" else name, P["arch"])
    return format_html('<svg class="{}" viewBox="0 0 24 24" fill="{}" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{}"/></svg>', cls, fill, d)
TR = {"hi": {"Walks": "वॉक", "Routes": "रूट", "Log in": "लॉग इन", "Join": "जुड़ें", "My Bookings": "मेरी बुकिंग", "Log out": "लॉग आउट",
 "Explore walks": "वॉक देखें", "Become a partner": "पार्टनर बनें", "Walk through 600 years of stories.": "600 साल की कहानियों में चलिए।",
 "Featured walks": "चुनिंदा वॉक", "Book": "बुक करें", "Choose a slot": "स्लॉट चुनें", "Itinerary": "यात्रा कार्यक्रम", "Reviews": "समीक्षाएं",
 "Home": "होम", "Tickets": "टिकट", "Pay now": "अभी भुगतान करें", "Search": "खोजें", "Heritage walks in Ahmedabad": "अहमदाबाद में हेरिटेज वॉक"},
 "gu": {"Walks": "વોક", "Routes": "રૂટ", "Log in": "લૉગ ઇન", "Join": "જોડાઓ", "My Bookings": "મારી બુકિંગ", "Log out": "લૉગ આઉટ",
 "Explore walks": "વોક જુઓ", "Become a partner": "પાર્ટનર બનો", "Walk through 600 years of stories.": "600 વર્ષની વાર્તાઓમાં ચાલો.",
 "Featured walks": "પસંદગીના વોક", "Book": "બુક કરો", "Choose a slot": "સ્લોટ પસંદ કરો", "Itinerary": "કાર્યક્રમ", "Reviews": "સમીક્ષાઓ",
 "Home": "હોમ", "Tickets": "ટિકિટ", "Pay now": "હમણાં ચૂકવો", "Search": "શોધો", "Heritage walks in Ahmedabad": "અમદાવાદમાં હેરિટેજ વોક"}}
@register.simple_tag(takes_context=True)
def t(context, s):
    return TR.get(context.get("LANG", "en"), {}).get(s, s)
