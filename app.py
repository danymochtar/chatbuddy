import json
import os
from datetime import date, datetime, time

import anthropic
import streamlit as st

from numerology import (
    ARCHETYPES,
    KARMIC_DEBT_MEANINGS,
    LESSON_MEANINGS,
    build_profile,
    today_local,
)
from zodiac import JAKARTA_COORDS, SIGN_TRAITS, compute_chart, geocode_city, sun_sign

MODEL = "claude-haiku-4-5"
MAX_TOKENS = 3000
STORAGE_KEY = "chatbuddy_session_v1"


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


def base_persona() -> str:
    return (
        "Lo adalah **ChatBuddy** — teman curhat AI yang *diam-diam* pake numerologi Pythagorean "
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
    if minor_lines:
        lines += ["", "-- Minor aspects (buat kedalaman; blend halus saat relevan) --"]
        lines += minor_lines

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
        "Bikinin opening hangat dan personal buat gw — tone kyk temen deket yg udah kenal "
        "gw lama, bukan reading numerologi/astrologi. **JANGAN sebut istilah teknis** "
        "(Life Path, Sun, Moon, zodiac, rasi bintang, dst). Pake heading Markdown ## supaya "
        "jelas sectionsnya:\n\n"
        "## 👋 Halo [Nama Depan]\n"
        "Mulai dengan **1-2 kalimat synthesis** yang blend karakter gw jadi SATU KESELURUHAN — "
        "bukan list sifat satu-satu, tapi rangkaian yang mengalir, nunjukin dinamika antara "
        "misi hidup + bakat bawaan + panggilan hati + aura luar + talenta lahir. Pake kata "
        "sambung yang ngasih dinamika: 'yang', 'dan', 'tapi', 'walau', 'makanya', 'di "
        "dalemnya', 'di luar', dst. **WAJIB sertakan angka dalam kurung** setelah trait-nya — "
        "ini selain bikin referensinya clear, juga bikin user tau angka-angka penting mereka.\n\n"
        "Contoh tone (**JANGAN copy persis, selalu tailored ke user**):\n"
        "- _\"Hi Dany, lu itu born to be leader (1) yang natural-nya mengalir bebas (5), "
        "tapi di dalem jiwa lo itu penyayang banget (6) — dengan aura ambisius yang kerasa (8) "
        "plus talenta buat bikin dampak besar (8).\"_\n"
        "- _\"Hi Budi, kalo gw baca lo itu orang yang lahir buat ngayomi keluarga (6), "
        "dengan bakat ekspresi & kreativitas yang menular (3), tapi ambisi buat jadi powerful "
        "sebenernya kerasa juga (8) — aura luar yg stable (4) nutupin kompleksitas itu.\"_\n\n"
        "Kalo ada angka master (11/22/33), kasih emphasis (master vibe). "
        "Kalo 2 angka sama (kyk personality & birthday sama-sama 8), blend jadi penekanan "
        "kuat pada tema itu.\n\n"
        "## 🌞 Vibe Hari Ini\n"
        "Sebutin hari & tanggal. Rangkai energi hari ini + vibe bulan ini + tema tahun ini "
        "jadi satu cerita mengalir. Paling tebal di energi hari ini — 2-3 kalimat yg bikin "
        "gw bisa ngerasain energinya.\n\n"
        "## 👤 Kompleksitas Karakter Lo\n"
        "Zoom-in lebih dalem dari intro tadi. Ulasan 2-3 paragraf soal paradoks/harmoni "
        "antar aspek (misi vs bakat, aura luar vs panggilan hati dalem, dst). **Gabungin juga "
        "lapisan cara tampil / emosi internal / first impression** dari data tambahan — tapi "
        "tanpa pernah sebut 'astrologi' atau nama rasi.\n\n"
        "## 💡 Arah & Tips Buat Lo\n"
        "SATU section yang blend tips hari ini + bulan ini + tahun ini jadi panduan yang "
        "saling nyambung. Alurnya: dari immediate (hari ini) → zoom-out (bulan ini) → "
        "chapter besar (tahun ini). Format bebas (bisa bullet, bisa paragraf pendek) tapi "
        "hubungkan satu sama lain — bukan 3 list terpisah.\n\n"
        "Contoh alur:\n"
        "- Hari ini: [aksi spesifik sesuai energi hari ini + karakter]\n"
        "- Beberapa minggu ke depan: [tema bulan ini + cara navigatenya]\n"
        "- Chapter tahun ini: [tema tahun + apa yg bijak difokusin / di-release]\n"
        "- Hati-hati kalo: [warning dari karakter/debts yg relevan]\n\n"
        "Harus 4-6 poin total. Spesifik, actionable — bukan 'be yourself' tapi aksi yg "
        "bisa langsung dikerjain. Kalo ada karmic debt yg relevan sama energi sekarang, "
        "selipin halus.\n\n"
        "## 💬 Yuk Ngobrol\n"
        "Tutup hangat — undang ngobrol soal karir, cinta, keluarga, atau hal spesifik.\n\n"
        "**Style:** casual 'lo/gw', hangat, sedikit humor kalo pas. **Zero jargon teknis**. "
        "Astrologi WAJIB invisible."
    )


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
st.title("🔮 ChatBuddy")
st.caption("Temen AI lo buat refleksi diri")

if "profile" not in st.session_state:
    st.session_state.profile = None
if "zodiac" not in st.session_state:
    st.session_state.zodiac = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "opening_generated" not in st.session_state:
    st.session_state.opening_generated = False

if "storage_loaded" not in st.session_state:
    if st.session_state.profile is None:
        load_session_from_storage()
    st.session_state.storage_loaded = True

if st.session_state.profile is None:
    st.subheader("Kenalan dulu yuk")
    with st.form("profile_form"):
        full_name = st.text_input(
            "Nama lengkap (sesuai akta lahir)",
            placeholder="Contoh: Budi Santoso",
            help="Angka-angkanya dihitung dari nama ini",
        )
        nickname = st.text_input(
            "Panggilan / nickname (opsional)",
            placeholder="Biarin kosong buat pake nama depan",
            help="Ini yg ChatBuddy pakai buat sapa lo",
        )
        dob = st.date_input(
            "Tanggal lahir",
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            value=date(2000, 1, 1),
            format="DD/MM/YYYY",
        )
        col_time, col_city = st.columns(2)
        with col_time:
            birth_time_str = st.text_input("Jam lahir (HH:MM, opsional)", placeholder="contoh 13:30")
        with col_city:
            birth_city = st.text_input("Kota lahir (opsional)", placeholder="contoh Jakarta")
        submitted = st.form_submit_button("Mulai ngobrol →", use_container_width=True)

    if submitted:
        if not full_name.strip() or len(full_name.strip()) < 2:
            st.error("Nama lengkapnya dong biar bisa dihitung 🙏")
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
                    st.error("Format jam lahir salah. Pake `HH:MM` ya (contoh `13:30`) atau kosongin.")
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

    user_input = st.chat_input("Tulis pertanyaan atau cerita lo...")
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

    with st.sidebar:
        st.header("Sesi")
        nick_display = profile.get("nickname") or profile["full_name"].split()[0]
        st.write(f"**{nick_display}** _({profile['full_name']})_")
        st.write(f"Lahir: {profile['dob']}")
        if zodiac and zodiac.get("birth_time"):
            st.write(f"Jam: {zodiac['birth_time']}")
        if zodiac and zodiac.get("birth_city"):
            st.write(f"Kota: {zodiac['birth_city']}")

        with st.expander("📊 Angka utama"):
            for label, key in [
                ("Misi Hidup", "life_path"),
                ("Bakat Bawaan", "expression"),
                ("Panggilan Hati", "soul_urge"),
                ("Aura Luar", "personality"),
                ("Talenta Lahir", "birthday"),
            ]:
                num = profile[key]
                st.markdown(f"**{label}:** `{num}` · _{ARCHETYPES[num]}_")

        with st.expander("🔍 Aspek dalam"):
            debts = profile.get("karmic_debts") or {}
            debt_labels = {
                "life_path": "Misi Hidup", "expression": "Bakat Bawaan",
                "soul_urge": "Panggilan Hati", "personality": "Aura Luar",
            }
            active_debts = [(debt_labels[k], v) for k, v in debts.items() if v]
            if active_debts:
                st.markdown("**PR hidup (karmic debt):**")
                for lbl, val in active_debts:
                    st.markdown(f"- {lbl}: `{val}`")
            lessons = profile.get("karmic_lessons") or []
            if lessons:
                st.markdown(f"**Pelajaran hidup:** {', '.join(str(n) for n in lessons)}")
            else:
                st.markdown("**Pelajaran hidup:** lengkap (semua angka ada di nama)")
            passion = profile.get("hidden_passion") or []
            if passion:
                names = ", ".join(f"`{n}` ({ARCHETYPES[n]})" for n in passion)
                st.markdown(f"**Obsesi tersembunyi:** {names}")
            maturity = profile.get("maturity")
            if maturity:
                st.markdown(f"**Versi dewasa lo:** `{maturity}` · _{ARCHETYPES[maturity]}_")

        st.caption("💾 Sesi lo auto-tersimpen di browser — bisa tutup tab, balik lagi kapan aja.")
        if st.button("Reset sesi", use_container_width=True):
            clear_session_storage()
            st.session_state.profile = None
            st.session_state.zodiac = None
            st.session_state.messages = []
            st.session_state.opening_generated = False
            st.rerun()
