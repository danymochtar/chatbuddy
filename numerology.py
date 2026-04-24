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


def reduce_to_single(n: int) -> int:
    """Fully reduce to 1-9 — master numbers are NOT preserved.
    Used where Decoz says master should not stop reduction
    (Universal Day, Personal Day, Challenges)."""
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def chain_info(raw: int, keep_master: bool = True) -> dict:
    """Walk the reduction chain and report:
        raw            — the starting sum
        chain          — every step including raw and final
        final          — endpoint (master if keep_master and master appears, else 1-9)
        single         — endpoint forced to 1-9 (master ignored)
        masters        — master numbers appearing anywhere in chain
        karmic_debts   — karmic debt numbers (13/14/16/19) in chain
        notation       — "raw/final" or "raw/master/single" or "n" if no reduction
    """
    chain = [raw]
    n = raw
    if keep_master:
        while n > 9 and n not in MASTER_NUMBERS:
            n = sum(int(d) for d in str(n))
            chain.append(n)
    else:
        while n > 9:
            n = sum(int(d) for d in str(n))
            chain.append(n)
    final = chain[-1]
    single = final
    while single > 9:
        single = sum(int(d) for d in str(single))
    masters = [x for x in chain if x in MASTER_NUMBERS]
    debts = [x for x in chain if x in KARMIC_DEBTS]
    # Build notation: include master intermediates between raw and final
    parts = [chain[0]]
    for mid in chain[1:-1]:
        if mid in MASTER_NUMBERS:
            parts.append(mid)
    if final != chain[0]:
        parts.append(final)
    notation = "/".join(str(p) for p in parts) if len(parts) > 1 else str(parts[0])
    return {
        "raw": raw,
        "chain": chain,
        "final": final,
        "single": single,
        "masters": masters,
        "karmic_debts": debts,
        "notation": notation,
    }


# Forward declarations — KARMIC_DEBTS dict is defined later in the file but
# referenced by chain_info above. Define it early so the lookup works at module
# import time.


def digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))


def life_path(dob: date) -> int:
    return life_path_full(dob)["final"]


def life_path_full(dob: date) -> dict:
    """Hans Decoz: reduce Month, Day, Year separately first, then combine.

    This per-component reduction is what surfaces karmic debt at the
    summing stage (e.g. 5 + 8 + 6 = 19 — karmic debt 19 — even though
    every component reduces cleanly).
    """
    m_raw = dob.month
    d_raw = dob.day
    y_digits_sum = digit_sum(dob.year)
    m_red = reduce_number(m_raw)
    d_red = reduce_number(d_raw)
    y_red = reduce_number(y_digits_sum)
    total = m_red + d_red + y_red
    info = chain_info(total, keep_master=True)
    info["components"] = {
        "month": chain_info(m_raw, keep_master=True),
        "day": chain_info(d_raw, keep_master=True),
        "year": chain_info(y_digits_sum, keep_master=True),
    }
    return info


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


def _name_words(full_name: str) -> list[str]:
    """Split full name into individual word components, uppercased,
    keeping only words that contain any letters."""
    return [w for w in full_name.upper().split() if any(c in PYTHAGOREAN for c in w)]


def _word_letter_sum(word: str, only_vowels: bool = False, only_consonants: bool = False) -> int:
    total = 0
    for ch in word:
        if ch not in PYTHAGOREAN:
            continue
        if only_vowels and ch not in VOWELS:
            continue
        if only_consonants and ch in VOWELS:
            continue
        total += PYTHAGOREAN[ch]
    return total


def _name_full(full_name: str, *, only_vowels: bool = False, only_consonants: bool = False) -> dict:
    """Hans Decoz: reduce each name (first/middle/last) separately, then
    combine. Preserves master numbers + karmic debts that appear at
    component level."""
    words = _name_words(full_name)
    per_word = []
    for w in words:
        raw = _word_letter_sum(w, only_vowels=only_vowels, only_consonants=only_consonants)
        info = chain_info(raw, keep_master=True)
        info["word"] = w
        per_word.append(info)
    total = sum(w["final"] for w in per_word)
    overall = chain_info(total, keep_master=True)
    overall["per_word"] = per_word
    return overall


def expression_full(full_name: str) -> dict:
    return _name_full(full_name)


def soul_urge_full(full_name: str) -> dict:
    return _name_full(full_name, only_vowels=True)


def personality_full(full_name: str) -> dict:
    return _name_full(full_name, only_consonants=True)


def expression_number(name: str) -> int:
    return expression_full(name)["final"]


def soul_urge_number(name: str) -> int:
    return soul_urge_full(name)["final"]


def personality_number(name: str) -> int:
    return personality_full(name)["final"]


def birthday_number(dob: date) -> int:
    return reduce_number(dob.day)


def birthday_full(dob: date) -> dict:
    """Full Birth Day info — preserves the double digit so karmic debts
    (13, 14, 16, 19) and master Birth Days (11, 22) surface naturally.
    Day 22 stays 22 (master), day 13 reduces to 4 with karmic 13 in chain,
    etc."""
    return chain_info(dob.day, keep_master=True)


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
    # Hans Decoz: daily vibration is ALWAYS fully reduced to 1-9. Master
    # numbers can appear as intermediates in the chain (captured in
    # personal_cycles_full) but the day's primary energy is single digit.
    pm = personal_month(dob, today)
    n = pm + today.day
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def universal_day(today: date) -> int:
    # Per Decoz: Universal Day & Personal Day are always 1-9 — master
    # numbers do NOT stop the reduction.
    digits = [int(d) for d in today.strftime("%d%m%Y")]
    return reduce_to_single(sum(digits))


def universal_day_full(today: date) -> dict:
    digits = [int(d) for d in today.strftime("%d%m%Y")]
    return chain_info(sum(digits), keep_master=False)


def _reduce_stop_at_master(raw: int) -> tuple[str, int]:
    """Reduce until single digit OR master number, preserving master.
    Returns (notation, final). Notation shows raw/final or just final if same.
    """
    n = raw
    while n > 9 and n not in MASTER_NUMBERS:
        n = sum(int(d) for d in str(n))
    if raw == n:
        return str(n), n
    return f"{raw}/{n}", n


def _reduce_full_with_chain(raw: int) -> tuple[str, int, list[int]]:
    """Reduce ALL the way to single digit (1-9). Chain tracks master
    intermediates so notation can show them. Used for Personal Day where
    the daily vibration is always single-digit but master intermediates
    add flavor.

    Returns (notation, final_single_digit, master_intermediates).
    Notation format examples: '29/11/2', '25/7', '7'.
    """
    chain = [raw]
    n = raw
    while n > 9:
        n = sum(int(d) for d in str(n))
        chain.append(n)
    final = chain[-1]
    masters = [x for x in chain if x in MASTER_NUMBERS]
    parts = [chain[0]]
    for mid in chain[1:-1]:
        if mid in MASTER_NUMBERS:
            parts.append(mid)
    parts.append(final)
    if len(parts) == 2 and parts[0] == parts[1]:
        return str(final), final, masters
    return "/".join(str(p) for p in parts), final, masters


def personal_cycles_full(dob: date, today: date) -> dict:
    """Hans Decoz personal cycles for the given dob at the given today.

    - Personal Year uses TODAY's year (Universal Year), not the birth year.
    - Personal Year & Personal Month: master numbers PRESERVED (big-picture
      cycles where master matters).
    - Personal Day: FULLY reduced to 1-9 — master intermediates recorded
      in the chain + notation, but the vibration for the day is always
      single digit (e.g. 29 → 11 → 2).
    """
    bm = reduce_number(dob.month)
    bd = reduce_number(dob.day)
    cy = reduce_number(digit_sum(today.year))

    py_raw = bm + bd + cy
    py_notation, py_reduced = _reduce_stop_at_master(py_raw)

    cm = reduce_number(today.month)
    pm_raw = py_reduced + cm
    pm_notation, pm_reduced = _reduce_stop_at_master(pm_raw)

    pd_raw = pm_reduced + today.day
    pd_notation, pd_reduced, pd_masters = _reduce_full_with_chain(pd_raw)

    all_masters = set(pd_masters)
    if py_reduced in MASTER_NUMBERS:
        all_masters.add(py_reduced)
    if pm_reduced in MASTER_NUMBERS:
        all_masters.add(pm_reduced)

    return {
        "py": {"raw": py_raw, "reduced": py_reduced, "notation": py_notation},
        "pm": {"raw": pm_raw, "reduced": pm_reduced, "notation": pm_notation},
        "pd": {"raw": pd_raw, "reduced": pd_reduced, "notation": pd_notation},
        "master_numbers": sorted(all_masters),
    }


ARCHETYPES = {
    1: "Pemimpin",
    2: "Pendamai",
    3: "Kreatif",
    4: "Pekerja",
    5: "Petualang",
    6: "Penyayang",
    7: "Pemikir",
    8: "Ambisius",
    9: "Idealis",
    11: "Visioner",
    22: "Pembangun",
    33: "Guru",
}

# Short label companions for compact display (sidebar, quick reference)
KARMIC_DEBT_SHORT = {
    13: "disiplin & kerja keras",
    14: "kelola kebebasan",
    16: "lepas ego",
    19: "balance mandiri & empati",
}

LESSON_SHORT = {
    1: "berani ambil pimpinan",
    2: "belajar kerjasama",
    3: "ekspresi diri",
    4: "disiplin & struktur",
    5: "adaptif ke perubahan",
    6: "tanggung jawab orang terdekat",
    7: "inner work & refleksi",
    8: "kelola power & uang",
    9: "kasih tanpa pamrih",
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


def cornerstone(full_name: str) -> str:
    """First letter of first name — how you approach opportunities & obstacles."""
    words = _name_words(full_name)
    if not words:
        return ""
    for ch in words[0]:
        if ch in PYTHAGOREAN:
            return ch
    return ""


def capstone(full_name: str) -> str:
    """Last letter of first name — how you finish what you start."""
    words = _name_words(full_name)
    if not words:
        return ""
    for ch in reversed(words[0]):
        if ch in PYTHAGOREAN:
            return ch
    return ""


def first_vowel(full_name: str) -> str:
    """First vowel of first name — private, soul-level window into deepest motivations."""
    words = _name_words(full_name)
    if not words:
        return ""
    for ch in words[0]:
        if ch in VOWELS:
            return ch
    return ""


# Decoz letter meanings (synthesized) — used for Cornerstone, Capstone, First Vowel
LETTER_MEANINGS = {
    "A": "ambisius, mandiri, inisiatif, cepat ambil keputusan",
    "B": "sensitif, emosional, butuh harmoni & koneksi",
    "C": "ekspresif, cerah, sosial, suka komunikasi",
    "D": "praktis, terstruktur, pekerja keras, no-nonsense",
    "E": "free spirit, banyak ide, butuh variasi & gerak",
    "F": "responsibility, caring, berorientasi keluarga & komunitas",
    "G": "introspektif, perfeksionis, deep thinker",
    "H": "ambisi material, fokus pencapaian, organisator",
    "I": "intens, passionate, emotional depth",
    "J": "leader, innovator, butuh control & arah sendiri",
    "K": "intuitif, tegang, high-strung, channel inspirasi",
    "L": "selflessness, servis, kasih tanpa pamrih (sometimes too much)",
    "M": "pekerja keras, stabil, pondasi, pengayom",
    "N": "kreatif, ekspresif, kadang impulsif, butuh outlet",
    "O": "tertutup, hati-hati, butuh ruang aman & boundary",
    "P": "intelektual, analitis, butuh waktu sendiri",
    "Q": "tegang/intens, magnetik, kadang kontradiktif",
    "R": "tolerant, peduli orang banyak, humanitarian",
    "S": "drama, emotional waves, charisma & turbulence",
    "T": "spiritual, restless, mencari yang lebih besar",
    "U": "artistik, generous, sensitif terhadap keindahan",
    "V": "visioner, master builder, ambisi besar",
    "W": "creative restlessness, banyak ide tapi sulit fokus",
    "X": "intens, sensual, magnetic & complicated",
    "Y": "ragu-ragu antara dua dunia, dualitas, butuh berani pilih",
    "Z": "harapan, optimis, ambisi tertinggi",
}


def subconscious_self(full_name: str) -> int:
    """Decoz: 9 minus the number of Karmic Lessons (missing numbers in
    full birth name). Range 3-9. Higher = more numerical "tools" in
    the name → more confident in surprise situations."""
    return 9 - len(karmic_lessons(full_name))


SUBCONSCIOUS_SELF_MEANINGS = {
    3: "Karakter belum lengkap — banyak situasi yang masih bikin lo bingung. Rentan panik di hal baru, tapi cepet adaptasi kalau udah dilatih.",
    4: "Beberapa area diri lo masih rapuh. Saat di luar zona nyaman, perlu waktu buat kalibrasi. Tapi sekali ngerti, lo solid.",
    5: "Mid-range — ada gap kepercayaan diri di beberapa situasi. Lo bisa pas-pasan sampai bagus, tergantung konteks.",
    6: "Lumayan tools-mu lengkap. Kebanyakan situasi bisa lo handle, tapi jangan over-confident karena masih ada blind spot.",
    7: "Cukup confident dalam banyak situasi — kalau ada yang surprise, biasanya lo cepet recover dan find footing.",
    8: "Hampir semua tools ada. Confident, jarang panik, bisa improvise di hampir semua situasi sosial / emosional.",
    9: "Semua angka 1-9 hadir di nama lo — confident penuh. Awas: bisa tergelincir ke aloof / over-confident di situasi yang sebenernya butuh humility.",
}


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
    """Backward-compat shim — DEPRECATED. The previous formula
    (birthday + expression) was wrong per Decoz. New code should call
    rational_thought_full(full_name, dob)."""
    return reduce_number(birthday_num + expression_num)


def rational_thought_full(full_name: str, dob: date) -> dict:
    """Decoz: sum of letters in first name + Birth Day number.
    Master numbers preserved."""
    words = _name_words(full_name)
    first_name_sum = _word_letter_sum(words[0]) if words else 0
    raw = first_name_sum + dob.day
    return chain_info(raw, keep_master=True)


def period_cycles(dob: date) -> list[dict]:
    """Decoz Three Period Cycles — the three chapters of your Life Path.

    - Period 1 = birth month (master preserved). From birth to the first
      Personal Year 1 that lands on age ≥ 27.
    - Period 2 = birth day (master preserved). Lasts 27 years.
    - Period 3 = birth year reduced (master preserved). Rest of life.
    """
    bm = reduce_number(dob.month)
    bd = reduce_number(dob.day)
    by = reduce_number(digit_sum(dob.year))

    # Locate the first Personal Year 1 that occurs on or after age 27.
    transition_year: int | None = None
    base_year = dob.year + 27
    for y in range(base_year, base_year + 9):
        uy = reduce_number(digit_sum(y))
        py = reduce_number(bm + bd + uy)
        if py == 1:
            transition_year = y
            break
    if transition_year is None:
        transition_year = base_year

    p1_end_age = transition_year - dob.year

    return [
        {"period": 1, "number": bm, "start_age": 0, "end_age": p1_end_age},
        {"period": 2, "number": bd, "start_age": p1_end_age + 1, "end_age": p1_end_age + 27},
        {"period": 3, "number": by, "start_age": p1_end_age + 28, "end_age": None},
    ]


def current_period_cycle(dob: date, today: date) -> dict:
    age = (today - dob).days // 365
    cycles = period_cycles(dob)
    for cyc in cycles:
        end = cyc["end_age"] if cyc["end_age"] is not None else 999
        if age <= end:
            return {**cyc, "age": age}
    return {**cycles[-1], "age": age}


PERIOD_CYCLE_MEANINGS = {
    1: "Babak inisiatif & jadi diri sendiri — fondasi self-direction.",
    2: "Babak hubungan & sensitivity — belajar diplomasi & cooperation.",
    3: "Babak ekspresi & sosial — kreativitas, comunication, joy of being seen.",
    4: "Babak kerja keras & fondasi material — disiplin, building, security.",
    5: "Babak perubahan & freedom — adventure, eksplorasi, banyak shift.",
    6: "Babak tanggung jawab & care — keluarga, komitmen, healing orang.",
    7: "Babak introspektif & wisdom — solo work, study, spiritual.",
    8: "Babak power & material achievement — karir, pengaruh, autoritas.",
    9: "Babak humanis & legacy — service, completion, lepas dari ego personal.",
    11: "Babak master 11 — channeling intuisi, jadi inspirator.",
    22: "Babak master 22 — building skala besar, monumen yg lasting.",
    33: "Babak master 33 — service universal, kasih tanpa syarat.",
}


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

    lp_info = life_path_full(dob)
    ex_info = expression_full(full_name)
    su_info = soul_urge_full(full_name)
    pe_info = personality_full(full_name)
    bd_info = birthday_full(dob)
    rt_info = rational_thought_full(full_name, dob)
    ud_info = universal_day_full(today)

    lp = lp_info["final"]
    ex = ex_info["final"]
    su = su_info["final"]
    pe = pe_info["final"]
    bd = bd_info["final"]
    rational = rt_info["final"]

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
    pins = pinnacles(dob)
    chals = challenges(dob)
    current = current_pinnacle_challenge(dob, today)
    nick = (nickname or "").strip() or full_name.strip().split()[0]

    return {
        "full_name": full_name,
        "nickname": nick,
        "dob": dob.isoformat(),
        "today": today.isoformat(),
        # Core numbers — final value (master-preserved where Decoz says so)
        "life_path": lp,
        "expression": ex,
        "soul_urge": su,
        "personality": pe,
        "birthday": bd,
        # Cycles
        "personal_year": py,
        "personal_month": pm,
        "personal_day": pd,
        # Karmic + supporting
        "karmic_debts": debts,
        "karmic_lessons": lessons,
        "hidden_passion": passion,
        "maturity": maturity,
        "balance": balance,
        "rational_thought": rational,
        "pinnacles": pins,
        "challenges": chals,
        "current_phase": current,
        # Rich chain_info dicts (notation, components, masters, karmic intermediates)
        "info": {
            "life_path": lp_info,
            "expression": ex_info,
            "soul_urge": su_info,
            "personality": pe_info,
            "birthday": bd_info,
            "rational_thought": rt_info,
            "universal_day_today": ud_info,
        },
        "meanings": {
            "life_path": MEANINGS[lp],
            "expression": MEANINGS[ex],
            "soul_urge": MEANINGS[su],
            "personality": MEANINGS[pe],
            "birthday": MEANINGS[bd] if bd in MEANINGS else MEANINGS.get(reduce_to_single(bd), ""),
            "personal_year": YEAR_THEMES[py],
            "personal_month": MONTH_THEMES[pm],
            "personal_day": DAILY_VIBES[pd],
            "maturity": MEANINGS[maturity],
            "balance": MEANINGS[balance],
            "rational_thought": MEANINGS[rational],
        },
    }
