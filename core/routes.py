"""Official AMC-style heritage routes, redrawn as original stylised data (not to scale)."""
def _build(raw):
    out, n = [], 0
    for it in raw:
        if len(it) == 2:
            out.append({"x": it[0], "y": it[1], "s": False})
        else:
            n += 1
            out.append({"x": it[1], "y": it[2], "s": True, "name": it[0],
                        "note": it[3] if len(it) > 3 else "", "lab": it[4] if len(it) > 4 else str(n)})
    return out
R1 = [("Swaminarayan Mandir, Kalupur", 448, 91, "Built in 1822, the first temple of the Swaminarayan sect."), ("Kavi Dalpatram Chowk", 466, 148),
 ("Calico Dome", 483, 217), ("Kala Ramji Mandir", 524, 240), ("Shantinathji Mandir", 417, 277), ("Kuvavala Khancha", 397, 282),
 ("Jagvallabh Mandir", 361, 266), ("Zaveri Vad", 317, 282), ("Sambhavnath ni Khadki", 323, 330), ("Chaumukhji ni Pol", 356, 336),
 ("Doshivada ni Pol", 400, 405), ("Astapadji Mandir", 394, 455), ("Harkunvar Shethani ni Haveli", 406, 468),
 ("Fernandez Bridge & Gandhi Road", 370, 495), ("Chandla Ol", 347, 563), ("Muhurat Pol", 315, 622),
 ("Manek Baba's Mandir, Manek Chowk", 268, 602, "A jewellery market by day, a street-food square by night."),
 ("Rani ni Haziro", 308, 570, "Tombs of the queens of Ahmed Shah."), ("Badshah no Haziro", 225, 571, "Tomb of Ahmed Shah I, founder of the city."),
 ("Jumma Masjid", 167, 575, "Built in 1424 under Ahmed Shah I.")]
R2 = [("Manek Chowk (start)", 195, 826, "The walk begins at the old city's central square.", "S"), (270, 826), (255, 716), (366, 716), (370, 604),
 ("Astapadji Derasar", 410, 566, "", "A"), (400, 413), ("Sambhavnath Derasar", 340, 413, "", "B"), ("Ajitnath Derasar", 288, 461, "", "C"),
 ("Mahavir Swami Derasar", 259, 489, "", "D"), (288, 461), ("Shitalnath Derasar", 270, 356, "", "E"), (222, 350), (220, 285), (270, 266),
 ("Adishwar Bhagwan Derasar", 290, 258, "", "F"), ("Ajitnath Derasar", 358, 248, "", "G"), (405, 230), ("Jagvallabh Parshvanath Derasar", 458, 218, "", "H"),
 (515, 212), (500, 100), ("Chintamani Parshvanath Derasar", 435, 80, "", "I"), (410, 66), ("Shantinath Derasar", 338, 172, "", "J")]
R3 = [("Siddi Saiyad Mosque", 62, 903, "Famous for its stone jali lattice windows."), (122, 903), (122, 872), ("GTS Standard Bench Mark", 199, 869), (352, 845),
 ("Bhadrakali Mandir & Fort", 366, 845), (352, 800), ("Statue of Chinubhai Baronet", 352, 763), ("Bhadra Street Market", 366, 695),
 ("Teen Darwaza", 346, 615, "Ceremonial triple gateway of the old royal citadel."), ("Akhand Jyot", 363, 600), ("Oldest Market of the City", 349, 486),
 ("Jama Masjid", 350, 414, "Built in 1424 under Ahmed Shah I."), ("Badshah no Haziro", 353, 331), ("Rani no Haziro", 340, 309), (342, 266), (358, 120),
 ("Old Stock Exchange Building", 391, 118), ("Muhurat ni Pol", 437, 118), (468, 112), (461, 205), ("Manek Nath Mandir", 477, 208), ("Manek Chowk", 423, 210)]
ROUTES = [
 {"title": "Mandir to Masjid", "subtitle": "The classic morning walk from Kalupur's Swaminarayan temple to Jumma Masjid.", "meta": ["Morning walk", "Pols, havelis & mosques"], "secs": 26, "pts": _build(R1)},
 {"title": "Jain Derasar Walk", "subtitle": "Ten Jain derasars through the lanes behind Manek Chowk.", "meta": ["Starts 7:00 AM", "About 2 km"], "secs": 18, "pts": _build(R2)},
 {"title": "Night Heritage Walk", "subtitle": "From Siddi Saiyad Mosque through Bhadra to a lit-up Manek Chowk.", "meta": ["Starts 8:30 PM", "Evening walk"], "secs": 22, "pts": _build(R3)},
]
