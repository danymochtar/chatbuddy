import json
import os
from datetime import date, datetime, time

import anthropic
import streamlit as st

from numerology import ARCHETYPES, build_profile, today_local
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
        "'energi hari ini', 'vibe bulan ini', 'tema tahun ini'.\n\n"
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
    lines = [
        "=== PROFIL USER (konteks internal — jangan expose istilahnya) ===",
        f"Nama: {profile['full_name']}",
        f"Tanggal lahir: {profile['dob']}",
        "",
        "-- Baca karakter (JANGAN sebut istilah teknisnya) --",
        f"Misi hidup / tema besar: {profile['meanings']['life_path']}",
        f"Bakat bawaan / karakter natural: {profile['meanings']['expression']}",
        f"Panggilan hati / apa yg dia butuh buat bahagia: {profile['meanings']['soul_urge']}",
        f"Aura luar / first impression: {profile['meanings']['personality']}",
        f"Talenta spesifik dari hari lahir: {profile['meanings']['birthday']}",
    ]
    if zodiac and zodiac.get("sun"):
        lines += [
            "",
            "-- Lapisan tambahan (WAJIB DISEMBUNYIKAN — blend ke observasi) --",
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
        f"Tema tahun ini: {profile['meanings']['personal_year']}\n"
        f"Vibe bulan ini (angka {profile['personal_month']}): ulas berdasarkan tema angka\n"
        f"Energi hari ini: {profile['meanings']['personal_day']}\n\n"
        "Pake ini buat kasih konteks timing dan tips praktis. "
        "JANGAN sebut 'Personal Day/Month/Year' — sampein kyk lo emang 'tau' vibe-nya."
    )


def system_prompt(profile: dict, zodiac: dict | None, today: date) -> list:
    text = "\n\n".join([base_persona(), profile_block(profile, zodiac), daily_block(profile, today)])
    return [{"type": "text", "text": text, "cache_control": {"type": "ephemeral"}}]


def opening_prompt() -> str:
    return (
        "Bikinin opening hangat dan personal buat gw — tone kyk temen deket yg udah kenal "
        "gw lama, bukan reading numerologi/astrologi. **JANGAN sebut istilah teknis**. "
        "Pake heading Markdown ## supaya jelas sectionsnya:\n\n"
        "## 🌞 Vibe Hari Ini\n"
        "Sapa gw pake nama depan, sebutin hari & tanggal. Rangkai energi hari ini + vibe bulan "
        "ini + tema tahun ini jadi **satu cerita mengalir** (bukan daftar). Paling tebal di "
        "energi hari ini — 2-3 kalimat yg bikin gw bisa ngerasain energinya.\n\n"
        "## 👤 Siapa Lo, Menurut Gw\n"
        "Ulasan karakter — cerita 'siapa lo'. Gabungin observasi dari misi hidup, bakat "
        "bawaan, panggilan hati, aura luar, talenta lahir **+ lapisan cara tampil / emosi "
        "internal / first impression** jadi narasi utuh. Highlight paradoks/harmoni kalo ada. "
        "Min 2 paragraf.\n\n"
        "## 💡 Tips Buat Hari Ini\n"
        "3-4 tips praktis yang nyambung sama energi hari ini + karakter lo. Bullet points. "
        "Spesifik & actionable. Contoh bentuk: 'Hari bagus buat...', 'Hindarin dulu...', "
        "'Kalo ada keputusan soal X, pertimbangin...'.\n\n"
        "## 🗓️ Tips Bulan Ini\n"
        "2-3 tips zoom-out buat sebulan. Tema besarnya apa? Apa yg cocok di-prioritize / "
        "dihindari bulan ini?\n\n"
        "## 🌱 Tema Tahun Ini\n"
        "1 paragraf soal tema besar tahun ini — apa chapter yg lo jalanin, apa yang bijak "
        "difokusin / di-release sepanjang tahun.\n\n"
        "## 💬 Yuk Ngobrol\n"
        "Tutup hangat — undang ngobrol soal karir, cinta, keluarga, atau hal spesifik yg "
        "nyambung sama vibe hari ini.\n\n"
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
) -> tuple[dict, dict]:
    profile = build_profile(full_name, dob)
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
        full_name = st.text_input("Nama lengkap (sesuai akta lahir)", placeholder="Contoh: Budi Santoso")
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
    render_profile_panel(profile)

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
        st.write(f"**{profile['full_name']}**")
        st.write(f"Lahir: {profile['dob']}")
        if zodiac and zodiac.get("birth_time"):
            st.write(f"Jam: {zodiac['birth_time']}")
        if zodiac and zodiac.get("birth_city"):
            st.write(f"Kota: {zodiac['birth_city']}")
        st.caption("💾 Sesi lo auto-tersimpen di browser — bisa tutup tab, balik lagi kapan aja.")
        if st.button("Reset sesi", use_container_width=True):
            clear_session_storage()
            st.session_state.profile = None
            st.session_state.zodiac = None
            st.session_state.messages = []
            st.session_state.opening_generated = False
            st.rerun()
