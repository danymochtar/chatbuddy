from datetime import date

PYTHAGOREAN = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "O": 6, "P": 7, "Q": 8, "R": 9,
    "S": 1, "T": 2, "U": 3, "V": 4, "W": 5, "X": 6, "Y": 7, "Z": 8,
}
VOWELS = set("AEIOU")
MASTER_NUMBERS = {11, 22, 33}


def reduce_number(n: int) -> int:
    while n > 9 and n not in MASTER_NUMBERS:
        n = sum(int(d) for d in str(n))
    return n


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


def build_profile(full_name: str, dob: date) -> dict:
    lp = life_path(dob)
    ex = expression_number(full_name)
    su = soul_urge_number(full_name)
    pe = personality_number(full_name)
    bd = birthday_number(dob)
    return {
        "full_name": full_name,
        "dob": dob.isoformat(),
        "life_path": lp,
        "expression": ex,
        "soul_urge": su,
        "personality": pe,
        "birthday": bd,
        "meanings": {
            "life_path": MEANINGS[lp],
            "expression": MEANINGS[ex],
            "soul_urge": MEANINGS[su],
            "personality": MEANINGS[pe],
            "birthday": MEANINGS[bd],
        },
    }
