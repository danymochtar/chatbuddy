import json
import os
from datetime import date, datetime, time

import anthropic
import streamlit as st

from numerology import (
    ARCHETYPES,
    KARMIC_DEBT_MEANINGS,
    LESSON_MEANINGS,
    PINNACLE_MEANINGS,
    CHALLENGE_MEANINGS,
    build_profile,
    today_local,
)
from zodiac import (
    JAKARTA_COORDS,
    SIGN_TRAITS,
    chinese_zodiac,
    compute_chart,
    geocode_city,
    sun_sign,
    weton,
)

MODEL = "claude-haiku-4-5"
MAX_TOKENS = 3000
STORAGE_KEY = "chatbuddy_session_v1"

TEXTS = {
    "subtitle": {
        "id": "Temen AI lo buat refleksi diri",
        "en": "Your AI friend for self-reflection",
    },
    "kenalan": {"id": "Kenalan dulu yuk", "en": "Let's get to know you"},
    "name_label": {
        "id": "Nama lengkap (sesuai akta lahir)",
        "en": "Full name (as on birth certificate)",
    },
    "name_help": {
        "id": "Angka-angkanya dihitung dari nama ini",
        "en": "Your numbers are calculated from this name",
    },
    "nick_label": {
        "id": "Panggilan / nickname (opsional)",
        "en": "Nickname (optional)",
    },
    "nick_placeholder": {
        "id": "Biarin kosong buat pake nama depan",
        "en": "Leave blank to use first name",
    },
    "nick_help": {
        "id": "Ini yg ChatBuddy pakai buat sapa lo",
        "en": "ChatBuddy will call you by this",
    },
    "dob_label": {"id": "Tanggal lahir", "en": "Date of birth"},
    "time_label": {
        "id": "Jam lahir (HH:MM, opsional)",
        "en": "Birth time (HH:MM, optional)",
    },
    "city_label": {
        "id": "Kota lahir (opsional)",
        "en": "Birth city (optional)",
    },
    "submit": {"id": "Mulai ngobrol →", "en": "Start chatting →"},
    "err_name": {
        "id": "Nama lengkapnya dong biar bisa dihitung 🙏",
        "en": "Please enter your full name 🙏",
    },
    "err_time": {
        "id": "Format jam lahir salah. Pake `HH:MM` ya (contoh `13:30`) atau kosongin.",
        "en": "Invalid time format. Use `HH:MM` (e.g. `13:30`) or leave empty.",
    },
    "chat_placeholder": {
        "id": "Tulis pertanyaan atau cerita lo...",
        "en": "Ask a question or share something...",
    },
    "nav_chat": {"id": "Beranda", "en": "Home"},
    "nav_karakter": {"id": "Karakter", "en": "Character"},
    "nav_inner": {"id": "Aspek Dalam", "en": "Inner Aspect"},
    "nav_karmic": {"id": "PR Hidup", "en": "Life Lessons"},
    "nav_arah": {"id": "Arah Bulan & Tahun", "en": "Month & Year Guide"},
    "nav_fase": {"id": "Fase Hidup", "en": "Life Phases"},
    "nav_zodiak": {"id": "Zodiak", "en": "Zodiac"},
    "nav_shio": {"id": "Shio", "en": "Chinese Zodiac"},
    "nav_weton": {"id": "Horoskop Jawa", "en": "Javanese Horoscope"},
    "nav_relationship": {"id": "Relationship", "en": "Relationship"},
    "angka_utama": {"id": "📊 Angka utama", "en": "📊 Core numbers"},
    "aspek_detail": {"id": "🔎 Detail aspek dalam", "en": "🔎 Deeper aspects detail"},
    "pr_hidup_label": {"id": "PR hidup", "en": "Life challenges"},
    "pelajaran_label": {"id": "Pelajaran hidup", "en": "Life lessons"},
    "pelajaran_kosong": {
        "id": "lengkap (semua angka ada di nama)",
        "en": "complete (all numbers present in name)",
    },
    "obsesi_label": {"id": "Obsesi tersembunyi", "en": "Hidden drive"},
    "versi_dewasa_label": {"id": "Versi dewasa lo", "en": "Mature version"},
    "reset": {"id": "Reset sesi", "en": "Reset session"},
    "storage_note": {
        "id": "💾 Sesi tersimpen di browser lo.",
        "en": "💾 Session is saved in your browser.",
    },
    "misi_hidup": {"id": "Misi Hidup", "en": "Life Mission"},
    "bakat_bawaan": {"id": "Bakat Bawaan", "en": "Natural Talent"},
    "panggilan_hati": {"id": "Panggilan Hati", "en": "Heart's Calling"},
    "aura_luar": {"id": "Aura Luar", "en": "Outer Aura"},
    "talenta_lahir": {"id": "Talenta Lahir", "en": "Birthday Gift"},
    "refresh": {"id": "🔄 Refresh", "en": "🔄 Refresh"},
    "rel_header": {"id": "💑 Relationship", "en": "💑 Relationship"},
    "rel_caption": {
        "id": "Liat dinamika karakter lo sama orang deket — pasangan, sahabat, keluarga. Tambahin nama & tanggal lahir mereka, nanti gw analisis chemistry-nya.",
        "en": "See your dynamic with someone close — partner, best friend, family. Add their name & birthday, and I'll analyze the chemistry.",
    },
    "rel_add": {"id": "➕ Tambah orang baru", "en": "➕ Add new person"},
    "rel_name": {
        "id": "Nama lengkap mereka",
        "en": "Their full name",
    },
    "rel_nick": {
        "id": "Panggilan (opsional)",
        "en": "Nickname (optional)",
    },
    "rel_dob": {
        "id": "Tanggal lahir mereka",
        "en": "Their date of birth",
    },
    "rel_relation": {"id": "Hubungan kalian", "en": "Your relationship"},
    "rel_relation_opts": {
        "id": ["pasangan", "sahabat", "keluarga", "temen kerja", "gebetan", "lainnya"],
        "en": ["partner", "best friend", "family", "coworker", "crush", "other"],
    },
    "rel_submit": {"id": "Analisa →", "en": "Analyze →"},
    "rel_err_name": {
        "id": "Nama-nya harus diisi 🙏",
        "en": "Name is required 🙏",
    },
    "rel_loading": {
        "id": "Gw baca dulu dinamikanya...",
        "en": "Reading your dynamic...",
    },
    "rel_empty": {
        "id": "Belum ada orang yang dianalisa. Tambahin di atas ☝️",
        "en": "No one added yet. Add above ☝️",
    },
}


def t(key: str) -> str:
    lang = st.session_state.get("language", "id")
    entry = TEXTS.get(key, {})
    return entry.get(lang, entry.get("id", key))


def _get_local_storage():
    try:
        from streamlit_local_storage import LocalStorage
        return LocalStorage()
    except Exception:
        return None


def save_session_to_storage() -> None:
    ls = _get_local_storage()
    if ls is None or st.session_state.profile is None:
        return
    try:
        data = {
            "profile": st.session_state.profile,
            "zodiac": st.session_state.zodiac,
            "messages": st.session_state.messages,
            "opening_generated": st.session_state.opening_generated,
            "cached_pages": st.session_state.get("cached_pages", {}),
            "relationships": st.session_state.get("relationships", []),
            "language": st.session_state.get("language", "id"),
        }
        ls.setItem(STORAGE_KEY, json.dumps(data))
    except Exception:
        pass


def load_session_from_storage() -> bool:
    ls = _get_local_storage()
    if ls is None:
        return False
    try:
        raw = ls.getItem(STORAGE_KEY)
        if not raw:
            return False
        data = json.loads(raw) if isinstance(raw, str) else raw
        if not isinstance(data, dict) or not data.get("profile"):
            return False
        st.session_state.profile = data["profile"]
        st.session_state.zodiac = data.get("zodiac")
        st.session_state.messages = data.get("messages", [])
        st.session_state.opening_generated = data.get("opening_generated", False)
        st.session_state.cached_pages = data.get("cached_pages", {})
        st.session_state.relationships = data.get("relationships", [])
        st.session_state.language = data.get("language", "id")

        # Backfill fields added after older sessions were first saved.
        profile = st.session_state.profile
        zodiac = st.session_state.zodiac or {}
        migrated = False
        try:
            dob = date.fromisoformat(profile["dob"])
        except Exception:
            dob = None

        if dob is not None:
            if not zodiac.get("shio"):
                zodiac["shio"] = chinese_zodiac(dob)
                migrated = True
                st.session_state.cached_pages.pop("shio", None)
            if not zodiac.get("weton"):
                zodiac["weton"] = weton(dob)
                migrated = True
                st.session_state.cached_pages.pop("weton", None)

        if "balance" not in profile or "rational_thought" not in profile \
                or "pinnacles" not in profile:
            try:
                today = today_local()
                nickname = profile.get("nickname")
                fresh = build_profile(
                    profile["full_name"], dob, today=today, nickname=nickname,
                )
                for key in (
                    "balance", "rational_thought", "pinnacles", "challenges",
                    "current_phase", "karmic_debts", "karmic_lessons",
                    "hidden_passion", "maturity",
                ):
                    if key in fresh and key not in profile:
                        profile[key] = fresh[key]
                profile.setdefault("meanings", {}).update(
                    {k: v for k, v in fresh["meanings"].items() if k not in profile["meanings"]}
                )
                migrated = True
                st.session_state.cached_pages.pop("fase", None)
                st.session_state.cached_pages.pop("inner", None)
            except Exception:
                pass

        if migrated:
            st.session_state.zodiac = zodiac
            try:
                save_session_to_storage()
            except Exception:
                pass
        return True
    except Exception:
        return False


def clear_session_storage() -> None:
    ls = _get_local_storage()
    if ls is None:
        return
    try:
        ls.deleteItem(STORAGE_KEY)
    except Exception:
        try:
            ls.setItem(STORAGE_KEY, "")
        except Exception:
            pass


def get_client() -> anthropic.Anthropic:
    api_key = st.secrets.get("ANTHROPIC_API_KEY") if hasattr(st, "secrets") else None
    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("ANTHROPIC_API_KEY belum di-set. Tambahin di Streamlit secrets atau env variable.")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)


def format_today_id(today: date) -> str:
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    months = [
        "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember",
    ]
    return f"{days[today.weekday()]}, {today.day} {months[today.month]} {today.year}"


def language_directive() -> str:
    lang = st.session_state.get("language", "id")
    if lang == "en":
        return (
            "**LANGUAGE: You MUST respond in casual English.** Use 'you/I', warm friend-like "
            "tone. Do not mix Indonesian words. When I give you Indonesian context terms "
            "like 'misi hidup', 'panggilan hati', 'aura luar', 'bakat bawaan', 'talenta "
            "lahir', translate them to English equivalents ('life mission', 'heart's "
            "calling', 'outer aura', 'natural talent', 'birthday gift'). Headings in "
            "English too.\n\n"
        )
    return (
        "**BAHASA: Lo WAJIB ngomong pake bahasa Indonesia casual** ('lo/gw' atau 'kamu/aku' "
        "nyesuain vibe user). Jangan campur English kecuali istilah umum.\n\n"
    )


def base_persona() -> str:
    return (
        language_directive()
        + "Lo adalah **ChatBuddy** — teman curhat AI yang *diam-diam* pake numerologi Pythagorean "
        "(sistem Hans Decoz / World Numerology) dan astrologi Barat sebagai lensa baca "
        "karakter + vibe user.\n\n"
        "**Tone:**\n"
        "- User nganggep lo temen curhat, BUKAN numerologist / astrologer.\n"
        "- **JANGAN sebut istilah teknis**: 'Life Path', 'Expression', 'Soul Urge', "
        "'Personality Number', 'Birthday Number', 'Personal Year/Month/Day', 'Sun sign', "
        "'Moon sign', 'Rising', 'Ascendant', 'natal chart', 'zodiac', 'astrologi', "
        "'numerologi', nama-nama rasi bintang (Taurus, Cancer, dll).\n"
        "- **Astrologi WAJIB invisible** — banyak orang skeptis. Sampein insight dari "
        "Sun/Moon/Rising sebagai observasi karakter, bukan sebagai reading. Contoh: bukan "
        "'Moon Sagittarius lo bikin lo butuh kebebasan', tapi 'di dalem, lo itu butuh banget "
        "ruang buat gerak, ga suka dikurung rutinitas'.\n"
        "- Numerologi boleh disinggung halus ('pola angka lahir lo'), tapi hindari istilah "
        "teknis + jangan sebut angkanya.\n"
        "- Pake bahasa karakter: 'misi hidup', 'bakat bawaan', 'panggilan hati', 'aura luar', "
        "'energi hari ini', 'vibe bulan ini', 'tema tahun ini'.\n"
        "- **Karmic debts & lessons**: jangan sebut 'karmic debt' atau 'karmic lesson'. Ubah "
        "jadi 'PR hidup lo', 'pelajaran yang harus lo kuasain', 'rem yang harus dijaga', 'tema "
        "yang keliatan absen dari karakter lo'. Blend ke narasi saat relevan.\n"
        "- **Hidden passion**: sampein sebagai 'obsesi tersembunyi lo' atau 'drive yang paling "
        "sering nongol'.\n"
        "- **Maturity number**: sampein sebagai 'lo akan grow into sosok yg ...' atau 'versi "
        "dewasa lo (sekitar umur 35+)'.\n"
        "- **Panggil user pake nickname yang disediain** di profil, bukan nama lengkap.\n\n"
        "**Gaya ngomong:**\n"
        "- Casual temen deket — 'lo/gw' atau 'kamu/aku' nyesuain vibe user\n"
        "- Empatik, ga judgemental, validate feelings dulu sebelum kasih saran\n"
        "- Pake paragraf naratif; bullet cuma buat tips / list yang emang perlu\n\n"
        "**Aturan:**\n"
        "- Ini lensa refleksi, bukan ramalan pasti — ingetin halus kalau user treating ini as "
        "future prediction.\n"
        "- Kalau user cerita masalah berat (mental health, krisis), tetep suportif tapi arahin "
        "ke bantuan profesional."
    )


def profile_block(profile: dict, zodiac: dict | None) -> str:
    nick = profile.get("nickname", profile["full_name"].split()[0])
    lines = [
        "=== PROFIL USER (konteks internal — jangan expose istilahnya) ===",
        f"Nama: {profile['full_name']}",
        f"Panggilan (pake ini saat sapaan): {nick}",
        f"Tanggal lahir: {profile['dob']}",
        "",
        "-- Baca karakter utama (pake archetype & angka dalam kurung seperlunya) --",
        f"Misi hidup → angka {profile['life_path']} ({ARCHETYPES[profile['life_path']]}): {profile['meanings']['life_path']}",
        f"Bakat bawaan → angka {profile['expression']} ({ARCHETYPES[profile['expression']]}): {profile['meanings']['expression']}",
        f"Panggilan hati → angka {profile['soul_urge']} ({ARCHETYPES[profile['soul_urge']]}): {profile['meanings']['soul_urge']}",
        f"Aura luar → angka {profile['personality']} ({ARCHETYPES[profile['personality']]}): {profile['meanings']['personality']}",
        f"Talenta lahir → angka {profile['birthday']} ({ARCHETYPES[profile['birthday']]}): {profile['meanings']['birthday']}",
    ]

    # Karmic + minor aspects
    minor_lines = []
    debts = profile.get("karmic_debts") or {}
    debt_labels = {
        "life_path": "misi hidup", "expression": "bakat bawaan",
        "soul_urge": "panggilan hati", "personality": "aura luar",
    }
    for k, v in debts.items():
        if v:
            minor_lines.append(
                f"KARMIC DEBT {v} di {debt_labels[k]} — {KARMIC_DEBT_MEANINGS[v]}"
            )
    lessons = profile.get("karmic_lessons") or []
    if lessons:
        minor_lines.append("Karmic lessons (angka yg ga ada di nama → butuh dipelajarin seumur hidup):")
        for n in lessons:
            minor_lines.append(f"  {n} ({ARCHETYPES[n]}): {LESSON_MEANINGS[n]}")
    passion = profile.get("hidden_passion") or []
    if passion:
        if len(passion) == 1:
            minor_lines.append(
                f"Hidden passion (drive terkuat, sering muncul): {passion[0]} "
                f"({ARCHETYPES[passion[0]]})"
            )
        else:
            names = ", ".join(f"{n} ({ARCHETYPES[n]})" for n in passion)
            minor_lines.append(f"Hidden passions (drive ganda, ada ikatan): {names}")
    maturity = profile.get("maturity")
    if maturity:
        minor_lines.append(
            f"Maturity number (fokus setelah umur ~35): {maturity} "
            f"({ARCHETYPES[maturity]}) — {profile['meanings']['maturity']}"
        )
    balance = profile.get("balance")
    if balance:
        minor_lines.append(
            f"Balance number (cara dia handle emosi saat stres): {balance} "
            f"({ARCHETYPES[balance]}) — {profile['meanings']['balance']}"
        )
    rational = profile.get("rational_thought")
    if rational:
        minor_lines.append(
            f"Rational thought (gaya proses mental / cara berpikir): {rational} "
            f"({ARCHETYPES[rational]}) — {profile['meanings']['rational_thought']}"
        )
    if minor_lines:
        lines += ["", "-- Minor aspects (buat kedalaman; blend halus saat relevan) --"]
        lines += minor_lines

    # Life phases (pinnacles & challenges)
    current = profile.get("current_phase") or {}
    pins = profile.get("pinnacles") or []
    chals = profile.get("challenges") or []
    if current and pins and chals:
        lines += ["", "-- Fase hidup (pinnacles & challenges; blend halus, jangan sebut istilah teknis) --"]
        lines.append(f"Umur user saat ini: {current.get('age')}")
        lines.append(
            f"Fase sekarang (period {current.get('period')}): "
            f"Pinnacle {current.get('pinnacle')} ({PINNACLE_MEANINGS.get(current.get('pinnacle'), '')}), "
            f"Challenge {current.get('challenge')} ({CHALLENGE_MEANINGS.get(current.get('challenge'), '')})"
        )
        lines.append("Semua pinnacles (fase peluang):")
        for p in pins:
            end = p["end_age"] if p["end_age"] is not None else "seterusnya"
            lines.append(
                f"  Fase {p['period']} (umur {p['start_age']}-{end}): pinnacle {p['number']} "
                f"({PINNACLE_MEANINGS.get(p['number'], '')})"
            )
        lines.append("Semua challenges (obstacle per fase):")
        for c in chals:
            end = c["end_age"] if c["end_age"] is not None else "seterusnya"
            lines.append(
                f"  Fase {c['period']} (umur {c['start_age']}-{end}): challenge {c['number']} "
                f"({CHALLENGE_MEANINGS.get(c['number'], '')})"
            )

    if zodiac and zodiac.get("sun"):
        lines += [
            "",
            "-- Lapisan tambahan (WAJIB DISEMBUNYIKAN — blend ke observasi, JANGAN sebut rasi / istilah) --",
            f"Cara dia tampil/bertindak (ego eksternal): {SIGN_TRAITS[zodiac['sun']]}",
        ]
        if zodiac.get("moon"):
            lines.append(f"Kebutuhan emosi internal / comfort zone: {SIGN_TRAITS[zodiac['moon']]}")
        if zodiac.get("rising"):
            lines.append(f"Vibe pertama orang liat dari dia: {SIGN_TRAITS[zodiac['rising']]}")
    return "\n".join(lines)


def daily_block(profile: dict, today: date) -> str:
    return (
        f"=== VIBE HARI INI ({format_today_id(today)}) ===\n"
        f"Tema tahun ini (angka {profile['personal_year']}): {profile['meanings']['personal_year']}\n"
        f"Vibe bulan ini (angka {profile['personal_month']}): {profile['meanings']['personal_month']}\n"
        f"Energi hari ini (angka {profile['personal_day']}): {profile['meanings']['personal_day']}\n\n"
        "Pake ini buat kasih konteks timing — tips hari ini, bulan, dan tahun dirangkum "
        "jadi satu panduan yg saling nyambung. JANGAN sebut 'Personal Day/Month/Year' — "
        "sampein kyk lo emang 'tau' vibe-nya."
    )


def system_prompt(profile: dict, zodiac: dict | None, today: date) -> list:
    text = "\n\n".join([base_persona(), profile_block(profile, zodiac), daily_block(profile, today)])
    return [{"type": "text", "text": text, "cache_control": {"type": "ephemeral"}}]


def opening_prompt() -> str:
    return (
        "Bikinin opening yang SINGKAT, hangat, personal — tone temen deket. "
        "**JANGAN sebut istilah teknis** (Life Path, Sun, Moon, zodiac, rasi bintang, dst). "
        "3 section aja, pake heading Markdown ##:\n\n"
        "## 👋 Halo [Nickname]\n"
        "1-2 kalimat synthesis yg blend karakter gw jadi SATU KESELURUHAN — mengalir, pake "
        "kata sambung ('yang', 'tapi', 'di dalemnya', 'walau'), **WAJIB sertakan angka dalam "
        "kurung** setelah trait-nya.\n\n"
        "Contoh tone (JANGAN copy persis):\n"
        "- _\"Hi Dany, lu itu born to be leader (1) yang natural-nya mengalir bebas (5), "
        "tapi di dalem jiwa lo itu penyayang banget (6) — dengan aura ambisius yang kerasa (8) "
        "plus talenta buat bikin dampak besar (8).\"_\n\n"
        "Angka master (11/22/33) kasih emphasis. Angka dobel blend jadi penekanan kuat.\n\n"
        "## 🌞 Vibe Hari Ini\n"
        "Sebutin hari & tanggal. Rangkai energi hari ini jadi cerita singkat (1 paragraf) + "
        "LANGSUNG lanjut dengan **3-4 tips praktis buat hari ini** (bullet points) — yg "
        "nyambung sama energi hari ini + karakter lo. Tips harus spesifik & actionable, bukan "
        "'be yourself' tapi aksi yg bisa langsung dikerjain.\n\n"
        "## 💬 Yuk Ngobrol\n"
        "1-2 kalimat invitation — undang ngobrol bebas, plus kasih tau kalau ada analisa "
        "lebih dalem (karakter, PR hidup, arah bulan/tahun, compatibility sama orang deket) "
        "bisa diakses lewat **menu di sidebar kiri**. Singkat aja.\n\n"
        "**Style:** casual 'lo/gw', hangat. **Zero jargon teknis**. Astrologi WAJIB invisible."
    )


def kompleksitas_prompt() -> str:
    return (
        "Tulis **analisa karakter mendalam** tentang gw (3-5 paragraf storytelling, bukan "
        "list). Gabungin semua lapisan jadi cerita utuh 'siapa lo': misi hidup, bakat bawaan, "
        "panggilan hati, aura luar, talenta lahir, PLUS lapisan cara tampil / emosi internal "
        "/ first impression (dari data lahir tambahan). Tunjukin:\n"
        "- Paradoks / harmoni antar aspek (misi vs bakat, luar vs dalem)\n"
        "- Kekuatan natural lo\n"
        "- Shadow / tendency yg harus diwaspadain\n"
        "- Bagaimana semua puzzle-piece ini nyambung jadi karakter unik lo\n\n"
        "Pake heading ## di atas (misal `## 👤 Kompleksitas Karakter Lo`). Sertakan angka "
        "dalam kurung saat nyebut trait kunci. **Zero istilah teknis.** Astrologi WAJIB "
        "invisible — sampein sebagai observasi biasa, bukan reading."
    )


def inner_prompt() -> str:
    return (
        "Tulis tentang **aspek dalam** gw — hal-hal yg ga kelihatan dari luar tapi jadi motor "
        "dalem. Fokus ke 4 hal:\n"
        "1. **Obsesi tersembunyi** (drive yg paling sering nongol, dari pola nama lo) — "
        "ini yg sering keluar di pilihan-pilihan kecil sehari-hari.\n"
        "2. **Versi dewasa lo** (siapa lo akan grow into setelah umur ~35) — bagaimana "
        "karakter lo bakal matang.\n"
        "3. **Cara lo handle emosi saat stres** (balance number) — respon natural lo saat "
        "kesusahan / tekanan.\n"
        "4. **Gaya berpikir lo** (rational thought) — cara natural lo memproses informasi "
        "& ambil keputusan mental.\n\n"
        "Pake heading ## di atas (misal `## 🔍 Aspek Dalam Lo`). 4-5 paragraf storytelling. "
        "Angka dalam kurung saat nyebut trait. **Zero istilah teknis** ('hidden passion', "
        "'maturity number', 'balance number', 'rational thought' dll JANGAN disebut)."
    )


def fase_prompt() -> str:
    return (
        "Tulis tentang **fase hidup** gw — perjalanan besar dari masa lampau, sekarang, "
        "sampai masa depan. Pake data pinnacles (4 fase peluang) + challenges (4 obstacle "
        "per fase) + umur gw sekarang.\n\n"
        "Struktur pake heading ##:\n\n"
        "## 🎯 Fase Hidup Lo\n"
        "1 paragraf intro — kasih tau bahwa hidup lo terbagi 4 fase besar, tiap fase punya "
        "peluang & tantangan spesifik.\n\n"
        "## ✨ Fase Sekarang\n"
        "Zoom-in ke fase lo saat ini: umur berapa sampai berapa, apa temanya, apa "
        "challenge-nya, bagaimana navigate-nya. 2 paragraf.\n\n"
        "## 🗺️ Peta Fase-Fase Lo\n"
        "Ringkasan 4 fase dalam list: untuk setiap fase sebutin rentang umur + tema peluang "
        "+ tantangan yg mendampingi. Format bullet atau numbered list.\n\n"
        "## 💡 Tips Buat Fase Sekarang\n"
        "2-3 tips actionable buat memaksimalkan fase yg lagi lo jalani. Spesifik sesuai "
        "karakter + tema fase.\n\n"
        "**Zero istilah teknis** ('pinnacle', 'challenge' dll JANGAN disebut — pake "
        "'fase', 'tantangan', 'peluang'). Tone: temen deket yg ngeliat peta hidup lo."
    )


def karmic_prompt() -> str:
    return (
        "Tulis tentang **PR hidup** lo — pelajaran besar yg harus dikuasain. Sampein sebagai "
        "'rem yang harus dijaga' atau 'tema yg harus lo embrace'. Fokus:\n"
        "1. Kalo ada karmic debt (13/14/16/19) di aspek tertentu — jelasin sebagai tantangan "
        "spesifik yg karma-related (ini rem, bukan kutukan). Kasih cara ngehadapinnya.\n"
        "2. Kalo ada angka absen dari nama (karmic lessons) — jelasin sebagai tema yg absen "
        "dari karakter bawaan lo, justru jadi pelajaran yg lo harus aktif latih.\n"
        "3. Kalo lessons kosong / debt kosong — jelasin bahwa karakter lo udah relatively "
        "balanced di aspek itu, PR-nya di level yg lebih halus.\n\n"
        "Pake heading ## di atas (misal `## 🎓 PR Hidup Lo`). 2-4 paragraf. Tone: suportif, "
        "bukan nakut-nakutin. **Zero istilah teknis**."
    )


def arah_prompt() -> str:
    return (
        "Tulis **panduan arah buat bulan ini + tahun ini** — dua section terpisah tapi "
        "terkait. Jangan bahas energi hari ini (udah di chat utama). Fokus:\n\n"
        "## 🗓️ Bulan Ini\n"
        "1 paragraf soal tema/vibe bulan ini. Terus 3-4 tips actionable buat sebulan ke "
        "depan — apa yg cocok diprioritize, apa yg bijak dihindari.\n\n"
        "## 🌱 Tahun Ini\n"
        "1 paragraf soal chapter besar tahun ini. Terus 3-4 tips zoom-out — apa yg bijak "
        "difokusin / di-release sepanjang tahun.\n\n"
        "Hubungkan bulan ↔ tahun (bulan ini adalah microstep dari tahun). Specific & "
        "actionable. **Zero istilah teknis**."
    )


def zodiak_prompt(zodiac: dict | None) -> str:
    if not zodiac or not zodiac.get("sun"):
        return (
            "User ga kasih data cukup buat baca astrologi barat. Kasih tau dgn hangat "
            "bahwa buat baca zodiak lengkap (sun, moon, rising), perlu nama lengkap, "
            "tanggal lahir, jam lahir, dan kota lahir. User bisa reset sesi kalo mau isi "
            "ulang. Di section ini CUMA page ini lo BOLEH sebut istilah astrologi "
            "terbuka — karena user udah opt-in dengan buka menu zodiak."
        )
    lines = [f"Sun: {zodiac['sun']}"]
    if zodiac.get("moon"):
        lines.append(f"Moon: {zodiac['moon']}")
    if zodiac.get("rising"):
        lines.append(f"Rising/Ascendant: {zodiac['rising']}")
    chart_data = "\n".join(lines)
    return (
        f"**DI PAGE INI SAJA lo BOLEH sebut istilah astrologi barat terbuka** (Sun, "
        f"Moon, Rising, nama rasi) — user udah opt-in dengan buka menu Zodiak. Di "
        f"page lain tetep invisible.\n\n"
        f"Data astrologi user:\n{chart_data}\n\n"
        "Bikin analisa zodiak yang hangat & personal, pake heading ##:\n\n"
        "## ☀️ Sun Sign Lo\n"
        "Jelasin Sun sign lo — karakter ego, cara tampil ke dunia, core identity. "
        "2 paragraf.\n\n"
        "## 🌙 Moon Sign Lo (kalo ada)\n"
        "Kalo Moon ada: emosi dalem, kebutuhan batin, comfort zone emosional. Kalo "
        "ga ada: skip section ini, kasih note kecil bahwa butuh jam lahir buat "
        "Moon sign.\n\n"
        "## 🌅 Rising Sign Lo (kalo ada)\n"
        "Kalo Rising ada: first impression, vibe yang orang liat pertama kali dari "
        "lo. Kalo ga ada: skip, note butuh jam + kota lahir.\n\n"
        "## 💫 Blend Jadi Satu\n"
        "Gimana semua lapisan ini bareng-bareng bentuk persona astrologi lo yang "
        "unik. 1-2 paragraf.\n\n"
        "Style: pake 'lo/gw', hangat, storytelling bukan list kering."
    )


def shio_prompt(zodiac: dict) -> str:
    shio = zodiac.get("shio") or {}
    return (
        f"**DI PAGE INI SAJA lo BOLEH sebut istilah shio / Chinese zodiac terbuka** — "
        f"user udah opt-in. Di page lain tetep invisible.\n\n"
        f"Data shio user:\n"
        f"- Elemen: {shio.get('element')} — {shio.get('element_traits')}\n"
        f"- Hewan shio: {shio.get('animal')} — {shio.get('animal_traits')}\n"
        f"- Gabungan: **{shio.get('label')}**\n\n"
        "Bikin analisa shio yang hangat & personal, pake heading ##:\n\n"
        "## 🐾 Shio Lo\n"
        "Kenalin shio lo dan karakter hewan nya. 2 paragraf tentang karakter "
        "hewan ini — kekuatan, pola perilaku, sifat khasnya.\n\n"
        "## ☯️ Elemen Lo\n"
        "Jelasin elemen lo (Kayu/Api/Tanah/Logam/Air) dan gimana elemen ini warna-in "
        "shio lo. 1-2 paragraf.\n\n"
        "## 🎯 Blend Shio × Elemen\n"
        "Gimana shio + elemen jadi karakter unik lo. Apa kekuatan natural dari "
        "kombinasi ini, apa tendency yg harus diwaspadain.\n\n"
        "## 💡 Tips Buat Lo\n"
        "2-3 tips praktis yang nyambung sama karakter shio + elemen lo.\n\n"
        "Style: casual 'lo/gw', storytelling."
    )


def weton_prompt(zodiac: dict) -> str:
    w = zodiac.get("weton") or {}
    return (
        f"**DI PAGE INI SAJA lo BOLEH bahas weton / horoskop Jawa terbuka** — user "
        f"udah opt-in. Di page lain tetep invisible.\n\n"
        f"Data weton user:\n"
        f"- Dina (hari lahir): {w.get('dina')} — {w.get('dina_traits')}\n"
        f"- Pasaran: {w.get('pasaran')} — {w.get('pasaran_traits')}\n"
        f"- Weton lengkap: **{w.get('weton')}**\n"
        f"- Neptu (total): {w.get('neptu')} — {w.get('neptu_meaning')}\n\n"
        "Bikin analisa weton yang hangat, sedikit filosofis ala Jawa, pake heading ##:\n\n"
        "## 🌿 Weton Lo\n"
        "Kenalin weton (hari + pasaran) dan apa artinya dalam tradisi Jawa. 1 "
        "paragraf intro singkat.\n\n"
        "## ☀️ Dina Lo\n"
        "Karakter dari hari lahir lo. 1-2 paragraf.\n\n"
        "## 🌙 Pasaran Lo\n"
        "Karakter dari pasaran lo (siklus 5-harian Jawa). 1-2 paragraf.\n\n"
        "## 🔢 Neptu Lo\n"
        "Jelasin neptu (total nilai dina + pasaran) dan apa artinya buat kekuatan "
        "aura lo. 1 paragraf.\n\n"
        "## 💫 Kearifan Buat Lo\n"
        "2-3 insight / wewaler / tuntunan yg relate sama weton lo. Nada-nya "
        "nasehat leluhur yg hangat, bukan mistis/serem.\n\n"
        "Style: casual tapi sedikit rasa Jawa (boleh sesekali pake kata Jawa kayak "
        "'laku', 'urip', 'sangkan paraning dumadi' kalo pas). 'Lo/gw' OK."
    )


def relationship_prompt(partner_profile: dict) -> str:
    nick = partner_profile.get("nickname") or partner_profile["full_name"].split()[0]
    p_lines = [
        f"Nama: {partner_profile['full_name']} (panggil: {nick})",
        f"Tanggal lahir: {partner_profile['dob']}",
        f"Misi hidup: {partner_profile['life_path']} ({ARCHETYPES[partner_profile['life_path']]}) — {partner_profile['meanings']['life_path']}",
        f"Bakat bawaan: {partner_profile['expression']} ({ARCHETYPES[partner_profile['expression']]}) — {partner_profile['meanings']['expression']}",
        f"Panggilan hati: {partner_profile['soul_urge']} ({ARCHETYPES[partner_profile['soul_urge']]}) — {partner_profile['meanings']['soul_urge']}",
        f"Aura luar: {partner_profile['personality']} ({ARCHETYPES[partner_profile['personality']]}) — {partner_profile['meanings']['personality']}",
        f"Talenta lahir: {partner_profile['birthday']} ({ARCHETYPES[partner_profile['birthday']]}) — {partner_profile['meanings']['birthday']}",
    ]
    partner_block = "\n".join(p_lines)
    return (
        f"Gw mau tau gimana dinamika gw sama orang ini:\n\n{partner_block}\n\n"
        "Pake konteks energi hari ini, vibe bulan ini, dan tema tahun ini gw juga (udah "
        "ada di system prompt) saat kasih insight timing.\n\n"
        "Bikinin analisa compatibility yg blend karakter gw vs karakter dia. Pake heading ##:\n\n"
        "## 💫 Chemistry Karakter\n"
        "Gimana personality lo dua nyambung atau gesekan. Sebutin aspek mana yg klop (dan "
        "kenapa), aspek mana yg bisa bikin friksi. Tunjukin dinamika kayak yin-yang.\n\n"
        "## 💬 Cara Komunikasi\n"
        "Gimana lo dua sebaiknya ngomong. Tone lo kyk apa, tone dia kyk apa, gimana "
        "ketemuin tengahnya.\n\n"
        "## 🌱 Growth Together\n"
        "2-3 tips actionable buat hubungan ini tumbuh. Waspadain vs hargain.\n\n"
        "## 🌞 Vibe Buat Hari Ini\n"
        "1-2 tips konkret buat hari ini berdasarkan energi hari ini lo (dari system prompt) — "
        "apa yg cocok lo dua lakuin bareng hari ini, apa yg bijak dihindari hari ini.\n\n"
        "## 🗓️ Vibe Bulan & Tahun Ini\n"
        "1 paragraf — kasih hint gimana dinamika hubungan ini bakal kerasa sepanjang "
        "bulan ini (vibe bulan lo) dan chapter tahun ini (tema tahun lo). Yg diperjuangin "
        "bulan ini vs yg bijak di-hold buat tahun ini.\n\n"
        "Style: temen curhat, bukan therapy session kaku. **Zero istilah teknis** (jangan "
        "sebut Life Path / zodiac / Personal Year dll — blend halus). Pake angka dalam "
        "kurung kalo perlu biar clear."
    )


def build_partner_profile(
    full_name: str,
    dob: date,
    nickname: str | None = None,
) -> dict:
    return build_profile(full_name, dob, nickname=nickname)


def to_anthropic_messages(messages: list) -> list:
    result = []
    started = False
    for msg in messages:
        if not started and msg["role"] != "user":
            continue
        started = True
        result.append({"role": msg["role"], "content": msg["content"]})
    return result


def stream_assistant(messages_for_api: list, system: list, placeholder) -> str:
    client = get_client()
    full_text = ""
    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=messages_for_api,
    ) as stream:
        for text in stream.text_stream:
            full_text += text
            placeholder.markdown(full_text + "▌")
    placeholder.markdown(full_text)
    return full_text


def render_profile_panel(profile: dict) -> None:
    cols = st.columns(5)
    panels = [
        ("Misi Hidup", "life_path"),
        ("Bakat Bawaan", "expression"),
        ("Panggilan Hati", "soul_urge"),
        ("Aura Luar", "personality"),
        ("Talenta Lahir", "birthday"),
    ]
    for col, (label, key) in zip(cols, panels):
        num = profile[key]
        with col:
            st.caption(label)
            st.markdown(f"### {num}")
            st.caption(f"_{ARCHETYPES[num]}_")
    st.divider()


def render_cached_text_page(
    page_key: str,
    prompt_fn,
    profile: dict,
    zodiac: dict | None,
) -> None:
    cached = st.session_state.get("cached_pages", {})
    text = cached.get(page_key)

    if text:
        st.markdown(text)
        col1, col2 = st.columns([1, 4])
        if col1.button(t("refresh"), key=f"refresh_{page_key}"):
            cached.pop(page_key, None)
            st.session_state.cached_pages = cached
            save_session_to_storage()
            st.rerun()
    else:
        placeholder = st.empty()
        new_text = stream_assistant(
            messages_for_api=[{"role": "user", "content": prompt_fn()}],
            system=system_prompt(profile, zodiac, today_local()),
            placeholder=placeholder,
        )
        cached[page_key] = new_text
        st.session_state.cached_pages = cached
        save_session_to_storage()


def render_relationship_page(profile: dict, zodiac: dict | None) -> None:
    st.header(t("rel_header"))
    st.caption(t("rel_caption"))

    with st.expander(t("rel_add")):
        with st.form("partner_form", clear_on_submit=True):
            p_name = st.text_input(t("rel_name"))
            p_nick = st.text_input(
                t("rel_nick"),
                placeholder="Default: nama depan" if st.session_state.language == "id" else "Default: first name",
            )
            p_dob = st.date_input(
                t("rel_dob"),
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                value=date(2000, 1, 1),
                format="DD/MM/YYYY",
            )
            p_relation = st.selectbox(
                t("rel_relation"),
                TEXTS["rel_relation_opts"][st.session_state.language],
            )
            add = st.form_submit_button(t("rel_submit"), use_container_width=True)

        if add:
            if not p_name.strip() or len(p_name.strip()) < 2:
                st.error(t("rel_err_name"))
            else:
                partner = build_partner_profile(
                    p_name.strip(), p_dob,
                    nickname=p_nick.strip() or None,
                )
                with st.spinner(t("rel_loading")):
                    placeholder = st.empty()
                    analysis = stream_assistant(
                        messages_for_api=[{"role": "user", "content": relationship_prompt(partner)}],
                        system=system_prompt(profile, zodiac, today_local()),
                        placeholder=placeholder,
                    )
                rels = st.session_state.get("relationships", [])
                rels.append({
                    "id": datetime.now().strftime("r_%Y%m%d%H%M%S"),
                    "partner_name": p_name.strip(),
                    "partner_nick": p_nick.strip() or p_name.strip().split()[0],
                    "partner_dob": p_dob.isoformat(),
                    "partner_profile": partner,
                    "relation_type": p_relation,
                    "analysis": analysis,
                    "created_at": datetime.now().isoformat(),
                })
                st.session_state.relationships = rels
                save_session_to_storage()
                st.rerun()

    rels = st.session_state.get("relationships", [])
    if not rels:
        st.info(t("rel_empty"))
        return

    for i, rel in enumerate(rels):
        with st.container(border=True):
            header_cols = st.columns([5, 1])
            header_cols[0].subheader(f"💫 {rel['partner_nick']} · _{rel['relation_type']}_")
            if header_cols[1].button("🗑️", key=f"del_rel_{rel['id']}"):
                rels.pop(i)
                st.session_state.relationships = rels
                save_session_to_storage()
                st.rerun()
            st.caption(f"{rel['partner_name']} · lahir {rel['partner_dob']}")
            st.markdown(rel["analysis"])


def handle_chat_turn(profile: dict, zodiac: dict | None) -> None:
    user_input = st.chat_input(t("chat_placeholder"))
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_text = stream_assistant(
                messages_for_api=to_anthropic_messages(st.session_state.messages),
                system=system_prompt(profile, zodiac, today_local()),
                placeholder=placeholder,
            )
        st.session_state.messages.append({"role": "assistant", "content": full_text})
        save_session_to_storage()


def build_full_profile(
    full_name: str,
    dob: date,
    birth_time: time | None,
    birth_city: str | None,
    nickname: str | None = None,
) -> tuple[dict, dict]:
    profile = build_profile(full_name, dob, nickname=nickname)
    zodiac = {
        "sun": sun_sign(dob),
        "moon": None,
        "rising": None,
        "birth_time": birth_time.strftime("%H:%M") if birth_time else None,
        "birth_city": birth_city,
        "shio": chinese_zodiac(dob),
        "weton": weton(dob),
    }
    if birth_time:
        lat, lon = JAKARTA_COORDS
        if birth_city:
            coords = geocode_city(birth_city)
            if coords:
                lat, lon = coords
        chart = compute_chart(dob, birth_time, lat, lon)
        if chart:
            zodiac["sun"] = chart["sun"]
            zodiac["moon"] = chart["moon"]
            if birth_city and coords:
                zodiac["rising"] = chart["rising"]
    return profile, zodiac


st.set_page_config(page_title="ChatBuddy", page_icon="🔮", layout="centered")

if "language" not in st.session_state:
    st.session_state.language = "id"

_lang_cols = st.columns([3, 1])
with _lang_cols[1]:
    _lang_choice = st.segmented_control(
        "language",
        options=["🇮🇩 ID", "🇺🇸 EN"],
        default="🇮🇩 ID" if st.session_state.language == "id" else "🇺🇸 EN",
        label_visibility="collapsed",
        key="_lang_toggle",
    )
    if _lang_choice:
        _new_lang = "id" if "ID" in _lang_choice else "en"
        if _new_lang != st.session_state.language:
            st.session_state.language = _new_lang
            st.session_state.cached_pages = {}
            if st.session_state.get("profile"):
                try:
                    save_session_to_storage()
                except Exception:
                    pass
            st.rerun()

st.title("🔮 ChatBuddy")
st.caption(t("subtitle"))

if "profile" not in st.session_state:
    st.session_state.profile = None
if "zodiac" not in st.session_state:
    st.session_state.zodiac = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "opening_generated" not in st.session_state:
    st.session_state.opening_generated = False
if "cached_pages" not in st.session_state:
    st.session_state.cached_pages = {}
if "relationships" not in st.session_state:
    st.session_state.relationships = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "chat"

if "storage_loaded" not in st.session_state:
    if st.session_state.profile is None:
        load_session_from_storage()
    st.session_state.storage_loaded = True

if st.session_state.profile is None:
    st.subheader(t("kenalan"))
    with st.form("profile_form"):
        full_name = st.text_input(
            t("name_label"),
            placeholder="Contoh: Budi Santoso" if st.session_state.language == "id" else "Example: Jane Doe",
            help=t("name_help"),
        )
        nickname = st.text_input(
            t("nick_label"),
            placeholder=t("nick_placeholder"),
            help=t("nick_help"),
        )
        dob = st.date_input(
            t("dob_label"),
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            value=date(2000, 1, 1),
            format="DD/MM/YYYY",
        )
        col_time, col_city = st.columns(2)
        with col_time:
            birth_time_str = st.text_input(t("time_label"), placeholder="13:30")
        with col_city:
            birth_city = st.text_input(t("city_label"), placeholder="Jakarta")
        submitted = st.form_submit_button(t("submit"), use_container_width=True)

    if submitted:
        if not full_name.strip() or len(full_name.strip()) < 2:
            st.error(t("err_name"))
        else:
            birth_time_obj = None
            if birth_time_str.strip():
                for fmt in ("%H:%M", "%H.%M"):
                    try:
                        birth_time_obj = datetime.strptime(birth_time_str.strip(), fmt).time()
                        break
                    except ValueError:
                        continue
                if birth_time_obj is None:
                    st.error(t("err_time"))
                    st.stop()
            profile, zodiac = build_full_profile(
                full_name.strip(),
                dob,
                birth_time_obj,
                birth_city.strip() or None,
                nickname=nickname.strip() or None,
            )
            st.session_state.profile = profile
            st.session_state.zodiac = zodiac
            st.session_state.messages = []
            st.session_state.opening_generated = False
            save_session_to_storage()
            st.rerun()
else:
    profile = st.session_state.profile
    zodiac = st.session_state.zodiac

    with st.sidebar:
        nick_display = profile.get("nickname") or profile["full_name"].split()[0]
        st.markdown(f"### 👋 Hi, **{nick_display}**")
        st.caption(f"_{profile['full_name']} · lahir {profile['dob']}_")

        with st.expander(t("angka_utama")):
            for label_key, key in [
                ("misi_hidup", "life_path"),
                ("bakat_bawaan", "expression"),
                ("panggilan_hati", "soul_urge"),
                ("aura_luar", "personality"),
                ("talenta_lahir", "birthday"),
            ]:
                num = profile[key]
                st.markdown(f"**{t(label_key)}:** `{num}` · _{ARCHETYPES[num]}_")

        with st.expander(t("aspek_detail")):
            debts = profile.get("karmic_debts") or {}
            debt_labels = {
                "life_path": t("misi_hidup"),
                "expression": t("bakat_bawaan"),
                "soul_urge": t("panggilan_hati"),
                "personality": t("aura_luar"),
            }
            active_debts = [(debt_labels[k], v) for k, v in debts.items() if v]
            if active_debts:
                st.markdown(f"**{t('pr_hidup_label')}:**")
                for lbl, val in active_debts:
                    st.markdown(f"- {lbl}: `{val}`")
            lessons = profile.get("karmic_lessons") or []
            if lessons:
                st.markdown(
                    f"**{t('pelajaran_label')}:** {', '.join(str(n) for n in lessons)}"
                )
            else:
                st.markdown(f"**{t('pelajaran_label')}:** {t('pelajaran_kosong')}")
            passion = profile.get("hidden_passion") or []
            if passion:
                names = ", ".join(f"`{n}` ({ARCHETYPES[n]})" for n in passion)
                st.markdown(f"**{t('obsesi_label')}:** {names}")
            maturity = profile.get("maturity")
            if maturity:
                st.markdown(
                    f"**{t('versi_dewasa_label')}:** `{maturity}` · _{ARCHETYPES[maturity]}_"
                )

        st.divider()

        nav_items = [
            ("🏠", t("nav_chat"), "chat"),
            ("👤", t("nav_karakter"), "karakter"),
            ("🔍", t("nav_inner"), "inner"),
            ("🎓", t("nav_karmic"), "karmic"),
            ("🎯", t("nav_fase"), "fase"),
            ("💑", t("nav_relationship"), "relationship"),
            ("🗓️", t("nav_arah"), "arah"),
            ("♈", t("nav_zodiak"), "zodiak"),
            ("🐉", t("nav_shio"), "shio"),
            ("🌿", t("nav_weton"), "weton"),
        ]
        for emoji, label, key in nav_items:
            is_active = st.session_state.current_page == key
            prefix = "✓ " if is_active else ""
            if st.button(
                f"{prefix}{emoji} {label}",
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.current_page = key
                st.rerun()

        st.divider()
        st.caption(t("storage_note"))
        if st.button(t("reset"), use_container_width=True):
            clear_session_storage()
            for key in [
                "profile", "zodiac", "messages", "opening_generated",
                "cached_pages", "relationships", "current_page",
            ]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    page = st.session_state.current_page

    if page == "chat":
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if not st.session_state.opening_generated:
            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_text = stream_assistant(
                    messages_for_api=[{"role": "user", "content": opening_prompt()}],
                    system=system_prompt(profile, zodiac, today_local()),
                    placeholder=placeholder,
                )
            st.session_state.messages.append({"role": "assistant", "content": full_text})
            st.session_state.opening_generated = True
            save_session_to_storage()
            st.rerun()

    elif page == "karakter":
        render_cached_text_page("karakter", kompleksitas_prompt, profile, zodiac)

    elif page == "inner":
        render_cached_text_page("inner", inner_prompt, profile, zodiac)

    elif page == "karmic":
        render_cached_text_page("karmic", karmic_prompt, profile, zodiac)

    elif page == "arah":
        render_cached_text_page("arah", arah_prompt, profile, zodiac)

    elif page == "fase":
        render_cached_text_page("fase", fase_prompt, profile, zodiac)

    elif page == "zodiak":
        render_cached_text_page(
            "zodiak", lambda: zodiak_prompt(zodiac), profile, zodiac,
        )

    elif page == "shio":
        render_cached_text_page(
            "shio", lambda: shio_prompt(zodiac or {}), profile, zodiac,
        )

    elif page == "weton":
        render_cached_text_page(
            "weton", lambda: weton_prompt(zodiac or {}), profile, zodiac,
        )

    elif page == "relationship":
        render_relationship_page(profile, zodiac)

    handle_chat_turn(profile, zodiac)
