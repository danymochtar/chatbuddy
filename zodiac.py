from datetime import date, time
from typing import Optional

SIGN_TRAITS = {
    "Aries": "pelopor, impulsif, berani ambil risiko, energik",
    "Taurus": "stabil, sensual, keras kepala, cinta kenyamanan & keindahan",
    "Gemini": "komunikatif, ingin tahu, versatil, cepat bosan",
    "Cancer": "sensitif, protektif, moody, ikatan keluarga kuat",
    "Leo": "karismatik, bangga, generous, butuh pengakuan",
    "Virgo": "analitis, perfeksionis, helpful, detail-oriented",
    "Libra": "diplomat, estetik, mencari harmoni, kadang indesisif",
    "Scorpio": "intens, misterius, pasionat, transformatif",
    "Sagittarius": "petualang, filosofis, jujur, cinta kebebasan",
    "Capricorn": "disiplin, ambisius, praktis, reserved",
    "Aquarius": "independen, humanis, eksentrik, pemikir maju",
    "Pisces": "empatik, kreatif, melankolis, intuitif",
}


def sun_sign(dob: date) -> str:
    boundaries = [
        (1, 1, "Capricorn"),
        (1, 20, "Aquarius"),
        (2, 19, "Pisces"),
        (3, 21, "Aries"),
        (4, 20, "Taurus"),
        (5, 21, "Gemini"),
        (6, 21, "Cancer"),
        (7, 23, "Leo"),
        (8, 23, "Virgo"),
        (9, 23, "Libra"),
        (10, 23, "Scorpio"),
        (11, 22, "Sagittarius"),
        (12, 22, "Capricorn"),
    ]
    sign = "Capricorn"
    for m, d, s in boundaries:
        if (dob.month, dob.day) >= (m, d):
            sign = s
    return sign


def compute_chart(
    dob: date,
    birth_time: time,
    lat: float,
    lon: float,
) -> Optional[dict]:
    try:
        from immanuel import charts
        from immanuel.const import chart as chart_const
    except ImportError:
        return None
    try:
        dt_str = f"{dob.isoformat()} {birth_time.strftime('%H:%M')}"
        subject = charts.Subject(date_time=dt_str, latitude=lat, longitude=lon)
        natal = charts.Natal(subject)
        return {
            "sun": natal.objects[chart_const.SUN].sign.name,
            "moon": natal.objects[chart_const.MOON].sign.name,
            "rising": natal.objects[chart_const.ASC].sign.name,
        }
    except Exception:
        return None


INDONESIA_CITIES = {
    "jakarta": (-6.2088, 106.8456),
    "bandung": (-6.9175, 107.6191),
    "surabaya": (-7.2575, 112.7521),
    "medan": (3.5952, 98.6722),
    "semarang": (-6.9667, 110.4167),
    "makassar": (-5.1477, 119.4327),
    "palembang": (-2.9761, 104.7754),
    "denpasar": (-8.6705, 115.2126),
    "yogyakarta": (-7.7956, 110.3695),
    "jogja": (-7.7956, 110.3695),
    "malang": (-7.9797, 112.6304),
    "bogor": (-6.5950, 106.8166),
    "depok": (-6.4025, 106.7942),
    "tangerang": (-6.1783, 106.6319),
    "bekasi": (-6.2349, 106.9896),
    "batam": (1.0456, 104.0305),
    "pekanbaru": (0.5071, 101.4478),
    "padang": (-0.9471, 100.4172),
    "manado": (1.4748, 124.8421),
    "balikpapan": (-1.2379, 116.8529),
    "pontianak": (-0.0263, 109.3425),
    "banjarmasin": (-3.3194, 114.5906),
    "samarinda": (-0.5022, 117.1536),
    "jayapura": (-2.5337, 140.7181),
    "ambon": (-3.6955, 128.1814),
    "kupang": (-10.1772, 123.6070),
    "mataram": (-8.5833, 116.1167),
    "surakarta": (-7.5755, 110.8243),
    "solo": (-7.5755, 110.8243),
    "cirebon": (-6.7320, 108.5523),
    "tasikmalaya": (-7.3506, 108.2172),
    "bali": (-8.6705, 115.2126),
}

JAKARTA_COORDS = (-6.2088, 106.8456)


MBTI_TYPES = {
    "INTJ": "Si Arsitek — strategis, mandiri, visioner, perfeksionis dalam rencana jangka panjang",
    "INTP": "Si Logisi — analitis, pencari kebenaran, kreatif dalam ide, kadang lupa praktikalitas",
    "ENTJ": "Si Komandan — pemimpin alami, tegas, ambisius, efisien",
    "ENTP": "Si Debater — inovatif, suka tantangan intelektual, cepat berubah pikiran",
    "INFJ": "Si Advokat — idealis dalem, empatik, visioner, misi-driven",
    "INFP": "Si Mediator — penuh kasih, idealis, kreatif, butuh ruang sendiri",
    "ENFJ": "Si Protagonis — karismatik, inspiratif, peduli pertumbuhan orang lain",
    "ENFP": "Si Juara — antusias, penuh ide, sosial, butuh kebebasan",
    "ISTJ": "Si Logistik — disiplin, bisa diandalkan, setia pada tradisi",
    "ISFJ": "Si Pelindung — setia, teliti, nurturing, prioritas harmoni keluarga",
    "ESTJ": "Si Eksekutif — organisator, tegas, pekerja keras, to-the-point",
    "ESFJ": "Si Konsul — sosial, peduli, suka menolong, butuh validasi",
    "ISTP": "Si Virtuoso — praktis, observan, pintar teknis, tenang",
    "ISFP": "Si Petualang — artistik, fleksibel, sensitif, hidup di momen",
    "ESTP": "Si Pengusaha — energik, spontan, aksi-oriented, suka risiko",
    "ESFP": "Si Penghibur — ceria, ekspresif, spontan, pencari kesenangan",
}


SHIO_ANIMALS = [
    "Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular",
    "Kuda", "Kambing", "Monyet", "Ayam", "Anjing", "Babi",
]

SHIO_TRAITS = {
    "Tikus": "cerdas, cepat, oportunis, sosial",
    "Kerbau": "sabar, pekerja keras, bisa diandalkan, keras kepala",
    "Macan": "pemberani, pemimpin alami, kompetitif, rebellious",
    "Kelinci": "lembut, diplomatis, peka, butuh harmoni",
    "Naga": "karismatik, ambisius, penuh energi, dominan",
    "Ular": "bijak, intuitif, tenang, misterius",
    "Kuda": "bebas, energik, pencinta petualangan, impulsif",
    "Kambing": "artistik, empatik, sensitif, kadang ragu-ragu",
    "Monyet": "cerdik, inovatif, kreatif, gemar bersosialisasi",
    "Ayam": "teratur, jujur, detail, bangga akan penampilan",
    "Anjing": "loyal, protektif, jujur, kadang cemas",
    "Babi": "tulus, murah hati, cinta kenyamanan, naif",
}

ELEMENT_CYCLE = {
    0: "Logam", 1: "Logam",
    2: "Air", 3: "Air",
    4: "Kayu", 5: "Kayu",
    6: "Api", 7: "Api",
    8: "Tanah", 9: "Tanah",
}

ELEMENT_TRAITS = {
    "Logam": "disiplin, tegas, fokus pada pencapaian",
    "Air": "adaptif, intuitif, mengalir dengan situasi",
    "Kayu": "tumbuh, idealis, mencari ekspresi",
    "Api": "pasionat, kreatif, berani mengambil risiko",
    "Tanah": "stabil, praktis, bisa dipercaya",
}


def chinese_zodiac(dob: date) -> dict:
    year = dob.year
    if dob.month == 1 or (dob.month == 2 and dob.day < 5):
        year -= 1
    animal = SHIO_ANIMALS[(year - 1900) % 12]
    element = ELEMENT_CYCLE[year % 10]
    return {
        "animal": animal,
        "element": element,
        "animal_traits": SHIO_TRAITS[animal],
        "element_traits": ELEMENT_TRAITS[element],
        "label": f"{element} {animal}",
    }


DINA = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
DINA_NEPTU = {"Minggu": 5, "Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9}

PASARAN = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]
PASARAN_NEPTU = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}

DINA_TRAITS = {
    "Senin": "lembut, tenang, sabar, mudah bergaul",
    "Selasa": "penuh semangat, tegas, ambisius",
    "Rabu": "pandai komunikasi, analitis, cepat tanggap",
    "Kamis": "bijaksana, dewasa, berjiwa pemimpin",
    "Jumat": "sabar, penuh kasih, spiritual",
    "Sabtu": "mandiri, pekerja keras, disiplin",
    "Minggu": "kreatif, optimis, ceria",
}

PASARAN_TRAITS = {
    "Legi": "manis, lembut, disukai banyak orang",
    "Pahing": "tegas, keras kemauan, pantang menyerah",
    "Pon": "cerdas, banyak bicara, mudah bergaul",
    "Wage": "sederhana, jujur, kerja keras",
    "Kliwon": "misterius, kuat spiritual, penuh intuisi",
}

NEPTU_RANGE_MEANINGS = {
    "rendah": "karakter lembut & sabar (neptu 7-11)",
    "sedang": "karakter seimbang, fleksibel (neptu 12-14)",
    "tinggi": "karakter kuat, berkarisma (neptu 15-17)",
    "sangat_tinggi": "karakter dominan, ambisius (neptu 18+)",
}


def current_pasaran(today: date) -> dict:
    # Reference: 17 May 1995 = Rabu Legi (Legi = index 0)
    ref = date(1995, 5, 17)
    days = (today - ref).days
    idx = days % 5
    name = PASARAN[idx]
    return {
        "name": name,
        "traits": PASARAN_TRAITS[name],
    }


def current_moon_sign(today: date) -> Optional[str]:
    try:
        from immanuel import charts
        from immanuel.const import chart as chart_const

        # Use Jakarta noon as a neutral reference for collective moon tone
        dt_str = f"{today.isoformat()} 12:00"
        subject = charts.Subject(
            date_time=dt_str,
            latitude=JAKARTA_COORDS[0],
            longitude=JAKARTA_COORDS[1],
        )
        natal = charts.Natal(subject)
        return natal.objects[chart_const.MOON].sign.name
    except Exception:
        return None


def weton(dob: date) -> dict:
    # Reference: 17 May 1995 = Rabu Legi (verified against Javanese calendar)
    ref = date(1995, 5, 17)
    days = (dob - ref).days
    pasaran_idx = days % 5  # Legi = 0 on reference date
    pasaran_name = PASARAN[pasaran_idx]
    dina_name = DINA[dob.weekday()]
    neptu = DINA_NEPTU[dina_name] + PASARAN_NEPTU[pasaran_name]
    if neptu <= 11:
        neptu_range = "rendah"
    elif neptu <= 14:
        neptu_range = "sedang"
    elif neptu <= 17:
        neptu_range = "tinggi"
    else:
        neptu_range = "sangat_tinggi"
    return {
        "dina": dina_name,
        "pasaran": pasaran_name,
        "weton": f"{dina_name} {pasaran_name}",
        "neptu": neptu,
        "neptu_range": neptu_range,
        "dina_traits": DINA_TRAITS[dina_name],
        "pasaran_traits": PASARAN_TRAITS[pasaran_name],
        "neptu_meaning": NEPTU_RANGE_MEANINGS[neptu_range],
    }


def geocode_city(city_name: str) -> Optional[tuple[float, float]]:
    key = city_name.strip().lower().split(",")[0].strip()
    if key in INDONESIA_CITIES:
        return INDONESIA_CITIES[key]
    try:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="chatbuddy-numerology")
        loc = geolocator.geocode(city_name, timeout=5)
        if loc:
            return (loc.latitude, loc.longitude)
    except Exception:
        pass
    return None
