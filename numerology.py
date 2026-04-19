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


def universal_day(today: date) -> int:
    digits = [int(d) for d in today.strftime("%d%m%Y")]
    return reduce_number(sum(digits))


ARCHETYPES = {
    1: "Si Leader",
    2: "Si Pendamai",
    3: "Si Kreatif",
    4: "Si Pekerja",
    5: "Si Bebas",
    6: "Si Penyayang",
    7: "Si Pemikir",
    8: "Si Ambisius",
    9: "Si Idealis",
    11: "Si Visioner",
    22: "Si Pembangun",
    33: "Si Guru",
}


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

MONTH_THEMES = {
    1: "Bulan inisiatif & awal baru — cocok buat mulai proyek / kebiasaan",
    2: "Bulan sabar & hubungan — perlahan, pertimbangkan feedback orang",
    3: "Bulan ekspresi & sosial — lagi cerah buat berkarya dan networking",
    4: "Bulan disiplin & bangun fondasi — fokus ke sistem & rutinitas",
    5: "Bulan perubahan & fleksibel — siap-siap shift, jangan kaku",
    6: "Bulan rumah & tanggung jawab — fokus ke orang terdekat & komitmen",
    7: "Bulan refleksi & belajar — tarik diri, deep thinking, studi",
    8: "Bulan power & pencapaian — momen ambil keputusan besar, uang/karir",
    9: "Bulan penutupan — selesaiin yang pending, release yang ga relevan",
    11: "Master month — intuisi kuat, bisa jadi inspirasi buat orang",
    22: "Master month — action skala besar, building jangka panjang",
    33: "Master month — service, pengabdian, care buat komunitas",
}

KARMIC_DEBTS = {13, 14, 16, 19}
KARMIC_DEBT_MEANINGS = {
    13: "kerja keras & disiplin berat — gampang ngerasa males atau stuck, tapi harus push terus buat manifest",
    14: "belajar batesin kebebasan & komitmen — bahaya kecanduan / lepas kendali kalau ga dijaga",
    16: "ego & kesombongan bakal diruntuhin — butuh ketenangan, relasi toxic bakal hancur sendiri",
    19: "belajar mandiri tanpa merugikan orang lain — balance independence dan empati",
}

LESSON_MEANINGS = {
    1: "belajar berdiri sendiri & ambil pimpinan — kadang terlalu nurut / nunggu orang mulai duluan",
    2: "belajar kerjasama & diplomasi — kadang terlalu egois / ga sabar sama tempo orang lain",
    3: "belajar ekspresi diri & joy — kadang terlalu serius / kaku buat self-expression",
    4: "belajar disiplin & struktur — kadang berantakan, susah fokus ke detail",
    5: "belajar adaptif & embrace change — kadang kaku / takut sama hal baru",
    6: "belajar tanggung jawab pada keluarga & orang lain — kadang cenderung avoidance",
    7: "belajar inner work & kepercayaan — kadang terlalu permukaan, butuh ruang sendiri",
    8: "belajar kelola power & uang — kadang menghindar dari ambisi / urusan material",
    9: "belajar kasih sayang universal — kadang terlalu personal / sulit lepas",
}


def _detect_karmic_debt(raw_sum: int) -> int | None:
    n = raw_sum
    while n > 9 and n not in MASTER_NUMBERS:
        if n in KARMIC_DEBTS:
            return n
        n = sum(int(d) for d in str(n))
    return None


def life_path_karmic(dob: date) -> int | None:
    m = reduce_number(dob.month)
    d = reduce_number(dob.day)
    y = reduce_number(digit_sum(dob.year))
    return _detect_karmic_debt(m + d + y)


def expression_karmic(name: str) -> int | None:
    total = sum(PYTHAGOREAN[ch] for ch in name.upper() if ch in PYTHAGOREAN)
    return _detect_karmic_debt(total)


def soul_urge_karmic(name: str) -> int | None:
    total = sum(PYTHAGOREAN[ch] for ch in name.upper() if ch in VOWELS)
    return _detect_karmic_debt(total)


def personality_karmic(name: str) -> int | None:
    total = sum(
        PYTHAGOREAN[ch] for ch in name.upper()
        if ch in PYTHAGOREAN and ch not in VOWELS
    )
    return _detect_karmic_debt(total)


def karmic_lessons(name: str) -> list[int]:
    present = {PYTHAGOREAN[ch] for ch in name.upper() if ch in PYTHAGOREAN}
    return sorted(set(range(1, 10)) - present)


def hidden_passion(name: str) -> list[int]:
    from collections import Counter
    counts = Counter(PYTHAGOREAN[ch] for ch in name.upper() if ch in PYTHAGOREAN)
    if not counts:
        return []
    max_count = max(counts.values())
    return sorted([n for n, c in counts.items() if c == max_count])


def maturity_number(life_path_num: int, expression_num: int) -> int:
    return reduce_number(life_path_num + expression_num)


def balance_number(full_name: str) -> int:
    total = 0
    for word in full_name.upper().split():
        for ch in word:
            if ch in PYTHAGOREAN:
                total += PYTHAGOREAN[ch]
                break
    return reduce_number(total)


def rational_thought(birthday_num: int, expression_num: int) -> int:
    return reduce_number(birthday_num + expression_num)


def _first_pinnacle_end_age(lp: int) -> int:
    lp_reduced = lp if lp not in MASTER_NUMBERS else reduce_number(lp // 10 + lp % 10)
    return 36 - lp_reduced


def pinnacles(dob: date) -> list[dict]:
    m = reduce_number(dob.month)
    d = reduce_number(dob.day)
    y = reduce_number(digit_sum(dob.year))
    p1 = reduce_number(m + d)
    p2 = reduce_number(d + y)
    p3 = reduce_number(p1 + p2)
    p4 = reduce_number(m + y)
    lp = life_path(dob)
    end1 = _first_pinnacle_end_age(lp)
    return [
        {"period": 1, "start_age": 0, "end_age": end1, "number": p1},
        {"period": 2, "start_age": end1 + 1, "end_age": end1 + 9, "number": p2},
        {"period": 3, "start_age": end1 + 10, "end_age": end1 + 18, "number": p3},
        {"period": 4, "start_age": end1 + 19, "end_age": None, "number": p4},
    ]


def _abs_reduce(n: int) -> int:
    n = abs(n)
    while n > 9 and n not in MASTER_NUMBERS:
        n = sum(int(d) for d in str(n))
    return n


def challenges(dob: date) -> list[dict]:
    m = reduce_number(dob.month)
    d = reduce_number(dob.day)
    y = reduce_number(digit_sum(dob.year))
    c1 = _abs_reduce(m - d)
    c2 = _abs_reduce(d - y)
    c3 = _abs_reduce(c1 - c2)
    c4 = _abs_reduce(m - y)
    lp = life_path(dob)
    end1 = _first_pinnacle_end_age(lp)
    return [
        {"period": 1, "start_age": 0, "end_age": end1, "number": c1},
        {"period": 2, "start_age": end1 + 1, "end_age": end1 + 9, "number": c2},
        {"period": 3, "start_age": end1 + 10, "end_age": end1 + 18, "number": c3},
        {"period": 4, "start_age": end1 + 19, "end_age": None, "number": c4},
    ]


def current_pinnacle_challenge(dob: date, today: date) -> dict:
    age = (today - dob).days // 365
    pins = pinnacles(dob)
    chals = challenges(dob)
    for i, p in enumerate(pins):
        end = p["end_age"] if p["end_age"] is not None else 999
        if age <= end:
            return {
                "age": age,
                "period": p["period"],
                "pinnacle": p["number"],
                "challenge": chals[i]["number"],
            }
    return {
        "age": age,
        "period": 4,
        "pinnacle": pins[-1]["number"],
        "challenge": chals[-1]["number"],
    }


PINNACLE_MEANINGS = {
    1: "fase kepemimpinan & inisiatif — saat jadi diri sendiri, berani ambil risiko",
    2: "fase sabar & bangun hubungan — diplomasi, kerja dengan orang lain",
    3: "fase ekspresi & kreativitas — karya, sosial, joy",
    4: "fase kerja keras & fondasi — bangun sistem, disiplin, stabilitas",
    5: "fase perubahan & kebebasan — adventure, eksplor hal baru",
    6: "fase tanggung jawab & keluarga — komitmen, nurture orang terdekat",
    7: "fase introspektif & spiritual — refleksi, cari wisdom, inner work",
    8: "fase power & pencapaian — karir, finansial, legacy",
    9: "fase penutupan & humanis — legacy, service, letting go",
    11: "master pinnacle — awakening, jadi inspirator",
    22: "master pinnacle — building impact jangka panjang",
    33: "master pinnacle — service ke komunitas besar",
}

CHALLENGE_MEANINGS = {
    0: "tantangan universal — dari dalem diri sendiri, eksplorasi karakter bebas",
    1: "tantangan assertiveness — belajar stand up buat diri sendiri tanpa ego",
    2: "tantangan kesabaran & kerja sama — kelola sensitivity, ga over-people-pleasing",
    3: "tantangan ekspresi — kelola mood swing, jangan kebawa emosi",
    4: "tantangan disiplin & detail — kelola rasa stuck / kewalahan sama rutinitas",
    5: "tantangan kebebasan — jangan lari dari komitmen atau kecanduan sensasi",
    6: "tantangan responsibility — balance antara ngurus orang & diri sendiri",
    7: "tantangan kepercayaan — jangan isolate diri, belajar open-up ke orang",
    8: "tantangan power & uang — belajar equitable dengan uang & autoritas",
}


def build_profile(
    full_name: str,
    dob: date,
    today: date | None = None,
    nickname: str | None = None,
) -> dict:
    today = today or today_local()
    lp = life_path(dob)
    ex = expression_number(full_name)
    su = soul_urge_number(full_name)
    pe = personality_number(full_name)
    bd = birthday_number(dob)
    py = personal_year(dob, today)
    pm = personal_month(dob, today)
    pd = personal_day(dob, today)
    debts = {
        "life_path": life_path_karmic(dob),
        "expression": expression_karmic(full_name),
        "soul_urge": soul_urge_karmic(full_name),
        "personality": personality_karmic(full_name),
    }
    lessons = karmic_lessons(full_name)
    passion = hidden_passion(full_name)
    maturity = maturity_number(lp, ex)
    balance = balance_number(full_name)
    rational = rational_thought(bd, ex)
    pins = pinnacles(dob)
    chals = challenges(dob)
    current = current_pinnacle_challenge(dob, today)
    nick = (nickname or "").strip() or full_name.strip().split()[0]
    return {
        "full_name": full_name,
        "nickname": nick,
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
        "karmic_debts": debts,
        "karmic_lessons": lessons,
        "hidden_passion": passion,
        "maturity": maturity,
        "balance": balance,
        "rational_thought": rational,
        "pinnacles": pins,
        "challenges": chals,
        "current_phase": current,
        "meanings": {
            "life_path": MEANINGS[lp],
            "expression": MEANINGS[ex],
            "soul_urge": MEANINGS[su],
            "personality": MEANINGS[pe],
            "birthday": MEANINGS[bd],
            "personal_year": YEAR_THEMES[py],
            "personal_month": MONTH_THEMES[pm],
            "personal_day": DAILY_VIBES[pd],
            "maturity": MEANINGS[maturity],
            "balance": MEANINGS[balance],
            "rational_thought": MEANINGS[rational],
        },
    }
