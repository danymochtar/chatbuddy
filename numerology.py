from datetime import date, datetime
from zoneinfo import ZoneInfo

PYTHAGOREAN = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "O": 6, "P": 7, "Q": 8, "R": 9,
    "S": 1, "T": 2, "U": 3, "V": 4, "W": 5, "X": 6, "Y": 7, "Z": 8,
}
VOWELS = set("AEIOUY")  # Hans Decoz / World Numerology treats Y as vowel
MASTER_NUMBERS = {11, 22, 33}
TZ = ZoneInfo("Asia/Jakarta")


def today_local() -> date:
    return datetime.now(TZ).date()


def reduce_number(n: int) -> int:
    while n > 9 and n not in MASTER_NUMBERS:
        n = sum(int(d) for d in str(n))
    return n


def digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))


def life_path(dob: date) -> int:
    digits = [int(d) for d in dob.strftime("%d%m%Y")]
    return reduce_number(sum(digits))


def letters_sum(name: str, only_vowels: bool = False, only_consonants: bool = False) -> int:
    total = 0
    for ch in name.upper():
        if ch not in PYTHAGOREAN:
            continue
        if only_vowels and ch not in VOWELS:
            continue
        if only_consonants and ch in VOWELS:
            continue
        total += PYTHAGOREAN[ch]
    return reduce_number(total)


def expression_number(name: str) -> int:
    return letters_sum(name)


def soul_urge_number(name: str) -> int:
    return letters_sum(name, only_vowels=True)


def personality_number(name: str) -> int:
    return letters_sum(name, only_consonants=True)


def birthday_number(dob: date) -> int:
    return reduce_number(dob.day)


def personal_year(dob: date, today: date) -> int:
    bm = reduce_number(dob.month)
    bd = reduce_number(dob.day)
    cy = reduce_number(digit_sum(today.year))
    return reduce_number(bm + bd + cy)


def personal_month(dob: date, today: date) -> int:
    py = personal_year(dob, today)
    cm = reduce_number(today.month)
    return reduce_number(py + cm)


def personal_day(dob: date, today: date) -> int:
    pm = personal_month(dob, today)
    cd = reduce_number(today.day)
    return reduce_number(pm + cd)


MEANINGS = {
    1: "Pemimpin, independen, ambisius, pionir",
    2: "Diplomat, harmonis, sensitif, kooperatif",
    3: "Kreatif, ekspresif, sosial, optimistis",
    4: "Pekerja keras, stabil, praktis, disiplin",
    5: "Petualang, bebas, dinamis, penuh rasa ingin tahu",
    6: "Penuh kasih, bertanggung jawab, pengasuh, harmonis",
    7: "Analitis, spiritual, introspektif, pencari kebenaran",
    8: "Ambisius, kuat, berorientasi materi dan kekuasaan",
    9: "Humanis, bijaksana, penuh kasih universal, idealis",
    11: "Master number — intuitif tinggi, visioner, inspirator spiritual",
    22: "Master number — master builder, mampu mewujudkan mimpi besar",
    33: "Master number — master teacher, pengabdi kemanusiaan tertinggi",
}

DAILY_VIBES = {
    1: "Hari mulai-mulai baru — inisiatif, langkah pertama, keberanian ambil keputusan",
    2: "Hari kolaborasi & kesabaran — tarik napas, dengerin orang lain, jangan buru-buru",
    3: "Hari ekspresif & kreatif — cocok sosial, berkarya, have fun",
    4: "Hari pekerja keras — fokus bangun fondasi, beresin urusan detail & administratif",
    5: "Hari dinamis — perubahan, adventure, fleksibel, coba hal baru",
    6: "Hari keluarga & tanggung jawab — urus orang terdekat, bikin harmoni",
    7: "Hari introspektif — refleksi, belajar, pelan-pelan dulu, jangan dipaksa",
    8: "Hari kekuatan & pencapaian — momentum buat keputusan besar, urusan uang/bisnis",
    9: "Hari penutupan & pelepasan — selesaiin yang belum beres, let go dari yang udah ga relevan",
    11: "Master day — intuisi tajam banget, inspirasi datang, percaya gut feeling",
    22: "Master day — mewujudkan mimpi besar, action yang berdampak jangka panjang",
    33: "Master day — pengabdian, kasih sayang meluap, momen peduli sesama",
}

YEAR_THEMES = {
    1: "Tahun awal baru — fondasi, visi jangka panjang, inisiatif besar",
    2: "Tahun sabar & kolaborasi — hubungan, partnership, perlahan tapi pasti",
    3: "Tahun kreatif — ekspresi diri, jaringan sosial meluas, karya",
    4: "Tahun kerja keras — bangun sistem, fondasi karir/finansial",
    5: "Tahun perubahan — freedom, adventure, banyak shift",
    6: "Tahun tanggung jawab — keluarga, rumah, komitmen",
    7: "Tahun refleksi — spiritual growth, belajar, inner work",
    8: "Tahun power — karir naik level, finansial, achievement",
    9: "Tahun penutupan — akhiri siklus, let go, persiapan siklus baru",
    11: "Master year — awakening spiritual, intuisi jadi kompas",
    22: "Master year — building mimpi raksasa jadi realita",
    33: "Master year — service ke komunitas / misi lebih besar",
}


def build_profile(full_name: str, dob: date, today: date | None = None) -> dict:
    today = today or today_local()
    lp = life_path(dob)
    ex = expression_number(full_name)
    su = soul_urge_number(full_name)
    pe = personality_number(full_name)
    bd = birthday_number(dob)
    py = personal_year(dob, today)
    pm = personal_month(dob, today)
    pd = personal_day(dob, today)
    return {
        "full_name": full_name,
        "dob": dob.isoformat(),
        "today": today.isoformat(),
        "life_path": lp,
        "expression": ex,
        "soul_urge": su,
        "personality": pe,
        "birthday": bd,
        "personal_year": py,
        "personal_month": pm,
        "personal_day": pd,
        "meanings": {
            "life_path": MEANINGS[lp],
            "expression": MEANINGS[ex],
            "soul_urge": MEANINGS[su],
            "personality": MEANINGS[pe],
            "birthday": MEANINGS[bd],
            "personal_year": YEAR_THEMES[py],
            "personal_day": DAILY_VIBES[pd],
        },
    }
