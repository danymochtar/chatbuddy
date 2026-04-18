import os
from datetime import date

import streamlit as st
from google import genai
from google.genai import types

from numerology import build_profile

MODEL = "gemini-2.0-flash"


def get_client() -> genai.Client:
    api_key = st.secrets.get("GEMINI_API_KEY") if hasattr(st, "secrets") else None
    api_key = api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY belum di-set. Tambahin di Streamlit secrets atau env variable.")
        st.stop()
    return genai.Client(api_key=api_key)


def system_prompt(profile: dict) -> str:
    return (
        "Lo adalah ChatBuddy — AI teman deket yang ngerti numerologi Pythagorean "
        "dan pake data numerologi user buat ngejawab pertanyaan mereka soal hidup, "
        "personality, karir, percintaan, pertemanan, keluarga, dan masalah personal lainnya.\n\n"
        "Gaya ngomong lo:\n"
        "- Casual, santai, kyk temen deket (pake 'lo/gw' atau 'kamu/aku' sesuai vibe user)\n"
        "- Empatik, ga judgemental, dengerin dulu sebelum ngasih saran\n"
        "- Jujur tapi hangat — kalau ada sisi 'gelap' dari angka, sampein dengan cara yang membangun\n"
        "- Hindari jargon numerologi yang terlalu berat, jelasin pake bahasa sehari-hari\n"
        "- Jangan kyk horoskop murahan — kasih insight yang nyambung sama situasi user\n\n"
        "Aturan penting:\n"
        "- Numerologi adalah lensa buat refleksi diri, bukan ramalan pasti. Ingetin user kalau perlu.\n"
        "- Kalau user cerita masalah berat (mental health, kekerasan, krisis), tetap suportif "
        "tapi arahin juga ke bantuan profesional.\n"
        "- Jawaban lo harus selalu nyambung sama profil numerologi di bawah ini.\n\n"
        f"=== PROFIL NUMEROLOGI USER ===\n"
        f"Nama: {profile['full_name']}\n"
        f"Tanggal Lahir: {profile['dob']}\n\n"
        f"Life Path Number: {profile['life_path']} — {profile['meanings']['life_path']}\n"
        f"Expression/Destiny Number: {profile['expression']} — {profile['meanings']['expression']}\n"
        f"Soul Urge Number: {profile['soul_urge']} — {profile['meanings']['soul_urge']}\n"
        f"Personality Number: {profile['personality']} — {profile['meanings']['personality']}\n"
        f"Birthday Number: {profile['birthday']} — {profile['meanings']['birthday']}\n\n"
        "Arti singkat masing-masing angka:\n"
        "- Life Path: tujuan & pelajaran hidup utama\n"
        "- Expression: bakat bawaan & cara natural lo berkontribusi ke dunia\n"
        "- Soul Urge: motivasi terdalam, apa yang bikin lo bahagia di hati\n"
        "- Personality: gimana orang lain lihat lo di first impression\n"
        "- Birthday: talenta spesifik yang lo bawa sejak lahir\n"
    )


def to_gemini_contents(messages: list) -> list:
    contents = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))
    return contents


def render_profile(profile: dict) -> None:
    cols = st.columns(5)
    labels = [
        ("Life Path", profile["life_path"]),
        ("Expression", profile["expression"]),
        ("Soul Urge", profile["soul_urge"]),
        ("Personality", profile["personality"]),
        ("Birthday", profile["birthday"]),
    ]
    for col, (label, num) in zip(cols, labels):
        col.metric(label, num)

    with st.expander("Arti angka-angka kamu"):
        for key in ["life_path", "expression", "soul_urge", "personality", "birthday"]:
            name = key.replace("_", " ").title()
            st.markdown(f"**{name} ({profile[key]}):** {profile['meanings'][key]}")


def initial_reading(profile: dict) -> str:
    return (
        f"Halo **{profile['full_name'].split()[0]}**! Gw ChatBuddy, temen AI lo yang pake "
        f"lensa numerologi buat ngobrol soal hidup. Udah gw itung angka-angka lo di atas — "
        f"Life Path lo **{profile['life_path']}** ({profile['meanings']['life_path'].lower()}) "
        f"jadi benang merah perjalanan hidup lo.\n\n"
        f"Mau mulai dari mana? Karir, percintaan, pertemanan, keluarga, "
        f"atau ada masalah spesifik yang lagi lo pikirin? Ceritain aja, gw dengerin."
    )


st.set_page_config(page_title="ChatBuddy Numerologi", page_icon="🔮", layout="centered")
st.title("🔮 ChatBuddy Numerologi")
st.caption("Temen AI lo, dibantu lensa numerologi buat refleksi diri")

if "profile" not in st.session_state:
    st.session_state.profile = None
if "messages" not in st.session_state:
    st.session_state.messages = []

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
        submitted = st.form_submit_button("Mulai ngobrol →", use_container_width=True)

    if submitted:
        if not full_name.strip() or len(full_name.strip()) < 2:
            st.error("Nama lengkapnya dong biar bisa dihitung 🙏")
        else:
            profile = build_profile(full_name.strip(), dob)
            st.session_state.profile = profile
            st.session_state.messages = [
                {"role": "assistant", "content": initial_reading(profile)}
            ]
            st.rerun()
else:
    profile = st.session_state.profile
    render_profile(profile)
    st.divider()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Tulis pertanyaan atau cerita lo...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        client = get_client()
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_text = ""
            stream = client.models.generate_content_stream(
                model=MODEL,
                contents=to_gemini_contents(st.session_state.messages),
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt(profile),
                ),
            )
            for chunk in stream:
                if chunk.text:
                    full_text += chunk.text
                    placeholder.markdown(full_text + "▌")
            placeholder.markdown(full_text)

        st.session_state.messages.append({"role": "assistant", "content": full_text})

    with st.sidebar:
        st.header("Sesi")
        st.write(f"**{profile['full_name']}**")
        st.write(f"Lahir: {profile['dob']}")
        if st.button("Reset sesi", use_container_width=True):
            st.session_state.profile = None
            st.session_state.messages = []
            st.rerun()
