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
